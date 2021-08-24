from torch.utils.data import Dataset
from torchvision import transforms
from PIL import Image
import torch, os

from transformers import BertTokenizer


class MultiModalDataset(Dataset):
    """
    Dataset Pipeline to load and pre-process
    Arguments:
        CSV: Path to the CSV
        path: Path to Image data
    """

    def __init__(self, CSV, path):
        super(MultiModalDataset, self).__init__()

        # Transformer for Image preprocessing
        self.transform = transforms.Compose(
            [
                transforms.Resize(
                    (224, 224), interpolation=transforms.InterpolationMode.BICUBIC
                ),
                transforms.ToTensor(),
            ]
        )

        # Tokenizer for text
        self.tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")

        # Load specific values from the dataframe
        self.data = CSV[["Img_src", "Description"]].values

        self.path = path

    def __len__(
        self,
    ):
        return len(self.data)

    def __getitem__(self, idx):
        img, text = self.data[idx]

        img = self.transform(Image.open(os.path.join(self.path, img)).convert("RGB"))

        text = self.tokenizer(
            text, truncation=True, padding="max_length", max_length=100
        ).input_ids

        return img, torch.tensor(text)
