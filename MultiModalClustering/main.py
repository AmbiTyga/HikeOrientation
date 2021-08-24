import argparse
import os

from model import Clusterer
from dataObject import MultiModalDataset
from save_clustered import group_move

from torch.utils.data import DataLoader
import pandas as pd


def cluster_train(args):
    """
    Train the Kmean algorithm and cluster the train set
    """
    # Load the data
    CSV = os.path.join(args.datapath, "train.csv")
    data = pd.read_csv(CSV)

    dataset = MultiModalDataset(data, "clustering_train")
    loader = DataLoader(dataset, batch_size=args.batch_size)

    # Initialize the ML model
    args.model_path = os.path.join(args.model_path, "kmean.pkl")
    clusterer = Clusterer(k=args.k, model_path=args.model_path, train=True)

    # Store output
    data["Label"] = clusterer.forward(loader)

    # Move and save
    group_move(data, dataset.path)
    data.to_csv(CSV, index=False)


def cluster_test(args):
    """
    Test the Kmean algorithm and cluster the test set
    """
    # Load the data
    CSV = os.path.join(args.datapath, "test.csv")
    data = pd.read_csv(CSV)

    dataset = MultiModalDataset(data, "clustering_test")
    loader = DataLoader(dataset, batch_size=args.batch_size)

    # Initialize the ML model
    args.model_path = os.path.join(args.model_path, "kmean.pkl")
    clusterer = Clusterer(dataloader=loader, model_path=args.model_path, train=False)

    # Store output
    data["Label"] = clusterer.forward(loader)

    # Move and save
    group_move(data, dataset.path)
    data.to_csv(CSV, index=False)


my_parser = argparse.ArgumentParser()
subparser = my_parser.add_subparsers()

clusterTrain = subparser.add_parser("cluster-train")
clusterTest = subparser.add_parser("cluster-test")

my_parser.add_argument(
    "--datapath", type=str, help="directory to the data", required=True
)

my_parser.add_argument(
    "--model_path", type=str, help="path to the directory for output model"
)
my_parser.add_argument("--k", default=2, type=int, help="no. of clusters")
my_parser.add_argument(
    "--batch_size", default=2, type=int, help="batch size to load into extractors"
)

clusterTrain.set_defaults(func=cluster_train)
clusterTest.set_defaults(func=cluster_test)


if __name__ == "__main__":
    # Execute the parse_args() method
    args = my_parser.parse_args()

    args.func(args)
