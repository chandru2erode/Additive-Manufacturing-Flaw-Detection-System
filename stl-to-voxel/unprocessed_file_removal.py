import sys
import os
import argparse
import glob
import shutil

def folderNameExtraction(PATH):
    dir_list = os.walk(PATH).__next__()[1]
    dir_list.sort()
    return dir_list

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Remove unprocessed folders from output directory')
    parser.add_argument('-i', "--string1", type = str, required = True)
    args = parser.parse_args()
    INPUTPATH = os.path.join(os.getcwd(), args.string1)
    dir_list_files = folderNameExtraction(INPUTPATH)
    dir_list_files.sort()
    FLAG = 0
    FLAG1 = 0
    os.chdir(args.string1)
    for elem in dir_list_files:
        os.chdir(elem)
        sub_directory_list = folderNameExtraction(os.getcwd())
        FLAG += 1
        if "output" not in sub_directory_list:
            os.chdir("..")
            print("{} folder removed".format(elem))
            shutil.rmtree(elem)
            FLAG1 += 1
        else:
            os.chdir("..")
    print("{} file processed".format(FLAG))
    print("{} files removed".format(FLAG1))
