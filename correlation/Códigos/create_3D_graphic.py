import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import numpy as np
from pkg_resources import yield_lines
import pandas as pd
import json

def createAxis (df, links, hours):
    x = []
    y = []
    z = []

    sz_links = len(links)
    sz_hours = len(hours)

    for i in range (sz_links):
        aux_list = json.loads(df.iloc[0, i])
        z.append(aux_list)

        for j in range(sz_hours):
            x.append(i+1)
            y.append(j+1)

    return x, y, z


def createGraphic (xlabel, ylabel, xvalue, yvalue, zvalue):
    # eixo x = links utilizados (numero de links)
    # eixo y = horario das mediçoes com atraso (tamanho da sequencia)
    # eixo z = score correspondente

    x = np.array(xvalue)
    y = np.array(yvalue)
    z = np.array(zvalue)

    x = x.reshape(z.shape)
    y = y.reshape(z.shape)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    surf = ax.plot_surface(x, y, z, rstride=1, cstride=1, cmap='plasma', edgecolor='none')

    ax.set_xlabel('Number of Links')
    ax.set_ylabel('High Delay Sequence Size')
    ax.set_zlabel('Score Value')
    
    plt.title('May 29th High Delay Links - Case 1')
    # plt.title('May 29th High Delay Links - Case 2')
    fig.colorbar(surf, shrink=0.5, aspect=10, pad=0.15)
    plt.savefig('Links com atraso - Todos os Valores.pdf')
    # plt.savefig('Links com atraso - Positivos.pdf')

if __name__ == "__main__":

    df = pd.read_csv('soma de todos os valores 29-05.csv')
    # df = pd.read_csv('soma dos positivos 29-05.csv')
    dflabel = df.columns.to_list()

    hours = ['00h12', '00h13', '00h14', '00h15', '00h16', '00h17', '00h18', '00h19', '00h20', '00h21']
    # hours = ['22h33', '22h34', '22h35', '22h36', '22h37', '22h38', '22h39', '22h40', '22h41', '22h42', '22h43']

    x, y, z = createAxis(df, dflabel, hours)
    createGraphic(dflabel, hours, x, y, z)