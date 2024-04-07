#Import Libaries
import os
import numpy as np
import pandas as pd
import torch
import torchvision
import matplotlib.pyplot as plt
from torch.utils.data import Dataset, DataLoader
from torchmetrics import Accuracy, Precision, F1Score
from pathlib import Path
from torch import optim
import torch.nn as nn
import torch.utils.data as data
from torchvision import transforms, models, datasets
import torchvision.models.efficientnet as e
import torchvision.models.resnet as r
from torch.cuda.amp import autocast, GradScaler
from torch.optim.lr_scheduler import StepLR
from PIL import Image
from datetime import datetime
from assistant.controllers.constants import constants



device = 'cuda' if torch.cuda.is_available() else 'cpu'

def create_data_loaders(dataset_path,img_size,batch_size,validation_split):

    transformer = torchvision.transforms.Compose([transforms.Resize(size = img_size),transforms.ToTensor(),])
    datafolder = torchvision.datasets.ImageFolder(dataset_path, transform = transformer)

    # Random split
    train_set_size = int(len(datafolder) * (1-validation_split))
    valid_set_size = len(datafolder) - train_set_size
    train_set, valid_set = data.random_split(datafolder, [train_set_size, valid_set_size])

    train_loader = DataLoader(dataset =train_set, batch_size =batch_size, shuffle = True)
    test_loader = DataLoader(dataset= valid_set, batch_size = batch_size)

    classes = datafolder.classes
    num_classes = len(classes)

    print(f"Dataset with length {len(datafolder)} with {num_classes} classes is split into Train: {len(train_set)}  & Validation : {len(valid_set)}")

    return train_loader, test_loader, num_classes,classes, transformer

def load_model_weight(num_classes):

    #Load Weights for Training
    WEIGHTS = r.resnet50(pretrained= True)
    # WEIGHTS2 = e.efficientnet_b0(pretrained= True)

    ##Freeze Model Params for Transfer Learning
    for p in WEIGHTS.parameters():
        p.requires_grad = False

    WEIGHTS.fc = nn.Linear(2048, num_classes)

    model = WEIGHTS
    model.to(device)

    return model

def setup_metrics(model,num_classes):
    loss_fn = nn.CrossEntropyLoss().to(device)
    optimizer = optim.Adam(model.parameters(), lr= 0.01)
    accuracy_fn = Accuracy(task="multiclass", num_classes= num_classes).to(device)
    f1 = F1Score(task="multiclass", num_classes= num_classes).to(device)

    return loss_fn,optimizer,accuracy_fn,f1


# Set up parameters
def train_model(train_loader,model,num_classes,epochs):
    loss_fn,optimizer,accuracy_fn,f1 = setup_metrics(model,num_classes)

    train_losses, train_acc = 0, 0
    # scaler = GradScaler()
    for epoch in range(epochs):
        print(f"EPOCH: {epoch+1}/{epochs}")
        for batch, (X, y )in enumerate(train_loader):
            X = X.to(device)
            y = y.to(device)
            model.train()

            y_pred =model(X)
            loss = loss_fn(y_pred, y)
            train_acc += accuracy_fn(y_pred.argmax(dim=1), y)
            train_losses += loss
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            if batch % 100 == 0:
                print(f'{train_losses} | {train_acc}')

        train_losses /= len(train_loader)
        train_acc /= len(train_loader)
        print(f' Train Loss: {train_losses:.4f} | Train Acc: {train_acc:.3f}')

    return model

def eval_model(test_loader,model,num_classes):
    loss_fn,optimizer,accuracy_fn,f1 = setup_metrics(model,num_classes)
    model.eval()
    test_loss, test_acc, test_f1 = 0, 0, 0
    with torch.inference_mode():
        for Xt, yt in test_loader:
            Xt = Xt.to(device)
            yt= yt.to(device)
            test_pred = model(Xt)
            t_loss = loss_fn(test_pred, yt)
            test_loss += t_loss
            test_acc += accuracy_fn(test_pred.argmax(dim=1), yt)
            test_f1 += f1(test_pred.argmax(dim=1), yt)
        test_loss /= len(test_loader)
        test_acc /= len(test_loader)
        test_f1 /= len(test_loader)

        msg = f' Test Loss {test_loss:.4f} | Test Acc: {test_acc:.2f} | F1Score: {test_f1}  '
        print(msg)
        return msg

def predict_class(img, loaded_model,transformer,classes):
    # Convert grayscale to RGB
    print(img.mode)
    if img.mode in ['L','P']:
        img = img.convert('RGB')

    transformed_img = transformer(img)
    transformed_img = transformed_img.unsqueeze(dim=0)
    print(transformed_img.shape)
    transformed_img.to(device)
    loaded_model.to(device)
    transformed_img = transformed_img.to(device)
    print(transformed_img.device)

    # Assuming transformed_img is a 4-channel image (RGBA) and you want to use only RGB channels
    rgb_img = transformed_img[:, :3, :, :]  # Extract the first 3 channels (RGB)
    rgb_img = rgb_img.to(device)

    # Run inference on the RGB image
    with torch.inference_mode():
        output = loaded_model(rgb_img)

    outputp = torch.argmax(output).detach()
    outputp =outputp.item()
    print(outputp)
    Predicted_class = classes[outputp]
    print(f'Predicted Class is: {Predicted_class} ')
    return Predicted_class
