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

def graph (dict1, dict2, hours, label):
# def graph (dict, hour, label):
    # colors = ['blue', 'lightblue', 'deepskyblue', 'dodgerblue', 'royalblue','mediumblue', 'navy', 'powderblue', 'purple', 'indigo', 'violet', 'mediumpurple', 'darkorchid', 'mediumorchid', 'blueviolet', 'darkmagenta', 'red', 'darkred', 'firebrick', 'indianred', 'orangered', 'tomato', 'coral', 'crimson', 'maroon', 'green', 'lime', 'forestgreen', 'limegreen', 'darkgreen', 'seagreen', 'mediumseagreen', 'springgreen', 'mediumspringgreen', 'lightgreen']

    colors = ['deepskyblue', 'green', 'firebrick', 'violet']

    plt.figure(figsize=(12,9))

    # xlabel = ['case 1', 'case 2', 'case 3', 'case 4']
    xlabel = ['All values', 'Positive values']

    # for i in range(0,2):
    #     plt.plot(label, dict[i], color=colors[i], label=xlabel[i], linewidth=3.0)

    plt.plot(hours, dict1[label], color=colors[0], label=xlabel[0], linewidth=3.0)
    plt.plot(hours, dict2[label], color=colors[1], label=xlabel[1], linewidth=3.0)

    label = label.upper()

    # plt.xlabel('Links', fontsize=15)
    plt.xlabel('Measurement Time', fontsize=15)
    plt.ylabel('Score values', fontsize=15)
    # plt.xticks(label, fontsize=9, rotation=90)
    plt.xticks(hours, fontsize=12)
    plt.yticks(fontsize=12)
    # plt.title(f'Score for May 29th 00-{hour}', fontsize=18)
    plt.title(f'Score for May 29th {label}', fontsize=18)
    plt.legend(loc='upper right', fontsize=12)
    # plt.show()
    # plt.savefig(f'29-05-2023 00-{hour} score.pdf')
    plt.savefig(f'29-05-2023 score {label}.pdf')

if __name__ == "__main__":

    label = ['df-am', 'ba-pb', 'ce-pi', 'rn-pb', 'se-al', 'ms-pr', 'to-df', 'sc-rs', 'se-ba', 'rj-sp', 'ap-pa', 'ro-ac', 'ma-df', 'ce-df', 'ce-rr', 'sp-rs', 'mt-ro', 'ba-mg', 'pr-sp', 'mg-ba', 'ac-ro', 'ce-sp', 'es-ba', 'df-ma', 'pa-ma', 'rs-sp', 'pi-ba', 'es-mg', 'mg-sp', 'pi-ce', 'to-go', 'rs-sc', 'mg-rj', 'df-ce', 'to-pa', 'ba-es', 'pr-rs', 'mg-df', 'ro-mt', 'pb-pe', 'ce-ba', 'ms-mt', 'df-go', 'ba-df', 'ma-pi', 'pe-al', 'ac-df', 'df-mg', 'am-df', 'rs-pr', 'sp-ce', 'am-ap', 'df-ba', 'am-rr', 'sc-sp', 'ap-am', 'ce-rn', 'pi-ma', 'df-to', 'df-ac', 'mt-df', 'pb-rn', 'sp-mg', 'ba-pi', 'ma-pa', 'ba-se', 'sc-pr', 'pr-sc', 'mg-es', 'rn-ce', 'pa-ap', 'rj-es', 'df-mt', 'rr-am', 'pe-pb', 'ba-ce', 'pa-to', 'go-to', 'mt-ms', 'sp-rj', 'sp-pr', 'sp-sc', 'es-rj']

    # label = ['pb-pe', 'mt-ms', 'sp-ce', 'ma-df', 'mg-df', 'rj-es', 'ac-df', 'ce-ba', 'pa-ma', 'sc-sp', 'es-ba', 'ba-ce', 'es-mg', 'mg-ba', 'df-go', 'rs-sc', 'ba-pb', 'ce-sp', 'rj-sp', 'sc-pr', 'ms-mt', 'am-ap', 'go-to', 'pr-rs', 'ap-pa', 'pa-ap', 'am-rr', 'ce-df', 'rs-pr', 'pi-ba', 'ro-mt', 'df-am', 'pi-ce', 'mt-ro', 'pe-al', 'se-ba', 'ba-pi', 'pi-ma', 'ce-pi', 'rr-am', 'sp-pr', 'rn-pb', 'to-df', 'to-go', 'ce-rr', 'df-ce', 'df-mg', 'sp-rs', 'pb-rn', 'ro-ac', 'df-ma', 'df-mt', 'rn-ce', 'mg-sp', 'pr-sc', 'ma-pa', 'ms-pr', 'ap-am', 'se-al', 'df-ac', 'ba-df', 'sp-rj', 'to-pa', 'mg-es', 'ac-ro', 'mg-rj', 'pr-sp', 'pa-to', 'sp-mg', 'ma-pi', 'ce-rn', 'es-rj', 'ba-es', 'mt-df', 'df-ba', 'df-to', 'ba-se', 'am-df', 'sc-rs', 'pe-pb', 'ba-mg', 'sp-sc']

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
    # hours = ['33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '43']

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
            bars[0].append(res)

            res = case2(matrix, i)
            pcoef2[dflabel[i]][j] = res
            bars[1].append(res)

        j+=1
        # name = f'performance coef 23-47 29-05-2023.csv'
        # save_as_csv(pcoef, name)

        # graph(bars, hour, dflabel)

    guiltyAll = {}
    guiltyP = {}

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

        # graph(pcoef1, pcoef2, hours, l)

        # sz = len(pcoef1[l]) - 1
        # sz2 = len(pcoef2[l]) - 1
        # guiltyAll[l] = pcoef1[l][sz]
        # guiltyP[l] = pcoef2[l][sz2]

    sortedGuiltyAll = dict(sorted(pcoef1.items(), key=lambda item: item[1], reverse=False))
    sortedGuiltyP = dict(sorted(pcoef2.items(), key=lambda item: item[1], reverse=False))

    save_as_csv(pcoef1, 'soma de todos os valores 29-05.csv')
    save_as_csv(pcoef2, 'soma dos positivos 29-05.csv')

    save_as_csv(sortedGuiltyAll, 'soma de todos os valores 29-05 ordenado.csv')
    save_as_csv(sortedGuiltyP, 'soma dos positivos 29-05 ordenado.csv')