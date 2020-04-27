import torch
import torch.nn as nn
import numpy as np
import torch.nn.functional as F
from torch.utils.data import Dataset
from torch import optim

class dataset(Dataset):
    def __init__(self, x, y):
        self.x = x 
        self.y = y

    def __len__(self):
        return len(self.x)

    def __getitem__(self, idx):
        return self.x[idx], self.y[idx]

class Net(nn.Module):

    def __init__(self):
       super(Net, self).__init__()
       self.a = nn.Linear(16*1, 1)

    def forward(self, x):
        x = F.relu(self.a(x))
        return torch.sigmoid(x)

if __name__ == "__main__": 
    data = []
    target = []
    for i in range(1, 2**8):
        result = 0
        if i%2 == 0:
          result  = 1 
        res = [ int(i) for i in ( '{:016b}'.format(i))]
        data.append(np.array(res))
        target.append(result) 
    x = data
    y = target
    data_set = dataset(x, y)
    train_data = torch.utils.data.DataLoader(data_set, batch_size = 10, shuffle=True)
    model = Net()
    optimizer = optim.Adam(model.parameters()) 
    device = 'cpu'
    floss = nn.MSELoss()
    model.train()
    for i in range(100):
        all_loss = 0
        num_loss = 0
        for batch_idx, (data, target) in enumerate(train_data):
            target = target.unsqueeze(-1)
            data, target = data.to(device), target.to(device)
            target = target.float()
            data = data.float()
    
            optimizer.zero_grad()
            output = model(data)
    
            loss = floss(output, target)
            loss.backward()
            optimizer.step()
    
            all_loss += loss.item()
            num_loss += 1
        print ('%3d: %f' %(i, all_loss/num_loss))
    torch.save(model.state_dict(), 'model.pth')
