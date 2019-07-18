import argparse
import os.path
import io
import xml.etree.cElementTree as ET
from zipfile import ZipFile
import zipfile
import os
import glob

from PIL import Image
import numpy as np

import slice
import stl_reader
import perimeter
from util import arrayToWhiteGreyscalePixel, padVoxelArray
from voxel_sum import voxelSum

def doExport(inputFilePath, outputFilePath, resolution, FOLDERNAME):
    mesh = list(stl_reader.read_stl_verticies(inputFilePath))
    (scale, shift, bounding_box) = slice.calculateScaleAndShift(mesh, resolution)
    mesh = list(slice.scaleAndShiftMesh(mesh, scale, shift))
    #Note: vol should be addressed with vol[z][x][y]
    vol = np.zeros((bounding_box[2],bounding_box[0],bounding_box[1]), dtype=bool)
    for height in range(bounding_box[2]):
        print('Processing layer %d/%d'%(height+1,bounding_box[2]))
        lines = slice.toIntersectingLines(mesh, height)
        prepixel = np.zeros((bounding_box[0], bounding_box[1]), dtype=bool)
        perimeter.linesToVoxels(lines, prepixel)
        vol[height] = prepixel
    vol, bounding_box = padVoxelArray(vol)
    outputFilePattern, outputFileExtension = os.path.splitext(outputFilePath)
    currentPath = os.getcwd()
    outputFilePath = os.path.join(currentPath, outputFilePath)
    if outputFileExtension == '.png':
        exportPngs(vol, bounding_box, outputFilePath)
    elif outputFileExtension == '.xyz':
        exportXyz(vol, bounding_box, outputFilePath)
    elif outputFileExtension == '.svx':
        exportSvx(vol, bounding_box, outputFilePath, scale, shift)
    voxelSum(FOLDERNAME)
    for i in range(2):    
        os.chdir('..')

def exportPngs(voxels, bounding_box, outputFilePath):
    size = str(len(str(bounding_box[2]))+1)
    outputFilePattern, outputFileExtension = os.path.splitext(outputFilePath)
    for height in range(bounding_box[2]):
        img = Image.new('L', (bounding_box[0], bounding_box[1]), 'black')  # create a new black image
        pixels = img.load()
        arrayToWhiteGreyscalePixel(voxels[height], pixels)
        path = (outputFilePattern + "%0" + size + "d.png")%height
        img.save(path)

def exportXyz(voxels, bounding_box, outputFilePath):
    output = open(outputFilePath, 'w')
    for z in range(bounding_box[2]):
        for x in range(bounding_box[0]):
            for y in range(bounding_box[1]):
                if voxels[z][x][y]:
                    output.write('%s %s %s\n'%(x,y,z))
    output.close()

def exportSvx(voxels, bounding_box, outputFilePath, scale, shift):
    size = str(len(str(bounding_box[2]))+1)
    root = ET.Element("grid", attrib={"gridSizeX": str(bounding_box[0]),
                                      "gridSizeY": str(bounding_box[2]),
                                      "gridSizeZ": str(bounding_box[1]),
                                      "voxelSize": str(1.0/scale[0]/1000), #STL is probably in mm, and svx needs meters
                                      "subvoxelBits": "8",
                                      "originX": str(-shift[0]),
                                      "originY": str(-shift[2]),
                                      "originZ": str(-shift[1]),
                                      })
    channels = ET.SubElement(root, "channels")
    channel = ET.SubElement(channels, "channel", attrib={
        "type":"DENSITY",
        "slices":"density/slice%0" + size + "d.png"
    })
    manifest = ET.tostring(root)
    with ZipFile(outputFilePath, 'w', zipfile.ZIP_DEFLATED) as zipFile:
        for height in range(bounding_box[2]):
            img = Image.new('L', (bounding_box[0], bounding_box[1]), 'black')  # create a new black image
            pixels = img.load()
            arrayToWhiteGreyscalePixel(voxels[height], pixels)
            output = io.BytesIO()
            img.save(output, format="PNG")
            zipFile.writestr(("density/slice%0" + size + "d.png")%height, output.getvalue())
        zipFile.writestr("manifest.xml",manifest)


def file_choices(choices,fname):
    filename, ext = os.path.splitext(fname)
    if ext == '' or ext not in choices:
        if len(choices) == 1:
            parser.error('%s doesn\'t end with %s'%(fname,choices))
        else:
            parser.error('%s doesn\'t end with one of %s'%(fname,choices))
    return fname

def getListOfFiles(dirName):

        listOfFile = os.listdir(dirName)
        allFiles = list()

        for entry in listOfFile:
            fullPath = os.path.join(dirName, entry)
            if os.path.isdir(fullPath):
                allFiles = allFiles + getListOfFiles(fullPath)
            else:
                allFiles.append(fullPath)  
        return allFiles        
 
 
def fileExtraction(PATH, inputString):
    dirName = PATH
    listOfFiles = getListOfFiles(dirName)
    FLAG = 0   
    for elem in listOfFiles:
        FLAG+=1
        base_filename = os.path.basename(elem)
        suffix = ".png"
        filePattern, fileExtension = os.path.splitext(base_filename)
        output = os.path.join(filePattern + suffix)
        os.makedirs(os.path.join(filePattern, "input"))
        os.chdir(os.path.join(filePattern, "input"))
        print(os.getcwd())
        print("Processing file {} ................".format(filePattern))
        doExport(elem, output, 100, filePattern)
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert STL files to voxels')
    parser.add_argument('-i', "--string1", type = str, required = True)
    parser.add_argument("-o", "--string2", type=str, required=True)
    args = parser.parse_args()
    os.mkdir(args.string2)
    PATH = os.path.join(os.getcwd(), args.string1)
    os.chdir(args.string2)
    fileExtraction(PATH, args.string1)