# ##############################################################################
# Author: Damien Marion
# ##############################################################################

import numpy as np
import matplotlib.pyplot as plt

def load_data (path):
    """
    load_trace
    Load the trace, plaintext, ciphertext or the key from the pointed file. 
    In the provided file (.npy):
       + the traces are stored as (D \times Q) array of float-32bits (np.float32). 
       + the plaintext/ciphertext  are stored as (16 \times Q) array of int-8bits (np.uint8)
       + (not always available) the key is stored as a array of of 16 int-8bits (np.uint8)  

    With D the number of samples and Q the number of traces.
    
    Args:
      - path: path of the file containing the traces. 

    Returns:
      - data: loaded data
          
    """
    data = np.load (path)

    return data


def display (data):
    """"display 
    use the 'import matplotlib.pyplot'
    (https://matplotlib.org/) librairy to display data (array)

    Args:
      - data: (\D \times \Q) array 

    Returns:
      - void: creat a window where the dataset is displayed. each traces 
      \{ data^D_q \}_{q < \Q} are displayed on the same window.
    """
    
    
    fig, axs = plt.subplots ()
    axs.plot (data)

    axs.set_ylabel ('y-axis')
    axs.set_xlabel ('x-axis')

    axs.set_xlabel ('title')
    
    plt.show ()

    return 1


    
