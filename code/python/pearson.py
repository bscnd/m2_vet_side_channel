import numpy as np

#This function gives the value and indexes for the highest pearson coefficient for a given traces and models
def get_highest_pearson_coeff(traces, model_first): #, model_last):

    ## using the formula :
    # https://wikimedia.org/api/rest_v1/media/math/render/svg/435a23c499a2450f0752112e69a9b808336a7cce
    D, Q = traces.shape ## get the dimensions

    model_first = np.array (model_first, dtype = np.float) # convert in 2D-array

    sxy   = np.dot (traces, model_first.T) # sum of traces multiplyed by the models
    sxx   = (traces**2).sum (1).reshape (D, 1) # sum of the square of the traces
    sx    = traces.sum (1).reshape (D, 1) # sum of the traces
    syy   = (model_first**2).sum (1).reshape (1, 256) # sum of the square of the models
    sy    = model_first.sum (1).reshape (1, 256) # sum of the models

    # compute pearson coeff
    coeffs_first = abs((Q*sxy - np.dot (sx, sy))/np.dot (np.sqrt (Q*sxx - (sx**2)), np.sqrt (Q*syy - (sy**2))))

    max_f = np.max(coeffs_first)
    # max_l = np.max(coeffs_last)
    indexes_f = np.unravel_index (coeffs_first.argmax(), coeffs_first.shape)
    # indexes_l = np.where(coeffs_last == max_l)
    return coeffs_first, max_f, indexes_f #, max_l, indexes_l
