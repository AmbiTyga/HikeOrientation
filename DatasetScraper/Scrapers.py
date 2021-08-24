import time, csv, os, shutil
from collections import deque
import pandas as pd
from glob import glob

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

from getImage import downloadImage


class Myntra:
    """
    Scrape Images from myntra.com/dresses?f=Gender%3Amen%20women%2Cwomen
    Arguments:
        path: Directory to store images into clustering_train and clustering_test
    """

    def __init__(self, path):

        self.path = path

        # Check number of images already extracted
        self.total_extracted = len(
            glob(os.path.join(path, "clustering_train", "*.jpg"))
        )

        # Start Chrome and go to the page
        self.browser = webdriver.Chrome()
        self.browser.get(
            "https://www.myntra.com/dresses?f=Gender%3Amen%20women%2Cwomen"
        )

    def next_fetch(self, k):
        """
        Goes to next page and fetches k elements
        """
        try:
            self.browser.find_element_by_class_name("pagination-next a").send_keys(
                Keys.RETURN
            )
            return (
                deque(
                    WebDriverWait(self.browser, 8).until(
                        EC.visibility_of_all_elements_located(
                            (By.CLASS_NAME, "product-base")
                        )
                    )[:k]
                ),
                k,
            )
        except NoSuchElementException as e:
            return None, 0

    def getElements(self, selector, filepath):
        """
        Extracts image and text from each element
        """
        # Get image source/link
        img_src = WebDriverWait(selector, 8).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "img.img-responsive"))
        )

        # Get brand
        brand = selector.find_element_by_class_name("product-brand").text

        # Get product type/description
        prod_type = selector.find_element_by_class_name("product-product").text

        try:
            # Get actual and discounted price
            cost_price = selector.find_element_by_class_name("product-strike").text
            selling_price = selector.find_element_by_class_name(
                "product-discountedPrice"
            ).text

        except NoSuchElementException as e:
            # if not discounted then actual price
            cost_price = selling_price = selector.find_element_by_class_name(
                "product-price"
            ).text

        # Image name and download image
        filename = img_src.get_attribute("title") + ".jpg"
        img_src = downloadImage(img_src.get_attribute("src"), filepath, filename)

        return img_src, brand, prod_type, cost_price, selling_price

    def get_data(self, k):
        """
        Scrape k elements throughout the website
        Arguments:
            k:(int) # of elements to scrape
        """

        # Checks # of already available elements
        k = k - self.total_extracted

        # lower or same then stop
        if k <= 0:
            return

        # Save all scrape to clustering_train
        filepath = os.path.join(self.path, "clustering_train")
        if not os.path.isdir(filepath):
            os.mkdir(filepath)

        # Output textual element to a Comman Separated file
        CSV = os.path.join(filepath, "train.csv")

        csv_file = open(CSV, "w", encoding="utf-8")

        csv_writer = csv.writer(csv_file, delimiter=",")
        csv_writer.writerow(
            ["Img_src", "Brand", "Description", "Cost_price", "Selling_price"]
        )

        # Get first set of elements to kick-off
        products = deque(
            WebDriverWait(self.browser, 20).until(
                EC.visibility_of_all_elements_located((By.CLASS_NAME, "product-base"))
            )
        )

        # Loop until total number of elements scraped
        while k > 0:

            # Product not emnpty
            if products:

                selector = products.popleft()
                self.browser.execute_script("arguments[0].scrollIntoView();", selector)

                img_src, brand, prod_type, cost_price, selling_price = self.getElements(
                    selector, filepath
                )

                csv_writer.writerow(
                    [img_src, brand, prod_type, cost_price, selling_price]
                )

                k -= 1
                self.total_extracted += 1

            # Collect another batch by going to next page
            else:
                products, k = self.next_fetch(k)

        # Save and Close CSV
        csv_file.close()

    def divide(self, N):
        """
        Divide dataset to train set of size N and test set of (total_extracted - N)
        """

        assert N < self.total_extracted, f"N should be less than {self.total_extracted}"

        CSV = os.path.join(self.path, "clustering_train", "train.csv")
        data = pd.read_csv(CSV)

        train = data.iloc[:N, :].copy()
        test = data.iloc[N:, :].copy()

        # Create directory for test set
        path = os.path.join(self.path, "clustering_test")
        if not os.path.isdir(path):
            os.mkdir(path)

        # local function to check and move from clustering_train->clustering_test
        def X(x):
            try:
                shutil.move(os.path.join(self.path, "clustering_train", x), path)
            except Exception as e:
                pass

        test.Img_src.apply(X)

        # Change the train.csv
        train.to_csv(CSV, index=False)

        # Save test.csv
        testCSV = os.path.join(path, "test.csv")
        test.to_csv(testCSV, index=False)


