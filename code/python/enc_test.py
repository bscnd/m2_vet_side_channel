import os
import numpy as np
import matplotlib.pyplot as plt
from pearson import get_highest_pearson_coeff
from aes import AES, bytes2matrix, matrix2bytes, sbox_output, leakage_model_first_round, leakage_model_first_round_allkeys


def main():
    
    # # Expand key
    # all_keys = AES._expand_key(aes_tool, master_key)
    # print(str(all_keys) + "\n")                     # Affiche toutes les clés
    # k10 = all_keys[-1]                              # On récupère la dernière clé (k10)
    # print("k10 : " + str(k10))                      # On l'affiche
    # print("k10 passe du type 'list of bytes' à 'bytes'")
    # k10 = b''.join(k10)                             # On passe k10 en bytes
    
    # print("Master Key : " + str(master_key))
    # print("type master key" + str(type(master_key)) + "\n")

    # # Reverse expand key
    # i = 10
    # for round_key in AES.inverse_expand_key(aes_tool, k10):
    #     print ("Round " + str(i) + " : " + str(round_key) + "\n")
    #     i-=1  
    # print("First Key : " + str(round_key)) 
    # round_key=bytes2matrix(round_key)
    # print(round_key)  

    # print("Master Key : " + str(master_key))
    # master_key=bytes2matrix(master_key)
    # print(str(master_key) + "\n")


    #Load data
    plaintext = np.load("F:\Documents\Cours\m2_cyber\m2_vet\data\software_traces_k_unknown\\plaintext.npy")
    ciphertext = np.load("F:\Documents\Cours\m2_cyber\m2_vet\data\software_traces_k_unknown\\ciphertext.npy")
    traces = np.load("F:\Documents\Cours\m2_cyber\m2_vet\data\software_traces_k_unknown\\traces.npy")
    traces = traces [:2000, :]

    #known_key = np.load("F:\Documents\Cours\m2_cyber\m2_vet\data\software_traces_k_known\\key.npy")
    computed_key = np.zeros(16, dtype=np.uint8)

    fig, axs= plt.subplots(1)
    for i in range(16):

        model_first_round = leakage_model_first_round_allkeys(plaintext, i)
        correlation_values, max_f, indexes_f = get_highest_pearson_coeff(traces, model_first_round)
        
        computed_key[i] = np.uint8(indexes_f[1])

        # Display highest correlation value
        axs.plot(correlation_values[indexes_f[0]])

    # Display all the highest correlation values
    # plt.show()

    # key = [123, 86, 39, 250, 142, 4, 139, 87, 144, 205, 225, 221, 217, 24, 29, 31]
    aes = AES (bytes(computed_key))
    assert np.all(bytes (plaintext [:, 0]) == aes.decrypt_block (bytes (ciphertext [:, 0])))

    
if __name__ == "__main__":
    main()
