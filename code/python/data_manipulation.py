# ##############################################################################
# Author: Damien Marion
# ##############################################################################

import numpy as np
import matplotlib.pyplot as plt

# Software : Fréquence 32Mhz
# Hardware : Fréquence 5Ghz

def main ():
    choice = 0
    data_type = ""

    # Choice menu
    while (choice != 5):
        print("\n -- Sélection des données --")
        print("1 : Hardware Traces - K known")
        print("2 : Hardware Traces - K unknown")
        print("3 : Software Traces - K known")
        print("4 : Software Traces - K unknown")
        print("5 : Exit")
        choice = int(input("\nVotre choix : "))
        
        if choice == 1:
            data_type = "F:\Documents\Cours\m2_cyber\m2_vet\\vet_sca\data\hardware_traces_k_known\\traces.npy"
        elif choice == 2:
            data_type = "F:\Documents\Cours\m2_cyber\m2_vet\\vet_sca\data\hardware_traces_k_unknown\\traces.npy"
        elif choice == 3:
            data_type = "F:\Documents\Cours\m2_cyber\m2_vet\\vet_sca\data\software_traces_k_known\\traces.npy"
        elif choice == 4:
            data_type = "F:\Documents\Cours\m2_cyber\m2_vet\\vet_sca\data\software_traces_k_unknown\\traces.npy"
        else:
            print("Closing...")
            return

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
