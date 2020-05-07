import numpy as np
import os
import datetime
from tqdm import tqdm
import sys

no = 0
state_np_array = []
action_np_array = []
savepath = r'./all_game/' 
filename = 'all_game' 
for f in tqdm(os.listdir("save_data")):
    if '.gamedata' in f:
        no += 1
        print (f)
        f = os.path.join("save_data", f)
        gamedata = np.load(f)
        states = gamedata['arr_0']
        actions  = gamedata['arr_1']
        b = 0
        for state,action in zip(states,actions):
            b += 1
            state_np_array.append(state.reshape(20, 20, 1) )
            a = np.zeros(44)
            a[action] = 1
            action_np_array.append(a)
        print ('total line %d ' %b)
if len(state_np_array) == 0:
    print('NO save game data')
    sys.exit()
print ('Saved game data with total %d of savefiles' %no)
x = np.array(state_np_array)
y = np.array(action_np_array)
np.savez(savepath + filename, x, y)

