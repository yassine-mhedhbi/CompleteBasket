import pandas as pd
import scipy.sparse as sp
import pickle

class RecommendationSystem:
    def __init__(self, pickle_path, algorithm="basic"):
        with open(pickle_path, 'rb') as f:
            self.params = pd.DataFrame.sparse.from_spmatrix(pickle.load(f))
        
        
    def __call__(self, products):
        return self.get_all(products)
    
        
    def get_all_cocart(self, pid, top=5):
    # sp_mat[pid] column product count, row product count: sp_mat.loc[pid] (index is the product id) 
    # We are doing this because we have triangular matrix
        return pd.concat((self.params[pid], self.params.loc[pid])).dropna().nlargest(top)


    def get_cocart(self, pid, top=5):
        json = {}
        for idx, val in self.get_all_cocart(pid, top=top).items():
            if val > 0:
                json[idx] =  val
        json = {pid: json}
        return json
    
    def get_all(self, idxx):
        all_responses = [self.get_cocart(idx)[idx] for idx in idxx]
        d = {}
        for resp in all_responses:
            d = {**d, **resp}
        return {str(pid): int(rec_pid) for pid, rec_pid in d.items()}
