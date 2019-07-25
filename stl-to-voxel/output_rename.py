import os
import argparse

def folder_name_extraction(path):
    """Return the foldernamae of the root directory."""
    dir_list = os.walk(path).__next__()[1]
    dir_list.sort()
    return dir_list

if __name__ == '__main__':
    PARSER = argparse.ArgumentParser(description='Rename output file names with unique name')
    PARSER.add_argument('-i', "--output", type=str, required=True)
    ARGS = PARSER.parse_args()
    INPUTPATH = os.path.join(os.getcwd(), ARGS.output)
    DIR_LIST_FILES = folder_name_extraction(INPUTPATH)
    DIR_LIST_FILES.sort()
    os.chdir(ARGS.output)

    for elem in DIR_LIST_FILES:
        os.chdir(elem)
        output_list = os.listdir("output")
        os.chdir("output")
        FLAG = 0
        for filename in output_list: 
            dst = elem + "_pr_" + str(FLAG) + ".png"
            src = filename 
            dst = dst
            try: 
                os.rename(src, dst)
            except FileExistsError:
                print("{} already renamed".format(filename))
                pass
            FLAG += 1
            print("{} File changed in {}".format(FLAG,elem))
        for i in range(2):    
            os.chdir("..")
        print("{} completed".format(elem))

