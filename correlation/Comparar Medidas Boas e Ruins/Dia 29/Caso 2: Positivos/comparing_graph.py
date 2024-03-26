import matplotlib.pyplot as plt
import pandas as pd
import json

def graph (label, dict1, dict2, hours):
    # colors = ['deepskyblue', 'navy'] # case 1
    colors = ['mediumspringgreen', 'darkgreen'] # case 2

    plt.figure(figsize=(12,9))

    xlabel = ['high delay', 'low delay']

    plt.plot(hours, dict1[label], color=colors[0], label=xlabel[0], linewidth=3.0)
    plt.plot(hours, dict2[label], color=colors[1], label=xlabel[1], linewidth=3.0)

    label = label.upper()

    plt.xlabel('Measurement Time', fontsize=15)
    plt.xticks(label, fontsize=12)
    plt.xticks(hours, fontsize=12)
    plt.yticks(fontsize=12)
    plt.title(f'Delays for May 29th {label}', fontsize=18)
    plt.legend(bbox_to_anchor=(0.95, 1), fontsize=12)
    # plt.show()
    plt.savefig(f'29-05-2023 comparison {label}.pdf')


if __name__ == "__main__":
    # label29 = ['df-to','ba-df','sp-rj','sc-rs','pb-ba','ac-df','df-ba','rj-sp','ms-pr','sc-sp']

    label29 = ["ac-df", "ac-ro", "am-ap", "am-df", "am-rr", "ap-pa", "ba-df", "ba-mg", "ba-se", 
    "ce-ba", "ce-mg", "ce-pi", "ce-rj", "ce-rn", "ce-sp", "df-am", "df-ba", "df-mg", 
    "df-mt", "df-to", "es-mg", "es-rj", "go-to", "ma-df", "ma-pi", "mg-ba", "mg-df", 
    "mg-rj", "mg-sp", "ms-mt", "ms-pr", "mt-df", "mt-ro", "pa-ap", "pa-to", "pb-ba", 
    "pb-pe", "pb-rn", "pe-pb", "pi-ce", "pi-ma", "pr-rs", "pr-sp", "rj-sp", "rn-ce", 
    "rn-pb", "ro-ac", "ro-mt", "rr-am", "rs-pr", "rs-sp", "sc-pr", "sc-rs", "sc-sp", 
    "se-ba", "sp-ce", "sp-mg", "sp-pr", "sp-rj", "sp-rs", "to-df", "to-go", "to-pa"]

    # label28 =['df-ba','ce-rr','ma-df','pi-ba','sp-pr','pr-rs','mg-rj','ce-rj','es-rj','rj-sp']

    label28 = ["ac-df", "ac-ro", "am-df", "am-rr", "ap-pa", "ba-df", "ba-mg", "ba-pb", "ba-se", 
    "ce-ba", "ce-mg", "ce-pi", "ce-rj", "ce-rn", "ce-rr", "ce-sp", "df-am", "df-ba", 
    "df-mg", "df-mt", "df-to", "es-ba", "es-mg", "es-rj", "go-to", "ma-df", "ma-pi", 
    "mg-ba", "mg-df", "mg-rj", "mg-sp", "ms-mt", "mt-df", "mt-ro", "pa-ap", "pa-to", 
    "pb-ba", "pb-pe", "pb-rn", "pe-pb", "pi-ba", "pi-ce", "pi-ma", "pr-rs", "pr-sp", 
    "rj-sp", "rn-ce", "rn-pb", "ro-ac", "ro-mt", "rr-am", "rs-pr", "rs-sp", "sc-pr", 
    "se-ba", "sp-ce", "sp-mg", "sp-pr", "sp-rj", "sp-rs", "to-df", "to-go", "to-pa"]

    hours29 = ['00h12', '00h13', '00h14', '00h15', '00h16', '00h17', '00h18', '00h19', '00h20', '00h21']

    hours28 = ['22h33', '22h34', '22h35', '22h36', '22h37', '22h38', '22h39', '22h40', '22h41', '22h42', '22h43']

    df = pd.read_csv('soma dos positivos 29-05 ruim.csv')
    dflabel = df.columns.to_list()

    df2 = pd.read_csv('soma dos positivos 29-05 bom.csv')
    dflabel2 = df.columns.to_list()
    
    dict1 = {}
    dict2 = {}

    for l in label29:
        for i in range (len(dflabel)):
            if (dflabel[i] == l):
                dict1[l] = json.loads(df.iloc[0, i])

            if (dflabel2[i] == l):
                dict2[l] = json.loads(df2.iloc[0, i])

    for l in label29:
        graph(l, dict1, dict2, hours29)
        