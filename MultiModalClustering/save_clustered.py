import os, shutil
from glob import glob
import pandas as pd

def group_move(data,path):
    dir_names = [os.path.join(path,i) for i in data.Label.unique()]

    for name in dir_names:
        if not os.path.isdir(name):
            os.mkdir(name)
    
    for source, label in data[['Img_src','Label']].values:
        source = os.path.join(path,source)
        dest = os.path.join(path,label)

        shutil.move(source, dest)
