import os
path =r'D:\HOME\Informatics\controllers\test00\images'
filenames = os.listdir(path)

#Iterate through all files in a folder
for filename in filenames:
    #Check if the file size is empty
    if os.stat(os.path.join(path,filename)).st_size == 0:
        #Slicing the file name and changing the extension to png
        os.remove(os.path.join(path,filename[:-3]+'png'))
        #Delete empty annotation text files
        os.remove(os.path.join(path,filename))
        print(f"Empty annotation: {filename} and it's image has now being removed")
