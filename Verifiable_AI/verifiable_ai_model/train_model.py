import matplotlib.pyplot as plt

from torchvision.datasets.mnist import MNIST
from torchvision.transforms import ToTensor
from torch.utils.data.dataloader import DataLoader
import torch
import torch.nn as nn

from torch.optim.adam import Adam

training_data = MNIST(root="./", train=True, download=True, transform=ToTensor())
test_data = MNIST(root="./", train=False, download=True, transform=ToTensor())

print(len(training_data))
print(len(test_data))


train_loader = DataLoader(training_data, batch_size=32, shuffle=True)
test_loader = DataLoader(test_data, batch_size=32, shuffle=False)


device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"device: {device}")

model = nn.Sequential(
    nn.Linear(784, 64), nn.ReLU(), nn.Linear(64, 64), nn.ReLU(), nn.Linear(64, 10)
)
model.to(device)

lr = 1e-3
optim = Adam(model.parameters(), lr=lr)

for epoch in range(20):
    for data, label in train_loader:
        optim.zero_grad()
        data = torch.reshape(data, (-1, 784)).to(device)
        preds = model(data)

        loss = nn.CrossEntropyLoss()(preds, label.to(device))
        loss.backward()
        optim.step()

    print(f"epoch{epoch + 1} loss:{loss.item()}")

torch.save(model.state_dict(), "./mock/MNIST.pth")


model.load_state_dict(torch.load("./mock/MNIST.pth", map_location=device))

num_corr = 0

with torch.no_grad():
    for data, label in test_loader:
        data = torch.reshape(data, (-1, 784)).to(device)

        output = model(data.to(device))
        preds = output.data.max(1)[1]

        corr = preds.eq(label.to(device).data).sum().item()
        num_corr += corr

print(f"Accuracy:{num_corr / len(test_data)}")