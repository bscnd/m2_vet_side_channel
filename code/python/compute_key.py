import os
import numpy as np
import matplotlib.pyplot as plt

from pearson import get_highest_pearson_coeff
from aes import AES, leakage_model_first_round_allkeys, leakage_model_last_round_allkeys

# Software data path
SOFTWARE_PLAINTEXT_PATH = "F:\Documents\Cours\m2_cyber\m2_vet\data\software_traces_k_unknown\\plaintext.npy"
SOFTWARE_CIPHERTEXT_PATH = "F:\Documents\Cours\m2_cyber\m2_vet\data\software_traces_k_unknown\\ciphertext.npy"
SOFTWARE_TRACES_PATH = "F:\Documents\Cours\m2_cyber\m2_vet\data\software_traces_k_unknown\\traces.npy"

# Hardware data path
HARDWARE_PLAINTEXT_PATH = "F:\Documents\Cours\m2_cyber\m2_vet\data\hardware_traces_k_known\\plaintext.npy"
HARDWARE_CIPHERTEXT_PATH = "F:\Documents\Cours\m2_cyber\m2_vet\data\hardware_traces_k_known\\ciphertext.npy"
HARDWARE_TRACES_PATH = "F:\Documents\Cours\m2_cyber\m2_vet\data\hardware_traces_k_known\\traces.npy"
HARDWARE_KEY_PATH = "F:\Documents\Cours\m2_cyber\m2_vet\data\hardware_traces_k_known\\key.npy"

def main():

    # compute_software_key(SOFTWARE_PLAINTEXT_PATH, SOFTWARE_CIPHERTEXT_PATH, SOFTWARE_TRACES_PATH)
    compute_hardware_key(HARDWARE_PLAINTEXT_PATH, HARDWARE_CIPHERTEXT_PATH, HARDWARE_TRACES_PATH, HARDWARE_KEY_PATH)


def compute_software_key(plaintext_path, ciphertext_path, traces_path):

    #Load data and reduce traces size to focus on the 2000 first cycles
    plaintext = np.load(plaintext_path)
    ciphertext = np.load(ciphertext_path)
    traces = np.load(traces_path)
    traces = traces[:2000, :]

    computed_key = np.zeros(16, dtype=np.uint8)
    fig, axs= plt.subplots(1)
    
    # for i in range(16):

    #     model_first_round = leakage_model_first_round_allkeys(plaintext, i)
    #     correlation_values, max_f, indexes_f = get_highest_pearson_coeff(traces, model_first_round)
    
    #     computed_key[i] = np.uint8(indexes_f[1])

    #     # Display highest correlation value
    #     axs.plot(correlation_values[indexes_f[0]])

    # Display all the highest correlation values
    # plt.show()

    computed_key = [123, 86, 39, 250, 142, 4, 139, 87, 144, 205, 225, 221, 217, 24, 29, 31]
    
    check_decrypt_cipher(computed_key, ciphertext, plaintext)


def compute_hardware_key(plaintext_path, ciphertext_path, traces_path, key_path):

    plaintext = np.load(plaintext_path)
    ciphertext = np.load(ciphertext_path)
    traces = np.load(traces_path)
    # traces = traces[:2000, :]
    known_key = bytes([161, 84, 134, 175, 124, 114, 233, 147, 179, 238, 20, 17, 99, 111, 188, 42])

    k10 = np.zeros(16, dtype=np.uint8)
    fig, axs= plt.subplots(1)

    # for i in range(16):
    #     model_last_round = leakage_model_last_round_allkeys(ciphertext, i)
    #     correlation_values, max_f, indexes_f = get_highest_pearson_coeff(traces, model_last_round)
    #     k10[i] = np.uint8(indexes_f[1])
    
    k10 = [151, 225, 230, 156, 11, 93, 34, 92, 88, 125, 245, 7, 176, 173, 134, 185]

    # Instanciate an AES object to invert the last round key (won't be using the master key).
    random_key = os.urandom(16)
    aes_tool = AES(random_key)

    # Compute all round keys and the master key from k10
    computed_key = aes_tool.inverse_expand_key(k10)[9]

    check_decrypt_cipher(computed_key, ciphertext, plaintext)

#The following two functions check decrypting/encrypting with the previously computed_key (a.k.a master key)
def check_decrypt_cipher(master_k, ciphertext, plaintext):
    aes_tool = AES(bytes(master_k))
    assert np.all(bytes (plaintext [:, 0]) == aes_tool.decrypt_block(bytes(ciphertext [:, 0])))

def check_encrypt_plain(masker_k, plaintext, ciphertext):
    aes_tool = AES(bytes(master_k))
    assert np.all(bytes (ciphertext [:, 0]) == aes_tool.encrypt_block(bytes(plaintext [:, 0])))

if __name__ == "__main__":
    main()
