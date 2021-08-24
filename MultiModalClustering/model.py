from sklearn.cluster import KMeans
from transformers import BertModel
import timm
import torch
import pickle

class Clusterer:
    """
    K-Means Clusterer for Multi-Modal Data
    Args:
        k:(int) # of Centroids
            default: 2

        model_path:(str) Path to the pickled scikit-lean's KMeans Algorithm
            default: .\kmean.pkl

        train:(bool) train or test
            default: True 
    """

    def __init__(self,k=2, model_path = 'kmean.pkl', train = True):
        
        self.train = train
        self.model_path = model_path
        
        # Text Representation Model
        self.bert = BertModel.from_pretrained('bert-base-uncased')

        # Image Representation Model
        self.vit = timm.create_model("vit_base_patch32_224_in21k", pretrained=True,num_classes = 0)
        
        if train:
            # Create New Kmean clusterer with k centroids to train
            self.kmean = KMeans(n_clusters = k)
            
        else:
            # Load Trained kmean algorithm for testing
            self.kmean = pickle.load(open(model_path, 'rb'))
    

    @torch.no_grad()
    def forward(self,loader):

        texts = []
        images = []

        # Iterate through each instance
        for batch in loader:
            image,text = batch

            # Get [CLS] output from BERT and ViT
            text = self.bert(text).pooler_output
            image = self.vit(image)
            
            # Store representation for each instance
            texts.append(text)
            images.append(image)

        # Concatenate to pass them in one go
        texts = torch.cat(texts)
        images = torch.cat(images)

        # Fusion and changing tensor->numpy
        fused_repr = (texts+images).squeeze().numpy()
        

        if self.train:
            # Train and save the kmean classifier
            self.kmean.fit(fused_repr)
            pickle.dump(self.kmean, open(self.model_path, 'wb'))

            return self.kmean.labels_
        
        # Test results
        return self.kmean.predict(fused_repr)
        