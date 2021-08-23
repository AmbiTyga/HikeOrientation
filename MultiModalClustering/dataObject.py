from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
from PIL import Image
import torch
import pandas as pd

class MultiModalDataset(Dataset):
    def __init__(self,CSV):
        super(MultiModalDataset,self).__init__()

        self.transform = transforms.Compose([
                                             transforms.Resize((224,224)),
                                             transforms.ToTensor()
        ])
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        self.data = pd.read_csv(CSV)[['Img_src','Description']].values
    
    def __len__(self,):
        return len(self.data)
    def __getitem__(self,idx):
        img,text = self.data[idx]
        img = self.transform(Image.open(img))
        text = self.tokenizer(text,padding='max_length', max_length=10,return_tensors='pt').input_ids

        return img,text