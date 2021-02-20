import os
import numpy as np
import matplotlib.pyplot as plt

from pearson import get_highest_pearson_coeff
from aes import AES, leakage_model_first_round_allkeys, leakage_model_last_round_allkeys

# Software data path
#SOFTWARE_PLAINTEXT_PATH = "F:\Documents\Cours\m2_cyber\m2_vet\data\software_traces_k_unknown\\plaintext.npy"
#SOFTWARE_CIPHERTEXT_PATH = "F:\Documents\Cours\m2_cyber\m2_vet\data\software_traces_k_unknown\\ciphertext.npy"
#SOFTWARE_TRACES_PATH = "F:\Documents\Cours\m2_cyber\m2_vet\data\software_traces_k_unknown\\traces.npy"
SOFTWARE_PLAINTEXT_PATH = "/home/scorpio/Documents/SCA/topic_M2/data/software_traces_k_unknown/plaintext.npy"
SOFTWARE_CIPHERTEXT_PATH = "/home/scorpio/Documents/SCA/topic_M2/data/software_traces_k_unknown/ciphertext.npy"
SOFTWARE_TRACES_PATH = "/home/scorpio/Documents/SCA/topic_M2/data/software_traces_k_unknown/traces.npy"

# Hardware data path
#HARDWARE_PLAINTEXT_PATH = "F:\Documents\Cours\m2_cyber\m2_vet\data\hardware_traces_k_known\\plaintext.npy"
#HARDWARE_CIPHERTEXT_PATH = "F:\Documents\Cours\m2_cyber\m2_vet\data\hardware_traces_k_known\\ciphertext.npy"
#HARDWARE_TRACES_PATH = "F:\Documents\Cours\m2_cyber\m2_vet\data\hardware_traces_k_known\\traces.npy"
#HARDWARE_KEY_PATH = "F:\Documents\Cours\m2_cyber\m2_vet\data\hardware_traces_k_known\\key.npy"
HARDWARE_PLAINTEXT_PATH = "/home/scorpio/Documents/SCA/topic_M2/data/hardware_traces_k_known/plaintext.npy"
HARDWARE_CIPHERTEXT_PATH = "/home/scorpio/Documents/SCA/topic_M2/data/hardware_traces_k_known/ciphertext.npy"
HARDWARE_TRACES_PATH = "/home/scorpio/Documents/SCA/topic_M2/data/hardware_traces_k_known/traces.npy"
HARDWARE_KEY_PATH = "/home/scorpio/Documents/SCA/topic_M2/data/hardware_traces_k_known/key.npy"

def main():

    #compute_software_key(SOFTWARE_PLAINTEXT_PATH, SOFTWARE_CIPHERTEXT_PATH, SOFTWARE_TRACES_PATH)
    compute_hardware_key(HARDWARE_PLAINTEXT_PATH, HARDWARE_CIPHERTEXT_PATH, HARDWARE_TRACES_PATH, HARDWARE_KEY_PATH)


def compute_software_key(plaintext_path, ciphertext_path, traces_path):

    #Load data and reduce traces size to focus on the 2000 first cycles and only the 400 first values
    plaintext = np.load(plaintext_path)
    ciphertext = np.load(ciphertext_path)
    traces = np.load(traces_path)
    traces = traces [:2000:, :400]
    plaintext = plaintext [:, :400]

    computed_key = np.zeros(16, dtype=np.uint8)
    #computed_key = compute_model(1, plaintext, traces)

    #Master key (saved for k_unknown)
    computed_key = [123, 86, 39, 250, 142, 4, 139, 87, 144, 205, 225, 221, 217, 24, 29, 31]
    
    #Test
    check_decrypt_cipher(computed_key, ciphertext, plaintext)


def compute_hardware_key(plaintext_path, ciphertext_path, traces_path, key_path):

    plaintext = np.load(plaintext_path)
    ciphertext = np.load(ciphertext_path)
    traces = np.load(traces_path)
    # traces = traces[:2000, :]

    #Secret key to be found
    known_key = np.zeros(16, dtype=np.uint8)
    known_key = [161, 84, 134, 175, 124, 114, 233, 147, 179, 238, 20, 17, 99, 111, 188, 42]

    k10 = np.zeros(16, dtype=np.uint8)
    #k10 = compute_model(0, ciphertext, traces)
    
    #K10 (save for k_known)
    k10 = [151, 225, 230, 156, 11, 93, 34, 92, 88, 125, 245, 7, 176, 173, 134, 185]

    # Instanciate an AES object to invert the last round key (won't be using the master key).
    random_key = os.urandom(16)
    aes_tool = AES(random_key)

    # Compute all round keys and the master key from k10
    computed_key = aes_tool.inverse_expand_key(k10)[9]

    check_decrypt_cipher(computed_key, ciphertext, plaintext)

#This function compute the leakage model depending on model (0:firt_round->software, 1:last_round->hardware)
#By doing this, we can build up the key array which gives the master key (or k10 if model=1)
def compute_model(model, text, traces):
    fig, axs= plt.subplots(1)
    key = np.zeros(16, dtype=np.uint8)
    for i in range(16):
        #firt_round or last_round ?
        if(model):
            s_model = leakage_model_first_round_allkeys(text, i) #text=plaintext
            
        else:
            s_model = leakage_model_last_round_allkeys(text, i) #text=ciphertext

        #Compute the correlation values with pearson and gives the key[i]
        correlation_values, max_f, indexes_f = get_highest_pearson_coeff(traces, s_model)

        key[i] = np.uint8(indexes_f[1])

        # Display highest correlation value
        axs.plot(correlation_values[indexes_f[0]])

    # Display all the highest correlation values
    #plt.show()

    return key

#The following two functions check decrypting/encrypting with the previously computed_key (a.k.a master key)
def check_decrypt_cipher(master_k, ciphertext, plaintext):
    aes_tool = AES(bytes(master_k))
    assert np.all(bytes (plaintext [:, 0]) == aes_tool.decrypt_block(bytes(ciphertext [:, 0])))

def check_encrypt_plain(masker_k, plaintext, ciphertext):
    aes_tool = AES(bytes(master_k))
    assert np.all(bytes (ciphertext [:, 0]) == aes_tool.encrypt_block(bytes(plaintext [:, 0])))

if __name__ == "__main__":
    main()
