import sys
import os
import argparse
import glob
import shutil

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

def fileExtraction(PATH):
    dirName = PATH
    listOfFiles = getListOfFiles(dirName)
    fileNames = []
    for elem in listOfFiles:
        print(elem)
        base_filename = os.path.basename(elem)
        filePattern, fileExtension = os.path.splitext(base_filename)
        fileNames.append(filePattern)
    fileNames.sort()
    return fileNames

def folderNameExtraction(PATH):
    dir_list = os.walk(PATH).__next__()[1]
    dir_list.sort()
    return dir_list

def returnUnmatches(input, output):
    FLAG  = 0
    Unmatches = list(set(input).difference(output))
    for elem in Unmatches:
        print(elem)
        FLAG+=1
    print(FLAG)
    moveUnmatches(Unmatches)

def moveUnmatches(unmatch):
    os.mkdir("STLFILES1")
    suffix = ".stl"
    outputdirectory = os.path.join(os.getcwd(), "STLFILES1")
    FLAG = 0
    for elem in unmatch:
        os.chdir("STLFILES")
        filename = elem + suffix
        shutil.move(os.path.join(os.getcwd(), filename), os.path.join(outputdirectory, filename))
        FLAG += 1
        print("{} moved sucessfully".format(filename))
        os.chdir("..")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Resume conversion from left off')
    parser.add_argument('-i', "--string1", type = str, required = True)
    parser.add_argument("-o", "--string2", type=str, required=True)
    args = parser.parse_args()
    INPUTPATH = os.path.join(os.getcwd(), args.string1)
    OUTPUTPATH = os.path.join(os.getcwd(), args.string2)
    INPUTFILENAMES = fileExtraction(INPUTPATH)
    OUTPUTFILENAMES = folderNameExtraction(OUTPUTPATH)  
    returnUnmatches(INPUTFILENAMES, OUTPUTFILENAMES)
