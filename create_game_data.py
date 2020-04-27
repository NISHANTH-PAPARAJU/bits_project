import numpy as np
import os
import datetime
from tqdm import tqdm


no = 0
state_np_array = []
action_np_array = []
savepath = r'./all_game/' 
filename = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")   + '_allgamedata'
for f in tqdm(os.listdir("save_game")):
    if '.gamedata' in f:
        no += 1
        print (f)
        f = os.path.join("data", f)
        gamedata = np.load(f)
        states = gamedata['arr_0']
        actions  = gamedata['arr_1']
        b = 0
        for action,state in tqdm(zip(states,actions)):
            b += 1
            state_np_array.append(state)
            action_np_array.append(action)
        print ('total line %d ' %b)
if len(state_np_array) == 0:
    print('NO save game data')
    return 
print ('Saved game data with total %d of savefiles' %no)
x = np.array(state_np_array)
y = np.array(action_np_array)
np.savez(savepath + filename, x, y)

