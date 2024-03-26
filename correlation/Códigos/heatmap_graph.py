import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# criar o heatmap
def heatmap (corr_matrix, ticks, labels, hour):
    fig, ax = plt.subplots()
    fig.set_figheight(12)
    fig.set_figwidth(12)

    im = ax.imshow(corr_matrix, cmap='RdBu_r')
    im.set_clim(-1, 1)
    
    ax.grid(False)
    ax.xaxis.set(ticks=ticks, ticklabels=labels)
    ax.yaxis.set(ticks=ticks, ticklabels=labels)
    ax.set_ylim((len(labels) - 0.5), -0.5)
    plt.xticks(fontsize=3)
    plt.yticks(fontsize=4)

    for i in range(len(labels)):
        for j in range(len(labels)):
            ax.text(j, i, corr_matrix[i, j], ha='center', va='center',
                    color='black', fontsize=2)
            
    cbar = ax.figure.colorbar(im, ax=ax, format='%.2f')

    plt.title(f"May 29th 00:{hour}", fontsize=16)
    # plt.show()
    plt.savefig(f'00:{hour} 29-05-2023 heatmap.pdf')

if __name__ == "__main__":

    # alterar de acordo com a label do dataset original
    # label

    hours = ['12', '13', '14', '15', '16', '17', '18', '19', '20', '21']
    # hours = ['33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '43']
    
    for h in hours:
        df2 = pd.read_csv(f'matriz de vetores do 29-5-2023 0-{h} sem colunas com zeros.csv')
        df2.set_index('0', inplace=True)
        labels = df2.columns.to_list()

        # criar o tamanho do heatmap
        ticks = []
        for i in range(len(labels)): 
            ticks.append(i)

        # ler documento que possui a matriz de correlação
        df = pd.read_csv(f'corr 00-{h} 29-05-2023.csv', header=None)
        
        # transformar dataframe para o formato de matriz numpy, arredonda os valores e chama a função de criar o heatmap
        matrix = df.to_numpy()
        matrix = matrix.round(decimals=2)
        heatmap(matrix, ticks, labels, h)