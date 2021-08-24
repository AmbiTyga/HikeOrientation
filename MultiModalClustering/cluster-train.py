import argparse
import os
import sys
from model import Clusterer
from dataObject import MultiModalDataset
from torch.utils.data import DataLoader
def cluster_train(datapath,model_path,k,bs):
    CSV = os.path.join(datapath,'train.csv')
    model_path = os.path.join(model_path,'kmean.pkl')
    dataset = MultiModalDataset(CSV,"clustering_train")
    loader = DataLoader(dataset,batch_size=bs)
    clusterer = Clusterer(model_path = model_path,train=True)
    out = clusterer.forward(loader)
    print(out)

if __name__ == '__main__':
    my_parser = argparse.ArgumentParser(description='Train Clustering')

    my_parser.add_argument('--datapath',
                           type=str,
                           help='directory to the data')
    my_parser.add_argument('--model_path',
                           type=str,
                           help='path to the directory for output model')
    my_parser.add_argument('--k',
                           default = 2,
                           type=int,
                           help='no. of clusters')
    my_parser.add_argument('--batch_size',
                           default = 2,
                           type=int,
                           help='batch size to load into extractors')

    # Execute the parse_args() method
    args = my_parser.parse_args()
    
    cluster_train(args.datapath,args.model_path,args.k,args.batch_size)
    