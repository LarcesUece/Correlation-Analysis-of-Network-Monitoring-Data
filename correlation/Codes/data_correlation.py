import pandas as pd
import numpy as np
import scipy.stats
import os

def extract_data (files):
    hours = []
    dates = []

    for file in files:
        parts = file.split()
        date = parts[4]
        hour = parts[5]
        hours.append(hour)
        dates.append(date)

    return dates, hours

def pearson (matrix):
    return np.corrcoef(matrix)

def spearman (matrix):
    corr_matrix, p_matrix = scipy.stats.spearmanr(matrix, axis=1)
    return corr_matrix

def kendall (df):
    return df.corr(method='kendall')

if __name__ == "__main__":
    user_path = os.getcwd()
    directory = f'{user_path}/datasets'
    files = os.listdir(directory)

    dates, hours = extract_data(files)

    for hour, date, file in zip(hours, dates, files):
        df = pd.read_csv(f'datasets/{file}')
        df.set_index('0', inplace=True)
        matrix = df.to_numpy()

        directory = 'correlation matrices'

        if not os.path.exists(directory):
            os.makedirs(directory)

        corr_matrix = pearson(matrix.T)
        np.savetxt(f'{directory}/corr matrix {hour} {date} with pearson.csv', corr_matrix, delimiter=',')

        corr_matrix = spearman(matrix.T)
        np.savetxt(f'{directory}/corr matrix {hour} {date} with spearman.csv', corr_matrix, delimiter=',')

        corr_matrix = kendall(df)
        np.savetxt(f'{directory}/corr matrix {hour} {date} with kendall.csv', corr_matrix, delimiter=',')

    print('Correlation matrices created.')