import shutil, os
from os import walk

myfilenames = ['test1.txt', 'test3.txt'] #replace with
parent = 'C:\\Users\\johnb\\Documents\\python\\testRepo' #replace with your parent directory that holds all of the P0 files
os.chdir(parent)
_, pfolders, _ = next(walk(parent))


def pcopy(source, dest):
    _, _, filenames = next(walk(source))
    for f in filenames:
        if f in myfilenames:
            shutil.copy(f, dest)


for pfolder in pfolders:
    currentPath = os.path.join(parent, pfolder)
    destPath = os.path.join(parent, pfolder+'copy')
    _, first, _ = next(walk(currentPath))
    os.mkdir(destPath)
    pcopy(currentPath, destPath)






