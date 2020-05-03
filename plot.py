import numpy as np
import os
import datetime
import numpy as np
import matplotlib.pyplot as plt

for f in os.listdir("save_game"):
    if '.gamedata' in f:
        print (f)
        f = os.path.join("save_game", f)
        gamedata = np.load(f)
        states = gamedata['arr_0']

        fig, ax = plt.subplots(ncols=10)
        fig.set_figheight(15)
        fig.set_figwidth(15)
        print (ax )
        for i in range(10):
            ax[i].imshow(states[i], interpolation='none')
        plt.show()
