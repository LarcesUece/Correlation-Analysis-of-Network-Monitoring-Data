import os

import pandas as pd


def select_delay_day(
    entry_directory, exit_directory, nome_ant, nome_nov, dia, mes, ano
):

    if not os.path.exists(exit_directory):
        os.makedirs(exit_directory)

    input_files = os.listdir(entry_directory)
    files = sorted(input_files)

    for file in files:
        if file.endswith(".csv"):
            input_path = os.path.join(entry_directory, file)
            df = pd.read_csv(input_path)
            df["Data"] = pd.to_datetime(df["Data"])
            data_filtrada = df[
                (df["Data"].dt.day == dia)
                & (df["Data"].dt.month == mes)
                & (df["Data"].dt.year == ano)
            ]

            if not data_filtrada.empty:
                output_file_name = file.replace(nome_ant, nome_nov)
                exit_path = os.path.join(exit_directory, output_file_name)
                data_filtrada.to_csv(exit_path, index=False)


def select_delay_day_minuto(
    entry_directory, exit_directory, nome_ant, nome_nov, dia, mes, ano, hora, minuto
):

    if not os.path.exists(exit_directory):
        os.makedirs(exit_directory)

    input_files = os.listdir(entry_directory)
    files = sorted(input_files)

    for file in files:
        if file.endswith(".csv"):
            input_path = os.path.join(entry_directory, file)
            df = pd.read_csv(input_path)
            df["Data"] = pd.to_datetime(df["Data"])
            data_filtrada = df[
                (df["Data"].dt.day == dia)
                & (df["Data"].dt.month == mes)
                & (df["Data"].dt.year == ano)
                & (df["Data"].dt.hour == hora)
                & (df["Data"].dt.minute == minuto)
            ]

            if not data_filtrada.empty:
                output_file_name = file.replace(nome_ant, nome_nov)
                exit_path = os.path.join(exit_directory, output_file_name)
                data_filtrada.to_csv(exit_path, index=False)


if __name__ == "__main__":
    dia = 28
    mes = 5
    ano = 2023

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
