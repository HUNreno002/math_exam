import numpy as np

def random_not_zero_or_one(lowerlimit,higherlimit):
    while True:
        val = np.random.randint(lowerlimit,higherlimit+1)
        if val != 0 and val != 1:
            return val