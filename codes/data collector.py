import os
import time
from datetime import date, datetime

import requests
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning

today = date.today()

base = "http://monipe-central.rnp.br"


def get_response(url, time_range):
    cont = 0
    while True:
        header = {"time-range": time_range}
        response = requests.get(url, params=header, verify=False)
        if response.status_code == 200:
            return response
        else:
            cont = cont + 1
            print(
                "Received Status Code {}. Trying again in 1 min...".format(
                    response.status_code
                )
            )
            print("Trial: {}".format(cont))
            time.sleep(60)


def get_data(url, time_range):
    response = get_response(url, time_range)
    json_data = response.json()

    return json_data


def request_by_metadata_key(url, type):
    response = requests.get(url, verify=False)

    json_data = response.json()

    if response.status_code == 200:
        for obj in json_data["event-types"]:
            if obj["event-type"] == type:

                return obj
    else:
        return response.status_code


def calc_mean(val):
    values = []
    for key, value in val.items():
        values.append(float(key))

    return round(sum(values) / len(values), 2)


def request(
    folder, name, source, destination, type, time_range, target_bandwidth="9999999999"
):
    disable_warnings(InsecureRequestWarning)
    url = "http://monipe-central.rnp.br/esmond/perfsonar/archive/?"
    hearder = {
        "pscheduler-test-type": type,
        "source": source,
        "destination": destination,
        "bw-target-bandwidth": target_bandwidth,
        "time-range": time_range,
    }
    response = requests.get(url, params=hearder, verify=False)

    print("endereço", response.url)
    if not os.path.exists(folder):
        os.makedirs(folder)

    json_data = response.json()
    if response.status_code == 200:
        datas = []
        for obj in json_data:
            url_obj = obj["url"]

            get_url_base_obj = request_by_metadata_key(url_obj, type)

            if not isinstance(get_url_base_obj, int):
                url_base = get_url_base_obj["base-uri"]
                f = open(
                    folder
                    + name
                    + " esmond data "
                    + source.split("-")[1]
                    + "-"
                    + destination.split("-")[1]
                    + " "
                    + today.strftime("%m-%d-%Y")
                    + ".csv",
                    "w",
                )
                f.write(f"{'Timestamp'},{'Data'},{'Vazao'}\n")
                data = get_data(base + url_base, time_range)
                datas.insert(0, data)
            else:
                return "Error " + response.status_code
        teste = []
        for i in range(len(datas)):
            cont = 0
            soma = 0
            anterior = None
            for obj in datas[i]:
                data = datetime.fromtimestamp(int(obj["ts"]))
                dia = str(data).split()[0][-2::]
                if (str(data).split()[0][-5::]) not in teste:
                    teste.append(str(data).split()[0][-5::])
                if dia == anterior or anterior is None:
                    soma += obj["val"]
                    cont += 1

                    f.write(
                        f"{int(obj['ts'])},{datetime.fromtimestamp(int(obj['ts'])).strftime('%Y-%m-%d %H:%M:%S')},{str(obj['val'])}\n "
                    )

        f.close()
    else:
        return "Error: " + response.status_code


def request_traceroute(folder, name, source, destination, type, time_range):
    disable_warnings(InsecureRequestWarning)
    limite = "?limit=26400"
    url = "http://monipe-central.rnp.br/esmond/perfsonar/archive/?"
    header = {
        "pscheduler-test-type": type,
        "source": source,
        "destination": destination,
        "time-range": time_range,
    }
    response = requests.get(url, params=header, verify=False)

    if not os.path.exists(folder):
        os.makedirs(folder)
    json_data = response.json()
    values = []
    if response.status_code == 200:
        print("Ok")
        bases = []
        for obj in json_data:
            types_list = obj["event-types"]
            for obj_types in types_list:
                if obj_types.get("event-type") == "packet-trace":
                    bases.append(obj_types.get("base-uri"))
                    break

    with open(
        folder
        + name
        + " esmond data "
        + source.split("-")[1]
        + "-"
        + destination.split("-")[1]
        + " "
        + today.strftime("%m-%d-%Y")
        + ".csv",
        "w",
    ) as f:

        for link in bases:

            values: list = get_data(base + link + limite, time_range)

            for obj in values:

                for dado in range(len(obj["val"])):
                    try:

                        if dado != len(obj["val"]) - 1:
                            f.write(f"{obj['val'][dado]['hostname']},")
                            # f.write(f"{obj['val'][dado]['ip']}, {obj['val'][dado]['hostname']},")
                        else:
                            f.write(f"{obj['val'][dado]['hostname']}\n")
                            # f.write(f"{obj['val'][dado]['ip']}, {obj['val'][dado]['hostname']}")
                    except BaseException:
                        if dado != len(obj["val"]) - 1:
                            f.write("'No Hostname',")
                            # f.write("'No Ip', 'No Hostname',")
                        else:
                            f.write("'No Hostname'\n")
                            # f.write("'No Ip', 'No Hostname'")

    f.close()


