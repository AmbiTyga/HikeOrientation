import os, shutil
from glob import glob
import pandas as pd


def group_move(data, path):

    # Get Clusters' name
    dir_names = [os.path.join(path, str(i)) for i in data.Label.unique()]

    # Make directory based on clusters' name
    for name in dir_names:
        if not os.path.isdir(name):
            os.mkdir(name)

    # Move images to their respective cluster
    for source, label in data[["Img_src", "Label"]].values:
        source = os.path.join(path, source)
        dest = os.path.join(path, str(label))

        try:
            shutil.move(source, dest)
        except Exception as e:
            print(e)
            continue
