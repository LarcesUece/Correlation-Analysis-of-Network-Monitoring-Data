import csv
import os
import pickle
import re
from datetime import datetime, timedelta

import pandas as pd

""" Important: pay attention to the location of all necessary folders
- The first one used is created before by the high delay filtering code - leaky low.py"""


def merge_csv_files(path_in, path_out, dia, mes, ano, hora, minuto):
    lista_para_cabacalho = [
        "0", "ac-df", "ac-ro", "am-ap", "am-df", "am-rr", "ap-ac",
        "ap-am", "ap-pa", "ba-ce", "ba-df", "ba-es", "ba-mg", "ba-pb",
        "ba-pi", "ba-se", "ce-ba", "ce-df", "ce-pi", "ce-rn", "ce-rr",
        "ce-sp", "df-ac", "df-am", "df-ba", "df-ce", "df-go", "df-ma",
        "df-mg", "df-mt", "df-pa", "df-sp", "df-to", "es-ba", "es-mg",
        "es-rj", "go-df", "go-mt", "go-to", "ma-df", "ma-pa", "ma-pi",
        "mg-ba", "mg-df", "mg-es", "mg-rj", "mg-sp", "ms-mt", "ms-pr",
        "mt-df", "mt-go", "mt-ms", "mt-ro", "pa-ap", "pa-ma", "pa-to",
        "pb-pe", "pb-rn", "pe-al", "pe-pb", "pi-ba", "pi-ce", "pi-ma",
        "pr-rs", "pr-sc", "pr-sp", "rj-df", "rj-es", "rj-mg", "rj-sp",
        "rn-ce", "rn-pb", "ro-ac", "ro-mt", "rr-am", "rr-ce", "rs-pr",
        "rs-sc", "rs-sp", "sc-pr", "sc-rs", "sc-sp", "se-al", "se-ba",
        "sp-ce", "sp-df", "sp-mg", "sp-pr", "sp-rj", "sp-rs", "sp-sc",
        "to-df", "to-go", "to-pa",
    ]
    

    if not os.path.exists(path_out):
        os.makedirs(path_out)

    file_in = [f for f in os.listdir(path_in) if f.endswith(".csv")]
    files_in = sorted(file_in)
    path_file_out = os.path.join(
        path_out,
        "matriz de vetores do "
        + str(dia)
        + "-"
        + str(mes)
        + "-"
        + str(ano)
        + " "
        + str(hora)
        + "-"
        + str(minuto)
        + ".csv",
    )

    with open(path_file_out, "w") as file_out:
        file_out.write(",".join(lista_para_cabacalho) + "\n")
        for file in files_in:

            prefix_value = re.findall(r"\b\w{2}-\w{2}\b", file[:52])
            file_path = os.path.join(path_in, file)
            with open(file_path, "r") as input_file:
                lines = input_file.readlines()[1:]  # Ignora o cabeçalho.
                # Adiciona o prefixo à frente de cada linha.
                lines = [f"{prefix_value[0]}, {line}" for line in lines]
                file_out.writelines(lines)


def remove_columns_with_zeros(file_in, file_out):
    df = pd.read_csv(file_in)
    colunas_com_zeros = df.columns[(df == 0).all()]
    df = df.drop(columns=colunas_com_zeros)
    df.to_csv(file_out, index=False)


def create_csv_file(file_name, list_of_lists, key_list):
    with open(file_name, mode="w", newline="") as file_csv:
        escritor_csv = csv.writer(
            file_csv, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL
        )
        escritor_csv.writerow(key_list)

        for lista_interna in list_of_lists:
            escritor_csv.writerow(lista_interna)


def load_list(path_file_key_list, path_file_key_values):
    with open(path_file_key_list, "rb") as file_keys:
        chaves = pickle.load(file_keys)
    with open(path_file_key_values, "rb") as files_values:
        valores = pickle.load(files_values)

    return chaves, valores


