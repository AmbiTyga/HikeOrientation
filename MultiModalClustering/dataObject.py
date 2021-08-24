from torch.utils.data import Dataset
from torchvision import transforms
from PIL import Image
import torch, os
import pandas as pd
from transformers import BertTokenizer

class MultiModalDataset(Dataset):
    def __init__(self,CSV,path):
        super(MultiModalDataset,self).__init__()

        self.transform = transforms.Compose([
                                             transforms.Resize((224,224),interpolation=transforms.InterpolationMode.BICUBIC),
                                             transforms.ToTensor()
        ])
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        self.data = pd.read_csv(CSV)[['Img_src','Description']].values
        self.path = path
    
    def __len__(self,):
        return len(self.data)
    def __getitem__(self,idx):
        img,text = self.data[idx]
        img = self.transform(Image.open(os.path.join(self.path,img)).convert('RGB'))
        text = self.tokenizer(text,truncation=True,padding='max_length', max_length=100).input_ids

        return img, torch.tensor(text)