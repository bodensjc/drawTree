import sys, os, shutil
import glob, win32com.client
import re
from re import search


#***********************************************************************************************************************************************************************************
#this group loacates and lists all of the folder/files in the selected directory

#lists all contents of a parent directory, including shortcut targets.
#may be prone to recursive shortcuts... somethign to think about
def listDirs(path):
    dirList=[]
    shortcuts = glob.glob(path + '/**/**/*.lnk', recursive=True)
    if len(shortcuts) > 0:
        shell = win32com.client.Dispatch("WScript.Shell")
        for shortcut in shortcuts:
            shortcut = shell.CreateShortCut(shortcut)
            shortcutDirs = listDirs(shortcut.TargetPath)
            dirList.append(shortcutDirs)
    pathDirs = glob.glob(path + '/*/*/*', recursive=True)
    dirList.append(pathDirs)

    return dirList



def flatten(lst):
    if lst == []:
        return []
    elif type(lst[0]) == list:
        return flatten([i for i in lst[0]]) + flatten(lst[1:])
    else:
        return [lst[0]] + flatten(lst[1:])

#**************************************************************************************************************************************************************************************
# this group seperates the input into the parts we need in order to find and match the correct .stp and .dat files

def psrCopy(fileName):
    content = fileName.split('_')
    year, psrNum, program, tireSize, ATC = content[0], content[1]+'_'+content[2], content[3], content[4]+'_'+content[5], content[6][1:-1]
    #********************************************************
    yearPath = 'Z:\\LnT\\DuelerLX_18Models\\Working Folder\\{0}_PSR_request'.format(year) #set path for psr year THIS MUST BE CHANGED DEPENDING ON USER
    #********************************************************
    #print( year, psrNum, program, tireSize, ATC)
    ''' 
    if os.path.exists(yearPath):
        print('this is a valid path')
    elif not os.path.exists(yearPath):
        print('this is not a valid path')
    '''
#**********************************************************************************************************************************************************************************
# this group creates the to & from LnT folders we need

    newFile = '_'.join([year,psrNum,program,tireSize])+'_({0})'.format(ATC) #newFile name for folders
    newFilePath = os.path.join(dir_path, newFile)
    os.mkdir(newFilePath)
    toLnT = os.path.join(newFilePath, 'to_LnT') #files go here
    fromLnT = os.path.join(newFilePath, 'from_LnT')#create this for future use
    os.mkdir(toLnT)
    os.mkdir(fromLnT)

    #print(listDirs(yearPath))

    dirs = flatten(listDirs(yearPath)) #list all folders and their contents
    print(listDirs(yearPath))
    #print (dirs)

#**********************************************************************************************************************************************************************************
# this is the group that finds the .stp files and .dat files

    boundaries = ATC+r'\_boundaries_for_cut.dat'
    print(boundaries)
    boundariesPath = None
    for f in dirs:
        print(f)
        if (f.find(boundaries) != -1):
            print('_boundaries_for_cut.dat file found in ', f)
            boundariesPath = f
        else:
            continue
    if boundariesPath is not None:
        shutil.copy(boundariesPath, toLnT)
        print('_boundaries_for_cut.dat copied to ', toLnT)
    else:
        print('_boundaries_for_cut.dat file not found, exiting program.')
        exit()


    stpPath = None
    for f in dirs:
        if (f.find(tireSize) != -1) and (f.endswith(r'.stp')):
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

#************************************************************************************************************************************************************************************
# this group copies the found files into the corresponding folders

def groupCopy(fileName):
    content = fileName.split('_')
    year, psrNum, program, tireSize, ATC = content[0], content[1]+'_'+content[2], content[3], content[4]+'_'+content[5], content[6][1:-1]
    #********************************************************
    yearPath = 'Z:\\LnT\\DuelerLX_18Models\\Working Folder\\{0}_PSR_request'.format(year) #set path for psr year, THIS MUST BE CHANGED DEPENDING ON USER
    #********************************************************
    newFile = '_'.join([year,psrNum,program]) #newFile name for folders
    newFilePath = os.path.join(groupPath, newFile)
    newFilePath = os.path.join(newFilePath, 'toLnT')
    infoFile = '_'.join([year,psrNum,program,tireSize,ATC]) #file for where the toLnT comes from
    source = os.path.join(dir_path, infoFile)
    toLnT = os.path.join(source, 'to_LnT')
    destination = shutil.copytree(toLnT, newFilePath)

#***********************************************************************************************************************************************************************************
# this is the input promts required


if __name__ == '__main__':
    #WARNING: the python file must be in the folder with all of the intended PSR folders "group"
    files = open('PSRnames.txt','r')
    fileNames = files.readlines()
    group = str(sys.argv[1])
    dir_path = os.path.dirname(os.path.realpath(__file__))
    
    
    for fileName in fileNames:

        PSR_list = fileName.split(" ")
        
        groupName = 'Group'+group
        
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
            
        