class AllRecipes:
    """
    Scrape Images from allrecipes.com/recipes/265/everyday-cooking/vegetarian/main-dishes/
    Arguments:
        path: Directory to store images into clustering_train and clustering_test
    """

    def __init__(self, path):
        self.path = path

        # Check number of images already extracted
        self.total_extracted = len(
            glob(os.path.join(path, "clustering_train", "*.jpg"))
        )

        # Start Chrome and go to the page
        self.browser = webdriver.Chrome()
        self.browser.get(
            "https://www.allrecipes.com/recipes/265/everyday-cooking/vegetarian/main-dishes/"
        )

    def get_recipes(self, k):
        """
        Get Next batch of k elements
        """
        try:
            return deque(
                WebDriverWait(self.browser, 8).until(
                    EC.visibility_of_all_elements_located(
                        (By.CLASS_NAME, "component.card.card__category")
                    )
                )[k:]
            )
        except TimeoutError as e:
            return None

    def load_more(self):
        """
        Finds and taps on load more button
        """
        try:
            WebDriverWait(self.browser, 8).until(
                EC.visibility_of_element_located(
                    (
                        By.CLASS_NAME,
                        "category-page-list-related-load-more-button.manual-link-behavior",
                    )
                )
            ).send_keys(Keys.RETURN)
            return True
        except Exception as e:
            return False

    def getElements(self, selector, filepath):
        """
        Extracts image and text from each element
        """

        # Get text data based on indexing
        text = selector.text.split("\n")

        if len(text) > 2:
            # Get title
            title = text[0]

            # Get Description
            desc = text[3]

            # Get the author
            author = text[-1].replace("By ", "")

            # Get image source/link
            img_src = WebDriverWait(selector, 20).until(
                EC.visibility_of_element_located((By.TAG_NAME, "img"))
            )

            # Get Image name and download it
            filename = img_src.get_attribute("title") + ".jpg"
            img_src = downloadImage(img_src.get_attribute("src"), filepath, filename)

            return img_src, title, desc, author

        else:
            return None

    def get_data(self, k):
        """
        Scrape k elements
        Argument:
            k:(int) # of elements to scrape
        """

        filepath = os.path.join(self.path, "clustering_train")

        if not os.path.isdir(filepath):
            os.mkdir(filepath)

        CSV = os.path.join(filepath, "train.csv")

        # Save textual data to a Comma Separated File
        csv_file = open(CSV, "w", encoding="utf-8")

        csv_writer = csv.writer(csv_file, delimiter=",")
        csv_writer.writerow(["Img_src", "Title", "Description", "Author"])

        # Get first batch of elements to kick-off
        recipes = self.get_recipes(self.total_extracted)

        # Loop until k elements are scraped
        while self.total_extracted < k:

            # Recipes contain elements
            if recipes:
                recipe = recipes.popleft()

                self.browser.execute_script("arguments[0].scrollIntoView();", recipe)

                elements = self.getElements(recipe, filepath)

                if elements:
                    csv_writer.writerow(elements)
                    self.total_extracted += 1

            # Load more recipes
            elif self.load_more():
                recipes = self.get_recipes(self.total_extracted)

            else:
                print(f"Collected {self.total_extracted} data-points")
                break
        # Save and close CSV
        csv_file.close()


def divide(self, N):
    """
    Divide dataset to train set of size N and test set of (total_extracted - N)
    """

    assert N < self.total_extracted, f"N should be less than {self.total_extracted}"

    CSV = os.path.join(self.path, "clustering_train", "train.csv")
    data = pd.read_csv(CSV)

    train = data.iloc[:N, :].copy()
    test = data.iloc[N:, :].copy()

    # Create directory for test set
    path = os.path.join(self.path, "clustering_test")
    if not os.path.isdir(path):
        os.mkdir(path)

    # local function to check and move from clustering_train->clustering_test
    def X(x):
        try:
            shutil.move(os.path.join(self.path, "clustering_train", x), path)
        except Exception as e:
            pass

    test.Img_src.apply(X)

    # Change the train.csv
    train.to_csv(CSV, index=False)

    # Save test.csv
    testCSV = os.path.join(path, "test.csv")
    test.to_csv(testCSV, index=False)