def creater_vector(path_file):

    path_file_key_list = "./lists/key_list.pkl"
    path_file_key_values = "./lists/values_list.pkl"
    key_list, lista_valores = load_list(path_file_key_list, path_file_key_values)
    lista_linha = []
    lista_completa = []

    caso_part1 = ".*monipe.*"
    caso_part2 = ".*cap1-popap.*"
    caso_part3 = ".*csc1-udesc.*"
    caso_part4 = ".*crs1-poprs.*"

    with open(path_file, "r") as csv_file:
        reader = csv.reader(csv_file)
        next(reader)

        for linha in reader:
            lista_linha = [0] * len(key_list)

            for valor_coluna in linha:
                for valor in lista_valores:

                    resultado = re.search(valor, valor_coluna[:10])
                    res1 = re.search(caso_part1, valor_coluna[:13])
                    res2 = re.search(caso_part2, valor_coluna[:13])
                    res3 = re.search(caso_part3, valor_coluna[:13])
                    res4 = re.search(caso_part4, valor_coluna[:13])
                    if res1 or res2 or res3 or res4:
                        resultado = False

                    if resultado:
                        posicao = lista_valores.index(valor)
                        lista_linha[posicao] = 1

                    else:
                        pass

            lista_completa.append(lista_linha)

    return lista_completa, key_list


def check_intervalo(timestamp1, timestamp2):
    time1 = datetime.fromtimestamp((timestamp1))
    time2 = datetime.fromtimestamp((timestamp2))
    time_difference = time2 - time1
    return abs(time_difference) <= timedelta(minutes=220) and (time1 > time2)


def select_traceroute(file1, file2, saida):
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2, header=None)
    found_lines = []

    for _, linha in df1.iterrows():
        timestamp1 = linha["Timestamp"]

        filtra_linha = df2[df2[0].apply(lambda x: check_intervalo(timestamp1, x))]

        if not filtra_linha.empty:
            linha_prox = filtra_linha.loc[filtra_linha[0].idxmax()]
            found_lines.append(linha_prox)

    result_df = pd.DataFrame(found_lines)
    if not result_df.empty:
        result_df.columns = df2.columns

        result_df.to_csv(saida, index=False)
    else:
        lista_arq_vazios.append(file1)



def select_delay_day(
    entry_directory, exit_directory, nome_ant, nome_nov, dia, mes, ano
):

    if not os.path.exists(exit_directory):
        os.makedirs(exit_directory)

    files_in = os.listdir(entry_directory)
    files = sorted(files_in)

    for file in files:
        if file.endswith(".csv"):
            path_in = os.path.join(entry_directory, file)
            df = pd.read_csv(path_in)

            df["Data"] = pd.to_datetime(df["Data"])
            data_filtrada = df[
                (df["Data"].dt.day == dia)
                & (df["Data"].dt.month == mes)
                & (df["Data"].dt.year == ano)
            ]

            if not data_filtrada.empty:
                nome_file_out = file.replace(nome_ant, nome_nov)
                path_out = os.path.join(exit_directory, nome_file_out)
                data_filtrada.to_csv(path_out, index=False)


def select_delay_day_minuto(
    entry_directory, exit_directory, nome_ant, nome_nov, dia, mes, ano, hora, minuto
):

    if not os.path.exists(exit_directory):
        os.makedirs(exit_directory)

    files_in = os.listdir(entry_directory)
    files = sorted(files_in)

    for file in files:
        if file.endswith(".csv"):
            path_in = os.path.join(entry_directory, file)
            df = pd.read_csv(path_in)
            df["Data"] = pd.to_datetime(df["Data"])
            data_filtrada = df[
                (df["Data"].dt.day == dia)
                & (df["Data"].dt.month == mes)
                & (df["Data"].dt.year == ano)
                & (df["Data"].dt.hour == hora)
                & (df["Data"].dt.minute == minuto)
            ]

            if not data_filtrada.empty:
                nome_file_out = file.replace(nome_ant, nome_nov)
                path_out = os.path.join(exit_directory, nome_file_out)
                data_filtrada.to_csv(path_out, index=False)


