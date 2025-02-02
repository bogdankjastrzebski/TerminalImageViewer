import matplotlib.pyplot as plt
import torch


plt.figure()
plt.plot(range(1000), torch.randn(1000).cumsum(0))
plt.savefig('test/img/plot1.png')
        

