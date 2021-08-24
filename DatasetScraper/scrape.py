import argparse
from Scrapers import *
import os


def scrape(args):
    """
    Scrape Images and textual data from Myntra and AllRecipes
    Arguments:
        --url: Website Name to scrape from
                Options: myntra, allRecipes

        --filepath: Path to save scraped data
                default: Current Working Directory

        --total_size: Total data points to be extracted
                default: 10
    """
    if args.url == "myntra":
        obj = Myntra(args.filepath)
    else:
        obj = AllRecipes(args.filepath)

    if obj.total_extracted < args.total_size:
        obj.get_data(args.total_size)
    obj.browser.close()

    N = int(input("\nTrain Set Size: "))
    obj.divide(N)


my_parser = argparse.ArgumentParser(fromfile_prefix_chars="@")
subparser = my_parser.add_subparsers()

scraper = subparser.add_parser("scrape")

scraper.add_argument(
    "--url", type=str, help="URL of the page", choices=["myntra", "allRecipes"]
)

scraper.add_argument(
    "--total_size", default=10, type=int, help="total no. of datapoints to be scraped"
)

scraper.add_argument(
    "--filepath",
    default=os.getcwd(),
    type=str,
    help="Specify path to save scraped files",
)

scraper.set_defaults(func=scrape)

if __name__ == "__main__":

    # Execute the parse_args() method
    args = my_parser.parse_args()

    args.func(args)
