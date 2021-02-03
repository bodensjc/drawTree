import shutil, os
from os import walk
from sys import argv
import re, string


def pcopy(source, dest):
    _, _, filenames = next(walk(source))
    for f in filenames:
        if f in myfilenames:
            shutil.copy(f, dest)
    return None


if __name__ == '__main__':
    if len(argv) > 1:
        PSRnum = str(argv[1]) # '0023'
    else:
        print('no PSR number given')
        exit()


    myfilenames = ['2020_PSR_{0}.stp'.format(PSRnum), 'PSR1000_{0}.xls'.format(PSRnum)]

    parent = 'C:\\Users\\johnb\\Documents\\python\\testRepo' #replace with your parent directory that holds all of the P0 files
    os.chdir(parent)
    _, pfolders, _ = next(walk(parent))

    for pfolder in pfolders:
        if pfolder[8:12] == PSRnum:
            currentPath = os.path.join(parent, pfolder)
            destPath = os.path.join(currentPath, 'to_LnT')
            os.mkdir(destPath)
            pcopy(currentPath, destPath)
    



