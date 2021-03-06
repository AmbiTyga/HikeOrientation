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
    if args.model_path:
        args.model_path = os.path.join(args.model_path, "kmean.pkl")
    else:
        args.model_path = os.path.join(os.getcwd(), "kmean.pkl")
    clusterer = Clusterer(k=args.k, model_path=args.model_path, train=True)

    # Store output
    data["Label"] = clusterer.forward(loader)

    # Move and save
    data.to_csv(CSV, index=False)
    group_move(data, dataset.path)


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
    if args.model_path:
        args.model_path = os.path.join(args.model_path, "kmean.pkl")
    else:
        args.model_path = os.path.join(os.getcwd(), "kmean.pkl")

    clusterer = Clusterer(k=args.k, model_path=args.model_path, train=False)

    # Store output
    data["Label"] = clusterer.forward(loader)

    # Move and save
    data.to_csv(CSV, index=False)

    group_move(data, dataset.path)


my_parser = argparse.ArgumentParser(fromfile_prefix_chars="@")

my_parser.add_argument("command", choices=["cluster-train", "cluster-test"])

my_parser.add_argument(
    "--datapath", type=str, help="directory to the data", required=True
)

my_parser.add_argument(
    "--model_path", type=str, help="path to the directory for output model"
)

my_parser.add_argument("--k", default="@config.txt", type=int, help="no. of clusters")

my_parser.add_argument(
    "--batch_size", default=2, type=int, help="batch size to load into extractors"
)

if __name__ == "__main__":
    # Execute the parse_args() method
    args = my_parser.parse_args()
    FUNCTION = {"cluster-train": cluster_train, "cluster-test": cluster_test}

    func = FUNCTION[args.command]
    func(args)
