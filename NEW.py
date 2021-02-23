import sys, os, shutil
import glob, win32com.client
import re
from re import search


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


def psrCopy(fileName):
    content = fileName.split('_')
    year, psrNum, program, tireSize_ATC = content[0], content[1]+'_'+content[2], content[3], content[4]+'_'+content[5]
    #********************************************************
    yearPath = 'C:\\Users\\johnb\\Documents\\python\\testRepo\\{0}_PSR_requests'.format(year) #set path for psr year
    #********************************************************

    newFile = '_'.join([year,psrNum,program,tireSize_ATC]) #newFile name for folders
    newFilePath = os.path.join(dir_path, newFile)
    os.mkdir(newFilePath)
    toLnT = os.path.join(newFilePath, 'to_LnT') #files go here
    fromLnT = os.path.join(newFilePath, 'from_LnT')#create this for future use
    os.mkdir(toLnT)
    os.mkdir(fromLnT)

    dirs = flatten(listDirs(yearPath)) #list all folders and their contents


    boundaries = tireSize_ATC+r'\_boundaries_for_cut.dat'
    boundariesPath = None
    for f in dirs:
        if boundaries in f:
            print('_boundaries_for_cut.dat file found in ', f)
            boundariesPath = f
        else:
            pass
    if boundariesPath is not None:
        shutil.copy(boundariesPath, toLnT)
        print('_boundaries_for_cut.dat copied to ', toLnT)
    else:
        print('_boundaries_for_cut.dat file not found, exiting program.')
        exit()


    stpPath = None
    for f in dirs:
        if (f.find(tireSize_ATC) != -1) and (f.endswith(r'.stp')):
            print('stp file found in ', f)
            stpPath = f
        else:
            pass
    if stpPath is not None:
        shutil.copy(stpPath, toLnT)
        print('stp copied to ', toLnT)
    else:
        print('STP file not found, exiting program')
        exit()


def groupCopy(fileName):
    content = fileName.split('_')
    year, psrNum, program, tireSize_ATC = content[0], content[1]+'_'+content[2], content[3], content[4]+'_'+content[5]
    #********************************************************
    yearPath = 'C:\\Users\\johnb\\Documents\\python\\testRepo\\{0}_PSR_requests'.format(year) #set path for psr year
    #********************************************************
    newFile = '_'.join([year,psrNum,program]) #newFile name for folders
    newFilePath = os.path.join(groupPath, newFile)
    newFilePath = os.path.join(newFilePath, 'toLnT')
    infoFile = '_'.join([year,psrNum,program,tireSize_ATC]) #file for where the toLnT comes from
    source = os.path.join(dir_path, infoFile)
    toLnT = os.path.join(source, 'to_LnT')
    destination = shutil.copytree(toLnT, newFilePath)




if __name__ == '__main__':
    #WARNING: the python file must be in the folder with all of the intended PSR folders "group"
    dir_path = os.path.dirname(os.path.realpath(__file__))#get directory that python file is in
    fileName = str(input('Input the file name (yyyy_PSR_nnnn_program_tiresize_ATC):\n'))
    group = str(input('What group is this file in (enter capital letter)? Hit \'Enter\' if not in a group.\n'))
    
    psrCopy(fileName)

    if group == '':
        print('File is not going to be put in a group.')
    else:
        groupName = 'Group'+group
        groupPath = os.path.join(dir_path, groupName)
        if not os.path.exists(groupPath):
            ('Group folder not found, created new folder.')
            os.mkdir(groupPath)
        groupCopy(fileName)
        


    #test psr
    '2020_PSR_0038_RE980_225_40R18(165503)'
    '2020_PSR_0038_RE980'
    '''

    '''