def request_atraso(folder, name, source, destination, type, time_range, label):
    disable_warnings(InsecureRequestWarning)
    limite1 = "?limit=285000"
    url = "http://monipe-central.rnp.br/esmond/perfsonar/archive/?"
    header = {
        "pscheduler-test-type": type,
        "source": source,
        "destination": destination,
        "time-range": time_range,
    }

    response = requests.get(url, params=header, verify=False)
    print(response.url)
    if not os.path.exists(folder):
        os.makedirs(folder)
    json_data = response.json()
    values = []
    if response.status_code == 200:
        print("Ok")
        bases = []
        for obj in json_data:
            types_list = obj["event-types"]
            for obj_types in types_list:
                if obj_types.get("event-type") == label:
                    bases.append(obj_types.get("base-uri"))
                    break
        with open(
            folder
            + name
            + " esmond data "
            + source.split("-")[1]
            + "-"
            + destination.split("-")[1]
            + " "
            + today.strftime("%m-%d-%Y")
            + ".csv",
            "w",
        ) as f:
            f.write(f"{'Timestamp'},{'Data'},{'Atraso(ms)'}\n")
            for link in bases:
                values = get_data(base + link + limite1, time_range)
                for value in values:
                    f.write(
                        f"{value['ts']},{datetime.fromtimestamp(int(value['ts'])).strftime('%Y-%m-%d %H:%M:%S')},{calc_mean(value['val'])}\n"
                    )
        f.close()


address = [
    "monipe-ce-banda.rnp.br",
    "monipe-ac-banda.rnp.br",
    "monipe-am-banda.rnp.br",
    "monipe-ap-banda.rnp.br",
    "monipe-ba-banda.rnp.br",
    "monipe-df-banda.rnp.br",
    "monipe-es-banda.rnp.br",
    "monipe-go-banda.rnp.br",
    "monipe-ma-banda.rnp.br",
    "monipe-mg-banda.rnp.br",
    "monipe-ms-banda.rnp.br",
    "monipe-mt-banda.rnp.br",
    "monipe-pa-banda.rnp.br",
    "monipe-pb-banda.rnp.br",
    "monipe-pe-banda.rnp.br",
    "monipe-pi-banda.rnp.br",
    "monipe-pr-banda.rnp.br",
    "monipe-rj-banda.rnp.br",
    "monipe-rn-banda.rnp.br",
    "monipe-ro-banda.rnp.br",
    "monipe-rr-banda.rnp.br",
    "monipe-rs-banda.rnp.br",
    "monipe-sc-banda.rnp.br",
    "monipe-se-banda.rnp.br",
    "monipe-sp-banda.rnp.br",
    "monipe-to-banda.rnp.br",
]
address_atraso = [
    "monipe-ce-atraso.rnp.br",
    "monipe-ac-atraso.rnp.br",
    "monipe-am-atraso.rnp.br",
    "monipe-ap-atraso.rnp.br",
    "monipe-ba-atraso.rnp.br",
    "monipe-df-atraso.rnp.br",
    "monipe-es-atraso.rnp.br",
    "monipe-go-atraso.rnp.br",
    "monipe-ma-atraso.rnp.br",
    "monipe-mg-atraso.rnp.br",
    "monipe-ms-atraso.rnp.br",
    "monipe-mt-atraso.rnp.br",
    "monipe-pa-atraso.rnp.br",
    "monipe-pb-atraso.rnp.br",
    "monipe-pe-atraso.rnp.br",
    "monipe-pi-atraso.rnp.br",
    "monipe-pr-atraso.rnp.br",
    "monipe-rj-atraso.rnp.br",
    "monipe-rn-atraso.rnp.br",
    "monipe-ro-atraso.rnp.br",
    "monipe-rr-atraso.rnp.br",
    "monipe-rs-atraso.rnp.br",
    "monipe-sc-atraso.rnp.br",
    "monipe-se-atraso.rnp.br",
    "monipe-sp-atraso.rnp.br",
    "monipe-to-atraso.rnp.br",
]
# 6 months
for i in range(len(address)):
    print(i)
    for j in range(i + 1, len(address)):
        request_traceroute(
            "datasets traceroute/",
            "traceroute",
            address_atraso[i],
            address_atraso[j],
            "trace",
            "15552000",
        )
        request_traceroute(
            "datasets traceroute/",
            "traceroute",
            address_atraso[j],
            address_atraso[i],
            "trace",
            "15552000",
        )
        request(
            "datasets vazao/cubic/",
            "cubic",
            address[i],
            address[j],
            "throughput",
            "15552000",
        )
        request(
            "datasets vazao/cubic/",
            "cubic",
            address[j],
            address[i],
            "throughput",
            "15552000",
        )
        request(
            "datasets vazao/bbr/",
            "bbr",
            address[i],
            address[j],
            "throughput",
            "15552000",
            "10000000000",
        )
        request(
            "datasets vazao/bbr/",
            "bbr",
            address[j],
            address[i],
            "throughput",
            "15552000",
            "10000000000",
        )
        request_atraso(
            "datasets atraso/",
            "atraso",
            address_atraso[i],
            address_atraso[j],
            "latencybg",
            "15552000",
            "histogram-owdelay",
        )
        request_atraso(
            "datasets atraso/",
            "atraso",
            address_atraso[j],
            address_atraso[i],
            "latencybg",
            "15552000",
            "histogram-owdelay",
        )
    print("Step {} of {}".format(i, len(address_atraso) - 1))