if __name__ == "__main__":
    dia = 30
    mes = 4
    ano = 2023

    hora = 7
    minutos = [12, 13, 14, 15, 16, 17, 18]
    
    # entry_directory = "./datasets alterados/filtragem de desempenho/desempenho atraso alto total 6 meses/"
    # exit_directory = "./datasets alterados/filtragem de desempenho/alto/_resultado atraso alto dia " + str(dia) +" "+ str(mes) +" "+ str(ano)+"/"
    entry_directory = "./datasets alterados/filtragem de desempenho/desempenho atraso baixo total 6 meses/"
    exit_directory = (
        "./datasets alterados/filtragem de desempenho/baixo/_resultado atraso baixo dia "
        + str(dia)
        + " "
        + str(mes)
        + " "
        + str(ano)
        + "/"
    )
    nome_ant = "desempenho atraso"
    nome_nov = "atraso alto do dia"

    select_delay_day(entry_directory, exit_directory, nome_ant, nome_nov, dia, mes, ano)
    print("Processing completed.")

    """ Seleciona o atraso pela hora e minuto """
    for minuto in minutos:
        # entry_directory = "./datasets alterados/filtragem de desempenho/_resultado vazao baixa bbr dia 29 05 2023/"
        # entry_directory = "./datasets alterados/filtragem de desempenho/_resultado vazao baixa cubic dia 29 05 2023/"
        # entry_directory = "./datasets alterados/filtragem de desempenho/alto/_resultado atraso alto dia " + str(dia) +" "+ str(mes) +" "+ str(ano)+"/"
        entry_directory = (
            "./datasets alterados/filtragem de desempenho/baixo/_resultado atraso baixo dia "
            + str(dia)
            + " "
            + str(mes)
            + " "
            + str(ano)
            + "/"
        )
        # exit_directory = "./datasets alterados/filtragem de desempenho/vetores e matrizes/resultado vazao baixa bbr em um dia " + str(dia) + " mes " + str(mes) + " hora-minuto "+str(hora)+"-"+str(minuto)+"/"
        # exit_directory = "./datasets alterados/filtragem de desempenho/vetores e matrizes/resultado vazao baixa cubic em um dia " + str(dia) + " mes " + str(mes) + " hora-minuto "+str(hora)+"-"+str(minuto)+"/"
        # exit_directory = "./datasets alterados/filtragem de desempenho/alto/vetores e matrizes/resultado atraso em um dia " + str(dia) + " mes " + str(mes) + " hora-minuto "+str(hora)+"-"+str(minuto)+"/"
        exit_directory = (
            "./datasets alterados/filtragem de desempenho/baixo/vetores e matrizes/resultado atraso em um dia "
            + str(dia)
            + " mes "
            + str(mes)
            + " hora-minuto "
            + str(hora)
            + "-"
            + str(minuto)
            + "/"
        )
        # nome_ant = 'vazao baixa do dia bbr esmond data'
        # nome_nov = 'vazao baixa bbr em um dia hora minuto ' + str(hora) + " e " + str(minuto)
        # nome_ant = 'vazao baixa do dia cubic esmond data'
        # nome_nov = 'vazao baixa cubic em um dia hora minuto ' + str(hora) + " e " + str(minuto)
        # nome_ant = 'alto atraso do dia esmond data'
        # nome_nov = 'alto atraso em um dia hora minuto ' + str(hora) + " e " + str(minuto)
        nome_ant = "baixo atraso do dia esmond data"
        nome_nov = (
            "baixo atraso em um dia hora minuto " + str(hora) + " e " + str(minuto)
        )
        select_delay_day_minuto(
            entry_directory,
            exit_directory,
            nome_ant,
            nome_nov,
            dia,
            mes,
            ano,
            hora,
            minuto,
        )

    print("Processamento concluído.")
    print()
    print("Procurando o traceroute.")
    print()

    for minuto in minutos:
        lista_arq_vazios = []
        # entry_directory1 = "./datasets alterados/filtragem de desempenho/vetores e matrizes/result bbr/"
        # entry_directory1 = "./datasets alterados/filtragem de desempenho/vetores e matrizes/result cubic/"
        # entry_directory1 = "./datasets alterados/filtragem de desempenho/alto/vetores e matrizes/resultado atraso em um dia " + str(dia) + " mes " + str(mes) + " hora-minuto "+str(hora)+"-"+str(minuto)+"/"
        entry_directory1 = (
            "./datasets alterados/filtragem de desempenho/baixo/vetores e matrizes/resultado atraso em um dia "
            + str(dia)
            + " mes "
            + str(mes)
            + " hora-minuto "
            + str(hora)
            + "-"
            + str(minuto)
            + "/"
        )
        entry_directory2 = "./datasets traceroute/"
        # exit_directory = "./datasets alterados/filtragem de desempenho/vetores e matrizes/traceroute vazao/bbr/"
        # exit_directory = "./datasets alterados/filtragem de desempenho/vetores e matrizes/traceroute vazao/cubic/"
        # exit_directory = "./datasets alterados/filtragem de desempenho/alto/vetores e matrizes/traceroute atraso em um dia " + str(dia) + " mes " + str(mes) + " hora-minuto "+str(hora)+"-"+str(minuto)+"/"
        exit_directory = (
            "./datasets alterados/filtragem de desempenho/baixo/vetores e matrizes/traceroute atraso em um dia "
            + str(dia)
            + " mes "
            + str(mes)
            + " hora-minuto "
            + str(hora)
            + "-"
            + str(minuto)
            + "/"
        )
        # nome = ' traceroute vazao bbr do dia '+ str(dia) + " hora " + str(hora) + " minuto " + str(minuto) + " "
        # nome = ' traceroute vazao cubic do dia '+ str(dia) + " hora " + str(hora) + " minuto " + str(minuto) + " "
        nome = (
            " traceroute atraso alto do dia "
            + str(dia)
            + " hora "
            + str(hora)
            + " minuto "
            + str(minuto)
            + " "
        )

        if not os.path.exists(exit_directory):
            os.makedirs(exit_directory)
        file_1 = os.listdir(entry_directory1)
        files1 = sorted(file_1)
        file_2 = os.listdir(entry_directory2)
        files2 = sorted(file_2)
        for file1 in files1:
            nome_links1 = re.findall(r"\b\w{2}-\w{2}\b", file1[:50])
            for file2 in files2:

                nome_links2 = re.findall(r"\b\w{2}-\w{2}\b", file2[:40])
                if nome_links1[0] == nome_links2[0]:
                    print(file1)
                    print(file2)
                    saida = exit_directory + nome + str(nome_links1[0]) + ".csv"
                    select_traceroute(
                        entry_directory1 + file1,
                        entry_directory2 + file2,
                        saida,
                    )
                else:
                    print("searching for the correct file")

    print("Processing completed.")
    print()
    print("creating the matrix.")
    print()

    for minuto in minutos:
        # entry_directory = "./datasets alterados/filtragem de desempenho/_traceroute atraso alto dia/"
        # entry_directory = "./datasets alterados/filtragem de desempenho/alto/vetores e matrizes/traceroute atraso em um dia " + str(dia) + " mes " + str(mes) + " hora-minuto "+str(hora)+"-"+str(minuto)+"/"
        entry_directory = (
            "./datasets alterados/filtragem de desempenho/baixo/vetores e matrizes/traceroute atraso em um dia "
            + str(dia)
            + " mes "
            + str(mes)
            + " hora-minuto "
            + str(hora)
            + "-"
            + str(minuto)
            + "/"
        )
        # exit_directory = "./datasets alterados/filtragem de desempenho/vetores atraso alto dia/"
        # exit_directory = "./datasets alterados/filtragem de desempenho/alto/vetores e matrizes/vetores da hora " + str(hora) + " e " + str(minuto) + " do dia " + str(dia) + "-" + str(mes) + "-" + str(ano) + "/"
        exit_directory = (
            "./datasets alterados/filtragem de desempenho/baixo/vetores e matrizes/vetores da hora "
            + str(hora)
            + " e "
            + str(minuto)
            + " do dia "
            + str(dia)
            + "-"
            + str(mes)
            + "-"
            + str(ano)
            + "/"
        )
        # exit_directory_sem_zeros = "./datasets alterados/filtragem de desempenho/vetores atraso alto dia sem zeros/"
        # exit_directory_sem_zeros = "./datasets alterados/filtragem de desempenho/alto/vetores e matrizes/vetores da hora " + str(hora) + " e " + str(minuto) + " do dia " + str(dia) + "-" + str(mes) + "-" + str(ano) + " sem colunas com zeros/"
        exit_directory_sem_zeros = (
            "./datasets alterados/filtragem de desempenho/baixo/vetores e matrizes/vetores da hora "
            + str(hora)
            + " e "
            + str(minuto)
            + " do dia "
            + str(dia)
            + "-"
            + str(mes)
            + "-"
            + str(ano)
            + " sem colunas com zeros/"
        )

        if not os.path.exists(exit_directory):
            os.makedirs(exit_directory)
        if not os.path.exists(exit_directory_sem_zeros):
            os.makedirs(exit_directory_sem_zeros)

        files_in = os.listdir(entry_directory)
        files = sorted(files_in)

        for file in files:
            path_file = os.path.join(entry_directory, file)
            nome_file_out = file.replace("traceroute", "vetor")

            path_out = os.path.join(exit_directory, nome_file_out)
            lista, lista_cabecalho = creater_vector(path_file)
            create_csv_file(path_out, lista, lista_cabecalho)

            print("file {} pronto".format(file))

        files_in = os.listdir(exit_directory)
        files = sorted(files_in)

        for file in files:
            path_file = os.path.join(exit_directory, file)
            nome_file_out = file.replace("vetor", "vetor sem zeros")

            path_out = os.path.join(exit_directory_sem_zeros, nome_file_out)

            remove_columns_with_zeros(path_file, path_out)

            print("file {} pronto".format(file))

        # path_in = "./datasets alterados/filtragem de desempenho/alto/vetores e matrizes/vetores da hora " + str(hora) + " e " + str(minuto) + " do dia " + str(dia) + "-" + str(mes) + "-" + str(ano) + "/"
        # path_out = "./datasets alterados/filtragem de desempenho/alto/vetores e matrizes/matrizes/matriz de vetores da hora " + str(hora) + " do min " + str(minuto) + " do dia " + str(dia) + "-" + str(mes) + "-" + str(ano) + "/"
        path_in = (
            "./datasets alterados/filtragem de desempenho/baixo/vetores e matrizes/vetores da hora "
            + str(hora)
            + " e "
            + str(minuto)
            + " do dia "
            + str(dia)
            + "-"
            + str(mes)
            + "-"
            + str(ano)
            + "/"
        )
        path_out = (
            "./datasets alterados/filtragem de desempenho/baixo/vetores e matrizes/matrizes/matriz de vetores da hora "
            + str(hora)
            + " do min "
            + str(minuto)
            + " do dia "
            + str(dia)
            + "-"
            + str(mes)
            + "-"
            + str(ano)
            + "/"
        )
        merge_csv_files(path_in, path_out, dia, mes, ano, hora, minuto)

        caminho_file_in = os.path.join(
            path_out,
            "matriz de vetores do "
            + str(dia)
            + "-"
            + str(mes)
            + "-"
            + str(ano)
            + " "
            + str(hora)
            + "-"
            + str(minuto)
            + ".csv",
        )
        path_file_out = os.path.join(
            path_out,
            "matriz de vetores do "
            + str(dia)
            + "-"
            + str(mes)
            + "-"
            + str(ano)
            + " "
            + str(hora)
            + "-"
            + str(minuto)
            + " sem colunas com zeros.csv",
        )
        remove_columns_with_zeros(caminho_file_in, path_file_out)
    print()
    print("All Processing completed.")
