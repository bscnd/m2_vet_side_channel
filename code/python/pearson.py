import numpy as np


#This fonction gives key assumptions for a given plaintext/ciphertext and a targeted byte
#Guess byte corresponds to k
def compute_keys_models(plaintext, targeted_byte):
    for k in range(256):
        for q in range(len(plaintext)):
            #only first_round ?
            key_model_first[k][q]=model_first_round(plaintext[q], targeted_byte, k)
            key_model_last[k][q]=model_last_round(plaintext[q], targeted_byte, k)
    return key_model_first, key_model_last

#This function gives the highest pearson coefficient for a given traces and models
def get_highest_pearson_coeff(traces, model_first, model_last):
    for k in range(256): #for each key assumption associated to the targeted_byte
        for i in range(len(traces)): #for each sample of traces
            maxCoeffs_first[k][i]= np.max(abs(np.corrcoef(traces[i], model_first[k])))
            maxCoeffs_last[k][i]= np.max(abs(np.corrcoef(traces[i], model_last[k])))
    return maxCoeffs_first, maxCoeffs_last
