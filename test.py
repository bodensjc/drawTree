import os

if __name__ == '__main__':
    #WARNING: the python file must be in the folder with all of the intended PSR folders "group"
    dir_path = os.path.dirname(os.path.realpath(__file__))#get directory that python file is in
    fileName = str(input('Input the file name (yyyy_PSR_nnnn_program_tiresize_ATC):\n'))

    content = fileName.split('_')
    year, psrNum, program, tireSize_ATC = content[0], content[1]+'_'+content[2], content[3], content[4]+'_'+content[5]
    #********************************************************
    yearPath = 'C:\\Users\\johnb\\Documents\\python\\testRepo\\{0}_PSR_requests'.format(year) #set path for psr year
    #********************************************************
    print('testing path:', yearPath)

    if os.path.exists(yearPath):
        print('this is a valid path.')
    elif not os.path.exists(yearPath):
        print('this is not a valid path')
        


    #test psr
    '2020_PSR_0038_RE980_225_40R18(165503)'
 





