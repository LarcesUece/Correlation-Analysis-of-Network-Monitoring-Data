import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
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

def set_label (files):
    aux_label = []

    for file in files:
        df = pd.read_csv(f'datasets/{file}', nrows=1)
        df.set_index('0', inplace=True)
        indexes = df.columns.to_list()

        for index in indexes:
            aux_label.append(index)

    label = set(aux_label)

    return list(label)

def case1 (matrix, id):
    return np.sum(matrix[id, :])

def case2 (matrix, id):
    sum = .0
    aux_matrix = np.shape(matrix)
    columns_number = aux_matrix[1]
    for i in range(columns_number):
        if (matrix[id, i] > 0):
            sum += matrix[id, i]

    return sum

def graph_score_links (dict, hour, date, label):
    plt.figure(figsize=(12,9))

    colors = ['deepskyblue', 'green']
    xlabel = ['All values', 'Positive values']

    for i in range(0,2):
        plt.plot(label, dict[i], color=colors[i], label=xlabel[i], linewidth=3.0)

    plt.xlabel('Links', fontsize=15)
    plt.ylabel('Score values', fontsize=15)
    plt.xticks(label, fontsize=9, rotation=90)
    plt.yticks(fontsize=12)

    plt.title(f'Score for {date} {hour}', fontsize=18)
    plt.legend(loc='upper right', fontsize=12)

    directory = 'graphics score x links'
    if not os.path.exists(directory):
        os.makedirs(directory)

    plt.savefig(f'{directory}/{date} {hour} score.pdf')

def graph_score_time (dict1, dict2, hours, date, label):
    plt.figure(figsize=(12,9))

    colors = ['deepskyblue', 'green']
    xlabel = ['All values', 'Positive values']

    plt.plot(hours, dict1[label], color=colors[0], label=xlabel[0], linewidth=3.0)
    plt.plot(hours, dict2[label], color=colors[1], label=xlabel[1], linewidth=3.0)

    label = label.upper()

    plt.xlabel('Measurement Time', fontsize=15)
    plt.ylabel('Score values', fontsize=15)
    plt.xticks(hours, fontsize=12)
    plt.yticks(fontsize=12)

    plt.title(f'Score for May 29th {label}', fontsize=18)
    plt.legend(loc='upper right', fontsize=12)

    directory = 'graphics score x time'
    if not os.path.exists(directory):
        os.makedirs(directory)

    plt.savefig(f'{directory}/{date} score {label}.pdf')

if __name__ == "__main__":

    user_path = os.getcwd()
    directory = f'{user_path}/datasets'
    files = os.listdir(directory)

    label = set_label(files)
    dates, hours = extract_data(files)

    weigth = []
    for w in range(1, 200, 2):
        weigth.append(1/w)

    pcoef1 = {}
    pcoef2 = {}
    for i in range(len(label)):
        pcoef1[label[i]] = []
        pcoef2[label[i]] = []

    for i in range(len(label)):
        for j in range(len(files)):
            pcoef1[label[i]].append(-1.0)
            pcoef2[label[i]].append(-1.0)

    j = 0
    for hour, date, file in zip(hours, dates, files):
        df2 = pd.read_csv(f'datasets/{file}')
        df2.set_index('0', inplace=True)
        dflabel = df2.columns.to_list()

        df = pd.read_csv(f'correlation matrices/corr matrix {hour} {date} with pearson.csv', header=None)
        matrix = df.to_numpy()

        bars = {}
        for i in range(2):
            bars[i] = []

        for i in range (len(dflabel)):
            res = case1(matrix, i)
            pcoef1[dflabel[i]][j] = res
            bars[0].append(res)

            res = case2(matrix, i)
            pcoef2[dflabel[i]][j] = res
            bars[1].append(res)

        j+=1

        graph_score_links(bars, hour, date, dflabel)

    for l in label:
        for c in range(len(pcoef1[l])):
            idc = c - 1
            idw = 1
            aux = pcoef1[l][c]
            aux2 = pcoef2[l][c]

            while (idc >= 0):
                aux += weigth[idw]*(pcoef1[l][idc])
                aux2 += weigth[idw]*(pcoef2[l][idc])
                
                idc -= 1
                idw += 1

            pcoef1[l][c] = aux
            pcoef2[l][c] = aux2

        graph_score_time(pcoef1, pcoef2, hours, date, l)

    print('Graphics with performance score created.')