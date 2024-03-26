import os

import pandas as pd

"""Generates datasets with low performance (low throughput or high delay)
-First step to generate the other datasets
-In comments are the command lines to be used to generate for leak"""

# local_file = "./datasets vazao/bbr/"
# directory_out = "./datasets alterados/filtragem de desempenho/desempenho vazao baixa total 6 meses/bbr/"
local_file = "./datasets atraso/"
# directory_out = "./datasets alterados/filtragem de desempenho/desempenho atraso alto total 6 meses/"
directory_out = "./datasets alterados/filtragem de desempenho/desempenho atraso baixo total 6 meses/"
if not os.path.exists(directory_out):
    os.makedirs(directory_out)

files = os.listdir(local_file)
file = sorted(files)
for i in range(len(files)):
    dataset = pd.read_csv(local_file + file[i])

    f = open(directory_out + "desempenho " + file[i], "w")
    # f = open(directory_out + "desempenho vazao " + file[i], "w")
    f.write(f"{'Timestamp'},{'Data'},{'Atraso'}\n")
    # f.write(f"{'Timestamp'},{'Data'},{'Vazao'}\n")
    for i in range(len(dataset["Timestamp"]) - 1):
        if float(dataset["Atraso"][i]) < 60.00:
            # if float(dataset[' Vazao'][i]) <= 200000000.0:
            f.write(
                f"{dataset['Timestamp'][i]},{dataset['Data'][i]},{str(dataset['Atraso'][i])}\n "
            )
            # f.write(
            #    f"{dataset['Timestamp'][i]},{dataset['Data'][i]},{int(dataset[' Vazao'][i])}\n "
            # )


f.close()
