import numpy as np
from tqdm import tqdm 



#This fonction gives key assumptions for a given plaintext/ciphertext and a targeted byte
#Guess byte corresponds to k
""" def compute_keys_models(plaintext, ciphertext, targeted_byte):
    key_model_first = []
    key_model_last = []
    for k in range(256):
        for q in range(len(plaintext)):
            #only first_round ?
            key_model_first[k][q]=model_first_round(plaintext[q], targeted_byte, k)
            key_model_last[k][q]=model_last_round(ciphertext[q], targeted_byte, k)
    return key_model_first, key_model_last """


#This function gives the value and indexes for the highest pearson coefficient for a given traces and models
def get_highest_pearson_coeff(traces, model_first): #, model_last):
    coeffs_first = np.zeros((traces.shape[0], 256))

    for k in tqdm(range(256)): #for each key assumption associated to the targeted_byte
        for i in range(traces.shape[0]): #for each sample of traces
            coeffs_first[i,k]= abs(np.corrcoef(traces[i,:], model_first[k])[0,1])
            # coeffs_last[k][i]= abs(np.corrcoef(traces[i], model_last[k]))
    max_f = np.max(coeffs_first)
    # max_l = np.max(coeffs_last)
    indexes_f = np.where(coeffs_first == max_f)
    # indexes_l = np.where(coeffs_last == max_l)
    return coeffs_first, max_f, indexes_f #, max_l, indexes_l
