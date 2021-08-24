# HikeOrientation

The assignment is to build automated scrapping tool and perform clustering on multi-modality that is on text and image, extracted using scrapping tool.

## Data Scraping 

In this assignment we have to extract images and text from following websites:

- [Myntra-Clothing/Dresses](https://www.myntra.com/dresses?f=Gender%3Amen%20women%2Cwomen)
- [allrecipes-Vegetarian Main Dishes](https://www.allrecipes.com/recipes/265/everyday-cooking/vegetarian/main-dishes/)

### Experiment
In the [config.txt](DatasetScraper/config.txt), change value under `--total_size` to extract the specific number of datapoints. By default it is 10

Run following commands:

```
python3 DatasetScraper/main.py scrape \\
	--url <myntra/allRecipes>
	--filepath <path>
	@config.txt
```

After Scraping CLI will ask for Train set's size, and divide the dataset to `clustering_train` and `clustering_test` directory. Each directory will contain scraped images and a CSV file for textual data.

## Clustering

In this assignment apply the K-Means algorithm, over the fused representation of texts and images. 
We used BERT-base and ViT for creating representation of text and image respectively.

### Experiment
In the [config.txt](MultiModalClustering/config.txt), change value under `--k` to specify number of centroids for K-Mean algorithm. By default it is 2.

Run following commands:

```
## For Training
python3 MultiModalClustering/main.py cluster-train \\
	--datapath <path>/clustering_train
	--modelpath <path to save kmean algorithm>
	--batch_size <number of datapoints to process at each iteration>
	@config.txt
	
## For Testing
python3 MultiModalClustering/main.py cluster-test \\
	--datapath <path>/clustering_test
	--modelpath <path to pickled kmean algorithm>
	--batch_size <number of datapoints to process at each iteration>
	@config.txt
```

After training or testing the images in clustering_train and clustering_test will be moved to clustered directory respectively with CSV file containing cluster class to which particular instance belongs to.

## Packages:
Packages used:

- [torch](https://pytorch.org/) == 1.8.0+cu111
- [torchvision](https://pytorch.org/vision/stable/index.html) == 0.9.0+cu111
- [timm](https://rwightman.github.io/pytorch-image-models/) == 0.4.5
- [transformers](https://huggingface.co/transformers/) == 4.4.2
- [scikit-lean](https://scikit-learn.org/) == 0.24.1
- [numpy](https://numpy.org/) == 1.20.1
- [pandas](https://pandas.pydata.org/) == 1.2.4
- [selenium](https://selenium-python.readthedocs.io/) == 3.141.0
