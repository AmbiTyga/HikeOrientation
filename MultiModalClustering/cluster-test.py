import argparse
import os
import sys
from model import Clusterer
from dataObject import MultiModalDataset
from torch.utils.data import DataLoader

def cluster_test(datapath,model_path,bs):
    CSV = os.path.join(datapath,'test.csv')
    model_path = os.path.join(model_path,'kmean.pkl')
    dataset = MultiModalDataset(CSV)
    loader = DataLoader(dataset,batch_size=bs)
    clusterer = Clusterer(dataloader=loader,model_path = model_path,train=False)
    out = clusterer.forward(loader)
    print(out)
    
if __name__ == '__main__':
    my_parser = argparse.ArgumentParser(description='Test Clustering')

    my_parser.add_argument('--datapath',
                           type=str,
                           help='directory to the data')
    my_parser.add_argument('--modelPath',
                           type=str,
                           help='path to the directory for output model')
    my_parser.add_argument('--batch_size',
                           default = -1,
                           type=int,
                           help='batch size to load into extractors')

    # Execute the parse_args() method
    args = my_parser.parse_args()
    
    cluster_test(args.datapath,args.model_path,args.batch_size)
    