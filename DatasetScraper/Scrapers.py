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
    def __init__(self,path):
        self.path = path
        self.total_extracted = len(glob(os.path.join(path,"clustering_train","*.jpg")))
        self.browser = webdriver.Chrome()
        self.browser.get("https://www.myntra.com/dresses?f=Gender%3Amen%20women%2Cwomen")
    
    def next_fetch(self,k):
        try:
            self.browser.find_element_by_class_name('pagination-next a').send_keys(Keys.RETURN)
            return deque(WebDriverWait(self.browser, 8).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "product-base")))[:k]), k
        except NoSuchElementException as e:
            return None, 0
    
    
        
    def getElements(self,selector,filepath):
    
        img_src = WebDriverWait(selector, 8).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "img.img-responsive")))

        brand = selector.find_element_by_class_name('product-brand').text
        prod_type = selector.find_element_by_class_name('product-product').text

        try:
            cost_price = selector.find_element_by_class_name('product-strike').text
            selling_price = selector.find_element_by_class_name('product-discountedPrice').text

        except NoSuchElementException as e:
            cost_price = selling_price = selector.find_element_by_class_name('product-price').text

        filename = img_src.get_attribute('title')+'.jpg'
        img_src = downloadImage(img_src.get_attribute('src'),filepath,filename)

        return img_src, brand, prod_type, cost_price, selling_price
        
    def get_data(self,k):
        k = k-self.total_extracted
        if k<=0:
            return 
        filepath = os.path.join(self.path,"clustering_train")
        if not os.path.isdir(filepath):
            os.mkdir(filepath)
            
        CSV = os.path.join(filepath,'train.csv')
        
        csv_file = open(CSV, 'w',encoding = 'utf-8')

        csv_writer = csv.writer(csv_file, delimiter=",")
        csv_writer.writerow(["Img_src", "Brand", "Description", "Cost_price", "Selling_price"])

        products = deque(WebDriverWait(self.browser, 20).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "product-base"))))        
        
        
        while k>0:
            if products:

                selector = products.popleft()
                self.browser.execute_script("arguments[0].scrollIntoView();", selector)

                img_src, brand, prod_type, cost_price, selling_price = self.getElements(selector,filepath)

                csv_writer.writerow([img_src, brand, prod_type, cost_price, selling_price])

                k-=1
                self.total_extracted+=1

            else :
                products,k = self.next_fetch(k)

        csv_file.close()
        
        
        
    def divide(self,N):
        assert N<self.total_extracted, f"N should be less than {self.total_extracted}"
        
        CSV = os.path.join(self.path,"clustering_train",'train.csv')
        data = pd.read_csv(CSV)
        
        train = data.iloc[:N,:].copy()
        test = data.iloc[N:,:].copy()
        
        path = os.path.join(self.path,"clustering_test")
        if not os.path.isdir(path):
            os.mkdir(path)
        
        def X(x):
            try:
                shutil.move(os.path.join(self.path,"clustering_train",x),path)
            except Exception as e:
                pass

        test.Img_src.apply(X)
        
        train.to_csv(CSV,index=False)
        
        testCSV = os.path.join(path,'test.csv')
        test.to_csv(testCSV,index=False)


class AllRecipes:
    def __init__(self,path):
        self.path = path
        self.total_extracted = len(glob(os.path.join(path,"clustering_train","*.jpg")))

        self.browser = webdriver.Chrome()
        self.browser.get("https://www.allrecipes.com/recipes/265/everyday-cooking/vegetarian/main-dishes/")
    
    def get_recipes(self,k):
        try:
            return deque(WebDriverWait(self.browser, 8).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, 'component.card.card__category')))[k:])
        except TimeoutError as e:
            return None
    
    def load_more(self):
        try:
            WebDriverWait(self.browser, 8).until(EC.visibility_of_element_located((By.CLASS_NAME, 'category-page-list-related-load-more-button.manual-link-behavior'))).send_keys(Keys.RETURN)
            return True
        except Exception as e:
            return False
        
    def getElements(self,selector,filepath):

        text = selector.text.split('\n')
        if len(text)>2:
            title = text[0]
            desc = text[3]
            author = text[-1].replace('By ',"")
            img_src = WebDriverWait(selector, 20).until(EC.visibility_of_element_located((By.TAG_NAME, "img")))
            
            filename = img_src.get_attribute('title')+'.jpg'
            img_src = downloadImage(img_src.get_attribute('src'),filepath,filename)
        
            return img_src, title, desc, author
        
        else:
            return None
        
    def get_data(self,k):
        filepath = os.path.join(self.path,"clustering_train")
        
        if not os.path.isdir(filepath):
            os.mkdir(filepath)
        CSV = os.path.join(filepath,'train.csv')
        
        csv_file = open(CSV, 'w',encoding = 'utf-8')

        csv_writer = csv.writer(csv_file, delimiter=",")
        csv_writer.writerow(["Img_src", "Title", "Description", "Author"])

        recipes = self.get_recipes(self.total_extracted)        
        while self.total_extracted<k:
            if recipes:
                recipe = recipes.popleft()

                self.browser.execute_script("arguments[0].scrollIntoView();", recipe)

                elements = self.getElements(recipe,filepath)

                if elements:
                    csv_writer.writerow(elements)
                    self.total_extracted+=1

            elif self.load_more():
                recipes = self.get_recipes(self.total_extracted)

            else:
                print(f"Collected {self.total_extracted} data-points")
                break  
        csv_file.close()
        
        
    def divide(self,N):
        assert N<self.total_extracted, f"N should be less than {self.total_extracted}"
        
        CSV = os.path.join(self.path,"clustering_train",'train.csv')
        data = pd.read_csv(CSV)
        
        train = data.iloc[:N,:].copy()
        test = data.iloc[N:,:].copy()
        
        path = os.path.join(self.path,"clustering_test")
        if not os.path.isdir(path):
            os.mkdir(path)
        
        def X(x):
            try:
                shutil.move(os.path.join(self.path,"clustering_train",x),path)
            except Exception as e:
                print(e)
                pass

        test.Img_src.apply(X)
        
        train.to_csv(CSV,index=False)
        
        testCSV = os.path.join(path,'test.csv')
        test.to_csv(testCSV,index=False)
        