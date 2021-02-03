import glob

path = 'C:\\Users\\johnb\\Documents\\python\\testRepo'

text_files = glob.glob(path + '/**/*.txt', recursive=True)

print(text_files)

