import torch
from torch.utils.data import Dataset, DataLoader
from PIL import Image
import numpy as np
import albumentations as A
from albumentations.pytorch import ToTensorV2

class MNISTDataset(Dataset):
    def __init__(self, image_path, labels, transform=None):
        self.image_path = image_path
        self.label_path = labels
        self.transform = transform

    def __len__(self):
        return len(self.image_path)
    
    def __getitem__(self, idx):
        image = Image.open(self.image_path[idx])
        label = self.label_path[idx]
        label = torch.tensor(label)
        image_np = np.array(image)

        if self.transform:
            augmented = self.transform(image=image_np)
            image = augmented['image']

        return image, label

def transforms(is_training=False):
    if is_training:
        return A.Compose([
            A.ShiftScaleRotate(shift_limit=0.06, scale_limit=0.1, rotate_limit=15, p=0.6),
            A.Normalize(mean=(0.1307,), std=(0.3081,)), # Use MNIST's specific mean and std
            ToTensorV2(),
        ])
    else:
        return A.Compose([
            A.Normalize(),
            ToTensorV2(),
        ])
        

