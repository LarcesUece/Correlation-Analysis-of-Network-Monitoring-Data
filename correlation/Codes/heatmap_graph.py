import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
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

def heatmap (corr_matrix, ticks, labels, hour, date, method):
    fig, ax = plt.subplots()
    fig.set_figheight(12)
    fig.set_figwidth(12)

    im = ax.imshow(corr_matrix, cmap='RdBu_r')
    im.set_clim(-1, 1)
    
    ax.grid(False)
    ax.xaxis.set(ticks=ticks, ticklabels=labels)
    ax.yaxis.set(ticks=ticks, ticklabels=labels)
    ax.set_ylim((len(labels) - 0.5), -0.5)
    plt.xticks(fontsize=6, rotation=90)
    plt.yticks(fontsize=6)

    for i in range(len(labels)):
        for j in range(len(labels)):
            ax.text(j, i, corr_matrix[i, j], ha='center', va='center',
                    color='black', fontsize=2)
            
    cbar = ax.figure.colorbar(im, ax=ax, format='%.2f')

    directory = 'heatmap graphics'
    if not os.path.exists(directory):
        os.makedirs(directory)

    plt.title(f'{date} {hour} {method}', fontsize=16)
    plt.savefig(f'{directory}/{hour} {date} {method} heatmap.pdf')

if __name__ == "__main__":

    user_path = os.getcwd()
    directory = f'{user_path}/datasets'
    files = os.listdir(directory)

    dates, hours = extract_data(files)
    
    for hour, date, file in zip(hours, dates, files):
        df2 = pd.read_csv(f'datasets/{file}')
        df2.set_index('0', inplace=True)
        labels = df2.columns.to_list()

        # create heatmap size
        ticks = []
        for i in range(len(labels)): 
            ticks.append(i)

        methods = ['pearson', 'spearman', 'kendall']
        for method in methods:
            df = pd.read_csv(f'correlation matrices/corr matrix {hour} {date} with {method}.csv', header=None)
            
            matrix = df.to_numpy()
            matrix = matrix.round(decimals=2)
            heatmap(matrix, ticks, labels, hour, date, method)

    print('Heatmap graphics created.')