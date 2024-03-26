import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import csv

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

def case3 (matrix, id):
    sum = .0
    aux_matrix = np.shape(matrix)
    columns_number = aux_matrix[1]
    for i in range(columns_number):
        if (matrix[id, i] > 0.5):
            sum += matrix[id, i]

    return sum

def case4 (matrix, id):
    sum = .0
    aux_matrix = np.shape(matrix)
    columns_number = aux_matrix[1]
    for i in range(columns_number):
        if (matrix[id, i] > 0.5 or matrix[id, i] < -0.5):
            sum += matrix[id, i]

    return sum

def save_as_csv (dict, name):
    with open(name, 'w', newline='') as arquivo_csv:
        escritor = csv.DictWriter(arquivo_csv, fieldnames=dict.keys())
        escritor.writeheader()
        escritor.writerow(dict)

# def graph (dict1, dict2, hours, label):
def graph (dict1, dict2, hours, label):
    # colors = ['blue', 'lightblue', 'deepskyblue', 'dodgerblue', 'royalblue','mediumblue', 'navy', 'powderblue', 'purple', 'indigo', 'violet', 'mediumpurple', 'darkorchid', 'mediumorchid', 'blueviolet', 'darkmagenta', 'red', 'darkred', 'firebrick', 'indianred', 'orangered', 'tomato', 'coral', 'crimson', 'maroon', 'green', 'lime', 'forestgreen', 'limegreen', 'darkgreen', 'seagreen', 'mediumseagreen', 'springgreen', 'mediumspringgreen', 'lightgreen']

    colors = ['deepskyblue', 'green', 'firebrick', 'violet']

    plt.figure(figsize=(12,9))

    # xlabel = ['case 1', 'case 2', 'case 3', 'case 4']
    xlabel = ['case 1', 'case 2']

    # for i in range(len(label)):
    #     if (label[i] =='ce-mg'):
    #         label[i] = 'es-mg'

    # label = sorted(label)

    # for i in range(0,2):
    #     plt.plot(label, dict[i], color=colors[i], label=xlabel[i], linewidth=3.0)

    # if (label =='ce-mg'):
    #     label = 'es-mg'

    plt.plot(hours, dict1[label], color=colors[0], label=xlabel[0], linewidth=3.0)
    plt.plot(hours, dict2[label], color=colors[1], label=xlabel[1], linewidth=3.0)

    label = label.upper()

    # plt.xlabel('Links', fontsize=15)
    plt.xlabel('Measurement Time', fontsize=15)
    plt.ylabel('Score values', fontsize=15)
    # plt.xticks(label, fontsize=10, rotation=90)
    plt.xticks(hours, fontsize=12)
    plt.yticks(fontsize=12)
    # plt.title(f'Score for May 29th 00-{hour}', fontsize=18)
    plt.title(f'Score for May 29th {label}', fontsize=18)
    plt.legend(bbox_to_anchor=(1.12, 1), fontsize=12)
    # plt.show()
    # plt.savefig(f'29-05-2023 00-{hour} score.pdf')
    plt.savefig(f'29-05-2023 score {label}.pdf')

if __name__ == "__main__":

    label = ['ro-ac', 'am-rr', 'se-ba', 'pr-sp', 'to-pa', 'pr-rs', 'ma-pi', 'pi-ce', 'rj-sp', 'ac-df', 'rn-ce', 'ma-df', 'ms-mt', 'pi-ma', 'sc-sp', 'rs-sp', 'sp-rs', 'mg-ba', 'ce-pi', 'df-mg', 'df-ba', 'pb-pe', 'rs-pr', 'mg-df', 'es-rj', 'am-df', 'mt-ro', 'pb-ba', 'pa-to', 'ms-pr', 'ce-rn', 'ro-mt', 'ce-ba', 'mg-rj', 'sc-pr', 'sp-pr', 'rn-pb', 'sp-rj', 'ce-sp', 'pb-rn', 'rr-am', 'ba-se', 'mg-sp', 'ce-rj', 'am-ap', 'ap-pa', 'df-am', 'sp-mg', 'pa-ap', 'mt-df', 'sc-rs', 'to-df', 'ac-ro', 'es-mg', 'ba-mg', 'to-go', 'pe-pb', 'df-mt', 'sp-ce', 'ce-mg', 'df-to', 'ba-df', 'go-to']

    weigth = []
    for w in range(1, 200, 2):
        weigth.append(1/w)

    pcoef1 = {}
    pcoef2 = {}
    for i in range(len(label)):
        pcoef1[label[i]] = []
        pcoef2[label[i]] = []

    for i in range(len(label)):
        for j in range(10):
            pcoef1[label[i]].append(-1.0)
            pcoef2[label[i]].append(-1.0)

    hours = ['12', '13', '14', '15', '16', '17', '18', '19', '20', '21']

    j = 0
    for hour in hours:
        df2 = pd.read_csv(f'matriz de vetores do 29-5-2023 0-{hour} sem colunas com zeros.csv')
        df2.set_index('0', inplace=True)
        dflabel = df2.columns.to_list()

        df = pd.read_csv(f'corr 00-{hour} 29-05-2023.csv', header=None)
        matrix = df.to_numpy()

        bars = {}
        for i in range(4):
            bars[i] = []

        for i in range (len(dflabel)):
            res = case1(matrix, i)
            pcoef1[dflabel[i]][j] = res
            # bars[0].append(res)

            res = case2(matrix, i)
            pcoef2[dflabel[i]][j] = res
            # bars[1].append(res)

        j+=1
        # name = f'performance coef 23-47 28-05-2023.csv'
        # save_as_csv(pcoef, name)

        # graph(bars, hour, dflabel)

    for l in label:
        for c in range(len(pcoef1[l])):
            idc = c - 1
            idw = 1
            aux = pcoef1[l][c]
            aux2 = pcoef2[l][c]

            while (idc >= 0):
                if (pcoef1[l][idc] >= 0):
                    aux -= weigth[idw]*(pcoef1[l][idc])
                else : 
                    aux += weigth[idw]*(pcoef1[l][idc])

                if (pcoef2[l][idc] >= 0):
                    aux2 -= weigth[idw]*(pcoef2[l][idc])
                else : 
                    aux2 += weigth[idw]*(pcoef2[l][idc])
                
                idc -= 1
                idw += 1

            pcoef1[l][c] = aux
            pcoef2[l][c] = aux2

        graph(pcoef1, pcoef2, hours, l)