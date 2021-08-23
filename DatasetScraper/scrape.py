import argparse
from Scrapers import *
import os
import sys
from selenium import webdriver

def scrape(website,k,filepath):
    if website=='myntra':
        obj = Myntra(filepath)
    else:
        obj = AllRecipes(filepath)
    
    if obj.total_extracted<k:
        obj.get_data(k)
    obj.browser.close()
    
    N = int(input('\nTrain Set Size: '))
    obj.divide(N)
    
if __name__ == '__main__':
    my_parser = argparse.ArgumentParser(description='Scrape dataset')

    my_parser.add_argument('--url',
                           type=str,
                           help='URL of the page')
    my_parser.add_argument('--total_size',
                           default = 10,
                           type=int,
                           help='total no. of datapoints to be scraped')
    my_parser.add_argument('--filepath',
                           default = os.getcwd(),
                           type=str,
                           help='Specify path to save scraped files')

    # Execute the parse_args() method
    args = my_parser.parse_args()
    
    scrape(args.url,args.total_size,args.filepath)
    