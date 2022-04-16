import h5py
import pandas as pd
import hdf5_getters
import os
import tables
root = './MillionSongSubset/'
allfiles = []

for path, subdirs, files in os.walk(root):  #Getting list of files
    for name in files:
        if '.h5' in name:
            allfiles.append(os.path.join(path, name))

cols = []
for file in allfiles[:1]:  #Getting column names
    h = hdf5_getters.open_h5_file_read(file)
    for i in dir(hdf5_getters):
            item = getattr(hdf5_getters,i)
            if callable(item) and i!='open_h5_file_read':
                cols.append(i.split('get_')[1])


def file_content(file):
    h = hdf5_getters.open_h5_file_read(file)
    lsstr = ''
    for i in dir(hdf5_getters):
            item = getattr(hdf5_getters,i)
            if callable(item) and i!='open_h5_file_read':
                lsstr = lsstr + str(item(h)).replace(',','') +','
                #fs.append(item(h))
    return lsstr[:-1]


with open('output.csv','w') as csvfile:
    csvfile.write(",".join(cols))
    csvfile.write('\n')
    i=0
    for file in allfiles:
        i += 1
        if i%100 == 0:
            print(i)
            tables.file._open_files.close_all()
        string = file_content(file)
        csvfile.write(string.replace('\n',''))
        csvfile.write('\n')
