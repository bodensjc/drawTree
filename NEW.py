import sys, os, shutil
import glob, win32com.client
import re

path = 'C:\\Users\\johnb\\Documents\\python\\testRepo\\2020_PSR_Requests'
filenames=['_boundaries_for_cut.dat', 'otherfile.txt']

#lists all contents of a parent directory, including shortcut targets.
#may be prone to recursive shortcuts... somethign to think about
def listDirs(path):
    dirList=[]
    shortcuts = glob.glob(path + '/**/*.lnk', recursive=True)
    if len(shortcuts) > 0:
        shell = win32com.client.Dispatch("WScript.Shell")
        for shortcut in shortcuts:
            shortcut = shell.CreateShortCut(shortcut)
            shortcutDirs = listDirs(shortcut.TargetPath)
            dirList.append(shortcutDirs)
    pathDirs = glob.glob(path + '/*/*', recursive=True)
    dirList.append(pathDirs)

    return dirList


def flatten(lst):
    if lst == []:
        return []
    elif type(lst[0]) == list:
        return flatten([i for i in lst[0]]) + flatten(lst[1:])
    else:
        return [lst[0]] + flatten(lst[1:])


def findPSR(num, lst):

    return psrPath, psr
    pass


def getParts(psrName):
    parts = psrName.split('_')
    year, psr, model, tail = parts[0], parts[1], parts[2], parts[3]+'_'+parts[4]
    return year, psr, model, tail




if __name__ == '__main__':
    year = str(input('What is the year?\n')) #get the year
    PSRnum = str(input('What is the PSR number?\n')).zfill(4) #get the psr number
    print(year, PSRnum)

    dirs = flatten(listDirs('C:\\Users\\johnb\\Documents\\python\\testRepo\\2020_PSR_Requests')) #list all folders and their contents
    print(dirs)

    #psrPath, psr = findPSR(PSRnum, dirs) #find the psrPath (where files need to go) and full psr name
    #parts = getParts(psr) #get the parts of the psr: year, num, model, tail
    psr = '2020_PSR0038_RE980_225_40R18(165503)'
    print(getParts(psr))

    #re.match(r'(ftp|http).*\.(jpg|png)$', f)



    #shutil.copy(f, psrPATH)













