# ##############################################################################
# Author: Damien Marion
# ##############################################################################

import argparse
import numpy as np
import matplotlib.pyplot as plt

# Software : Fréquence 32Mhz
# Hardware : Fréquence 5Ghz

def main ():
    choice = 0
    data_type = ""

    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', help="hardware or software", required=True)
    parser.add_argument('--key', help="known or unknown", required=True)

    args = parser.parse_args()

    data_type = "F:\Documents\Cours\m2_cyber\m2_vet\data\\" + args.mode + "_traces_k_" + args.key + "\\traces.npy"

    mean_data = compute_mean(data_type)
    std_data = compute_standard_deviation(data_type)
    display(mean_data, std_data)
    
    return


def compute_mean(path):

    data = np.load(path)
    data_array = np.array(data)
    mean_data = np.mean(data_array, axis=1)

    return mean_data


def compute_standard_deviation(path):

    data = np.load(path)
    data_array = np.array(data)
    std_data = np.std(data_array, axis=1)

    return std_data


def display (mean, std):    

    fig, (axs1, axs2) = plt.subplots(2)
    # Share x pour lier les zoom sur l'abcisse 
    fig.suptitle('Traces representation')

    axs1.plot(mean)
    axs1.legend(['mean'])
    axs1.set_ylabel('Consumption')
    axs1.set_xlabel('Time')

    axs2.plot(std)
    axs2.legend(['standard deviation'])
    axs2.set_ylabel('Consumption')
    axs2.set_xlabel('Time')
    
    plt.show()

    return 1

if __name__ == "__main__":
    # execute only if run as a script
    main()    
