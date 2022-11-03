import torch
import torch.nn as nn
import torchvision.transforms as transforms
from torchvision.models import resnet50, ResNet50_Weights
from jcopdl.callback import set_config
from PIL import Image
from torch.utils.data import DataLoader

#load model
class ModelResNet(nn.Module):
    def __init__(self, output_size):
        super().__init__()
        self.model = resnet50(weights=ResNet50_Weights.IMAGENET1K_V2)
        self.freeze()
        self.model.fc = nn.Sequential(
            nn.Linear(2048, 2),
            nn.LogSoftmax(1)
        )
        
    def forward(self, x):
        return self.model(x)
    
    def freeze(self):
        for param in self.model.parameters():
            param.requires_grad = False
            
    def unfreeze(self):
        for param in self.model.parameters():
            param.requires_grad = True

batch_size = 64
crop_size = 224

config = set_config({
    "output_size": 2,
    "batch_size": batch_size,
    "crop_size": crop_size
})

model = ModelResNet(config.output_size)

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
# PATH = "/devops-dtl-app/model/weights_best.pth"
PATH = "../model/weights_best.pth"
model.load_state_dict(torch.load(PATH, map_location='cpu'))
model = model.to(device)
model.eval()

#image -> tensor
def transform_image(image_bytes):
    transform = transforms.Compose([
        transforms.ToPILImage(),
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])

    return transform(image_bytes).unsqueeze(0)

#predict
def get_predict(image_tensor):
    testloader = DataLoader(image_tensor, batch_size = batch_size, shuffle = True)
    feature = next(iter(testloader))
    feature = feature.to(device)
    outputs = model(feature)
    predicted = outputs.argmax(1)
    return predicted