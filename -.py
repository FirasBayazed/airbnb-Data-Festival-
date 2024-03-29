# Building on Wendy Kan's ndgc_at_k example
# https://www.kaggle.com/wendykan/airbnb-recruiting-new-user-bookings/ndcg-example
#
# you can use this script for cross-validation

import numpy as np
import pandas as pd

def dcg_at_k(r, k, method=1):
    r = np.asfarray(r)[:k]
    if r.size:
        if method == 0:
            return r[0] + np.sum(r[1:] / np.log2(np.arange(2, r.size + 1)))
        elif method == 1:
            return np.sum(r / np.log2(np.arange(2, r.size + 2)))
        elif method == 2:
            return np.sum((2**r -1)/ np.log2(np.arange(2, r.size + 2)))
        else:
            raise ValueError('method must be 0 or 1 or 2.')
    return 0.


def ndcg_at_k(r, k=5, method=1):
    dcg_max = dcg_at_k(sorted(r, reverse=True), k, method)
    if not dcg_max:
        return 0.
    return dcg_at_k(r, k, method) / dcg_max


def score_predictions(preds, truth, n_modes=5):
    """
    preds: pd.DataFrame
      one row for each observation, one column for each prediction.
      Columns are sorted from left to right descending in order of likelihood.
    truth: pd.Series
      one row for each obeservation.
    """
    assert(len(preds)==len(truth))
    r = pd.DataFrame(0, index=preds.index, columns=preds.columns, dtype=np.float64)
    for col in preds.columns:
        r[col] = (preds[col] == truth) * 1.0

    score = pd.Series(r.apply(ndcg_at_k, axis=1, reduce=True), name='score')
    return score, score.mean
    
    
preds = pd.DataFrame([['US','FR'],['FR','US'],['FR','EN'],['FR','US']])  
truth = pd.Series(['US','US','FR','EN'])
print('\n\n scores: \n', score_predictions(preds, truth))
# print('predictions: \n', preds)
# print('\n\n truth: \n', truth)
