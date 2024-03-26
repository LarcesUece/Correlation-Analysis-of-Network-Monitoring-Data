import os
from datetime import date, datetime

import pandas as pd

file_location = "./datasets vazao/cubic/"
destination_location = "./vazao intervalos 4 medidas/cubic/"


files = os.listdir(file_location)
file = sorted(files)

for i in range(len(file) - 1):
    dataset = pd.read_csv(file_location + file[i])
    cont0, cont1, cont2, cont3 = 0, 0, 0, 0
    sum0, sum1, sum2, sum3 = [0], [0], [0], [0]
    mean0, mean1, mean2, mean3 = 0, 0, 0, 0
    dia = None
    f = open(destination_location + "intervalos vazao " + file[i], "w")
    f.write(f"{'Data'},{'Intervalo'},{'Vazao'}\n")
    for i in range(len(dataset["Timestamp"]) - 1):

        data = datetime.fromtimestamp(int(dataset["Timestamp"][i]))

        if dia == None:
            dia = str(data.day)
            dia_anterior = dia
            mes_anterior = str(data.month)
            ano = str(data.year)
        if str(data.day) != dia_anterior:
            if sum(sum0) != 0:
                mean0 = round(sum(sum0) / cont0, 2)
            else:
                mean0 = -1

            f.write(
                f"{dia_anterior+'-'+mes_anterior+'-'+ano},{'00:00:00 a 05:59:59'},{mean0}\n "
            )
            if sum(sum1) != 0:
                mean1 = round(sum(sum1) / cont1, 2)
            else:
                mean1 = -1

            f.write(
                f"{dia_anterior+'-'+mes_anterior+'-'+ano},{'06:00:00 a 11:59:59'},{mean1}\n "
            )
            if sum(sum2) != 0:
                mean2 = round(sum(sum2) / cont2, 2)
            else:
                mean2 = -1

            f.write(
                f"{dia_anterior+'-'+mes_anterior+'-'+ano},{'12:00:00 a 17:59:59'},{mean2}\n "
            )
            if sum(sum3) != 0:
                mean3 = round(sum(sum3) / cont3, 2)
            else:
                mean3 = -1

            f.write(
                f"{dia_anterior+'-'+mes_anterior+'-'+ano},{'18:00:00 a 23:59:59'},{mean3}\n "
            )

            dia = str(data.day)
            dia_anterior = dia
            mes_anterior = str(data.month)
            cont0, cont1, cont2, cont3 = 0, 0, 0, 0
            sum0, sum1, sum2, sum3 = [0], [0], [0], [0]
            mean0, mean1, mean2, mean3 = 0, 0, 0, 0

        if dia == dia_anterior:

            if str(data.time()) >= "00:00:00" and str(data.time()) < "06:00:00":
                cont0 = cont0 + 1
                sum0.append(int(dataset[" Vazao"][i]))
            if str(data.time()) >= "06:00:00" and str(data.time()) < "12:00:00":
                cont1 = cont1 + 1
                sum1.append(int(dataset[" Vazao"][i]))
            if str(data.time()) >= "12:00:00" and str(data.time()) < "18:00:00":
                cont2 = cont2 + 1
                sum2.append(int(dataset[" Vazao"][i]))
            if str(data.time()) >= "18:00:00" and str(data.time()) <= "23:59:59":
                cont3 = cont3 + 1
                sum3.append(int(dataset[" Vazao"][i]))
        else:
            pass

        if i == len(dataset["Timestamp"]) - 2:

            if sum(sum0) != 0:
                mean0 = sum(sum0) / cont0
            else:
                mean0 = -1

            f.write(
                f"{dia_anterior+'-'+mes_anterior+'-'+ano},{'00:00:00 a 05:59:59'},{mean0}\n "
            )
            if sum(sum1) != 0:
                mean1 = sum(sum1) / cont1
            else:
                mean1 = -1

            f.write(
                f"{dia_anterior+'-'+mes_anterior+'-'+ano},{'06:00:00 a 11:59:59'},{mean1}\n "
            )
            if sum(sum2) != 0:
                mean2 = sum(sum2) / cont2
            else:
                mean2 = -1

            f.write(
                f"{dia_anterior+'-'+mes_anterior+'-'+ano},{'12:00:00 a 17:59:59'},{mean2}\n "
            )
            if sum(sum3) != 0:
                mean3 = sum(sum3) / cont3
            else:
                mean3 = -1

            f.write(
                f"{dia_anterior+'-'+mes_anterior+'-'+ano},{'18:00:00 a 23:59:59'},{mean3}\n "
            )

f.close()
