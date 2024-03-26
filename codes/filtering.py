import os

import pandas as pd

# file_location = "./datasets vazao/bbr/"
# destination_location = "./desempenho/vazao/bbr/"
file_location = "./datasets atraso/"
destination_location = "./desempenho/atraso/"

files = os.listdir(file_location)
file = sorted(files)
for i in range(len(files) - 1):
    dataset = pd.read_csv(file_location + file[i])

    f = open(destination_location + "desempenho atraso " + file[i], "w")
    # f = open(destination_location + "desempenho vazao " + file[i], "w")
    f.write(f"{'Timestamp'},{'Data'},{'Atraso'}\n")
    for i in range(len(dataset["Timestamp"]) - 1):
        if float(dataset[" Atraso (ms)"][i]) > 60.00:
            # if float(dataset[' Vazao'][i]) <= 200000000.0:
            f.write(
                f"{dataset['Timestamp'][i]},{dataset['Data'][i]},{float(dataset[' Atraso (ms)'][i])}\n "
            )
            # f.write(f"{dataset['Timestamp'][i]},{dataset['Data'][i]},{int(dataset[' Vazao'][i])}\n ")


f.close()
