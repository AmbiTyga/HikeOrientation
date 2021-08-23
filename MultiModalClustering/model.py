from sklearn.cluster import KMeans
from transformers import BertModel
import timm
import torch
import pickle

class Clusterer:
    def __init__(self,k=2, model_path = 'kmean.pkl', train = True):
        self.train = train
        self.model_path = model_path
        self.bert = BertModel.from_pretrained('bert-base-uncased')
        self.vit = timm.create_model("vit_base_patch32_224_in21k", pretrained=True,num_classes = 0)
        
        if train:
            self.kmean = KMeans(n_clusters = k)
            
        else:
            self.kmean = pickle.load(open(model_path, 'rb'))
        
    @torch.no_grad()
    def forward(self,loader):
        texts = []
        images = []
        for batch in loader:
            text,image = batch
            text = self.bert(text.squeeze()).pooler_output
            image = self.vit(image)
            texts.append(text)
            images.append(image)
        texts = torch.stack(texts)
        imagess = torch.stack(images)
        fused_repr = texts+images
        
        if self.train:
            self.kmean.fit(fused_repr)
            pickle.dump(self.kmean, open(self.model_path, 'wb'))
            return self.kmean.labels_
        
        return self.kmeans.predict(fused_repr)
        