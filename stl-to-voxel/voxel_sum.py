import os
import cv2
import glob

class voxelSum(object):

    def __init__(self, FOLDERNAME):
        self.FLAG = 0
        self.CURRENTPATH = os.getcwd()
        self.FOLDERNAME = FOLDERNAME 
        self.INPUTPATH = os.path.join(self.CURRENTPATH,"*.png")
        os.chdir('..')
        os.mkdir('output')
        os.chdir('output')
        self.FILENAMES = self.fileNameExtraction()
        self.images = self.readImages()
        self.voxelSummation()


    ## IMAGES FILENAME EXTRACTION FROM THE DIRECTORY ##
    def fileNameExtraction(self):    
        FILENAMES = [img for img in glob.glob(self.INPUTPATH)]
        FILENAMES.sort()
        return FILENAMES

    ## READING IMAGES AND STORING IN THE LIST ##
    def readImages(self):    
        images = []
        for img in self.FILENAMES:
            n= cv2.imread(img)
            images.append(n)
        return images

    ## SUMMATION OF VOXEL IMAGES LAYERWISE AND STORING OUTPUT IMAGES ##
    def voxelSummation(self):    
        for val in range(len(self.images)):
            if val == len(self.images)-1:
                break
            out = cv2.addWeighted(self.images[val],1,self.images[val+1],1,0)
            self.images[val+1] = out
            self.FLAG+=1
            FOLDERNAME = os.path.dirname(self.FOLDERNAME)
            OUTPUTFILE = FOLDERNAME + str(self.FLAG) + ".png"
            os.chdir('..')
            os.chdir('output')
            CURRENTPATH = os.getcwd()
            OUTPUTPATH = os.path.join(CURRENTPATH, OUTPUTFILE)
            cv2.imwrite(OUTPUTPATH,self.images[val])