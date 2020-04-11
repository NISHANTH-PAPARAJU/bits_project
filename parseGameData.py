import numpy as np
import os


no = 0
for f in os.listdir("data"):
    if '.gamedata' in f:
        no += 1
        print (f)
        f = os.path.join("data", f)
        gamedata = np.load(f)
        states = gamedata['arr_0']
        score  = gamedata['arr_1']
        for state in states:
            print (state)
        print (score)
