import pandas as pd
import numpy as np
import scipy.stats

def pearson (matrix):
    return np.corrcoef(matrix)

def spearman (matrix):
    corr_matrix, p_matrix = scipy.stats.spearmanr(matrix, axis=1)
    return corr_matrix

def kendall (df):
    # precisa ser feito com a matriz transposta
    return df.corr(method='kendall')

if __name__ == "__main__":
    hours = ['12', '13', '14', '15', '16', '17', '18', '19', '20', '21']
    # hours = ['33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '43']

    for hour in hours:
        dfr = pd.read_csv(f'matriz de vetores do 29-5-2023 0-{hour} sem colunas com zeros.csv')
        dfr.set_index('0', inplace=True) # label do dataset
        rmatrix = dfr.to_numpy()

        corr_Tmatrix_reduced = pearson(rmatrix.T)
        np.savetxt(f'corr 00-{hour} 29-05-2023.csv', corr_Tmatrix_reduced, delimiter=',')