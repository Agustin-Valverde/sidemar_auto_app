import requests
import json
from pathlib import Path
import pandas as pd
from pprint import pprint
import numpy as np
from datetime import datetime, date, timedelta
import os
from collections import defaultdict

origin_name_dict = defaultdict(lambda: "NA",{
    "CNSGH": "Shanghai",
    "CNXGA": "Xingang",
    "CNSNZ": "Shenzhen",
    "CNNGB": "Ningbo",
    "CNXAM": "Xiamen",
    "CNQIN": "Qingdao",
    "CNSHK": "Shekou",
    "CNGGZ": "Guangzhou",
    "CNYTN": "Yantian",
    "HKHKG": "Hong Kong"
})

dest_name_dict = defaultdict(lambda: "NA",{
    "CLSAI": "San Antonio",
    "CLCNL": "Coronel",
    "CLSVE": "San Vicente",
    "CLVAP": "Valparaiso",
    "CLTAL": "Talcahuano",
    "CLLQN": "Lirquen"
})



# Funcion para llamar a la API
def create_shippter_doc(shippter_path):
    """"Calls ROD api and creates json file to path"""

    TODAY = date.today()
    SECRET = "shippter2021"
    url = "https://us-west-2.aws.data.mongodb-api.com/app/application-0-yrtca/endpoint/"
    url += f"quotes/details?secret={SECRET}&from={TODAY - timedelta(days=6*30)}"
    url += f"&to{TODAY}"

    print("Iniciado lectura de datos, esto puede tomar un momento...")

    r = requests.get(url)
    print(r.status_code)
    
    response_dict = r.json()

    response_json = json.dumps(response_dict)

    shippter_path.write_text(response_json) 
    print("Listo!")

def get_creation_time(path):
    """Gets the creation time of ROD"""

    creation_time = os.stat(path).st_mtime
    print(f"El ROD esta actualizado para el {datetime.fromtimestamp(creation_time):%d-%m-%Y}")


def get_shippter_quotes(shippter_path):
    """Reads ROD Json and retrieves quotes dataframe"""

    contents = shippter_path.read_text()
    info = json.loads(contents)

    quotes = info["quotes"]
    quotes_dataframe = pd.DataFrame(quotes)

    return quotes_dataframe

## Funciones transformar

def update_MBL(row):
    # Manejar NaN en 'shippingCompany2'
    if pd.isna(row['shippingCompany2']):
        row['shippingCompany2'] = " "
    # Manejar NaN en 'mblCode'
    if pd.isna(row['mblCode']):
        row['mblCode'] = " "
    
    if row['shippingCompany2'] == 'CMDU':
        return row['mblCode']
    elif row['shippingCompany2'] in row['mblCode']:
        return row['mblCode']
    else:
        return row['shippingCompany2'] + row['mblCode']

def update_origin(valor):
    if valor == "CNSZN":
        return "CNSZN"
    elif valor == "CNSHA":
        return "CNSGH"
    elif valor == "CNTXG":
        return "CNXGA"
    elif valor == "CNXMN":
        return "CNXAM"
    elif valor == "CNTAO":
        return "CNQIN"
    elif valor == "CNGZG":
        return "CNGGZ"
    else:
        return valor

def limpiar_base(base_1):
    """Cleans ROD and keeps only specific columns for SIDEMAR"""

    print("Empezando limpieza de ROD...")

    base_limpia = (
        base_1[~base_1["isSaas"]]
        .fillna({col: 0 for col in ["Container 20' ST", "Container 40' HC", "Container 40' ST", "Container 40' NOR"]})
        .assign(
            tipo_bulto ="73",
            shippingCompany2 =base_1["shippingCompany2"].apply(lambda x: 'EGLV' if x == 'EVRG' else x),
            blCode = "(H)" + base_1["blCode"],
            bultos = lambda x: (x["Container 20' ST"] + x["Container 40' HC"] + x["Container 40' ST"] + x["Container 40' NOR"]).astype(int),
            origin = base_1["origin"].apply(update_origin)
            )
        .assign(
            tipo_bulto=lambda x: x["tipo_bulto"].where(x["Container 40' NOR"] != 0, "76"),
            mblCode = base_1.apply(update_MBL, axis = 1),
            origin_name = lambda x: x["origin"].map(origin_name_dict),
            dest_name = base_1["destination"].map(dest_name_dict)
                        )
        .assign(
            tipo_bulto=lambda x: x["tipo_bulto"].where((x["Container 40' HC"] != 0) | (x["Container 40' HC"] != 0), "74")
        )
        .astype({"bultos": "str"})
        [["roi", "clientRut", "client", "blCode", "mblCode", "shippingCompany2", "origin", "destination", "tipo_bulto",
          "bultos", "origin_name", "dest_name"]]
                )
    print(base_limpia.columns) 

    return base_limpia


def create_roi_dictionary(base, roi):
    """Creates SIDEMAR dicctionary for a specific ROI"""

    dict_roi = (base
                .query(f"roi == '{roi}'")
                ).to_dict(orient='records')
    
    if isinstance(dict_roi, list):
        dict_roi = dict_roi[0]
        
    print(dict_roi)
    return dict_roi
    

if __name__ == "__main__":

    import time
    shippter_path = Path("data/rod_op.json")

    start_time = time.time()
    create_shippter_doc(shippter_path)
    end_time = time.time()
    print(f"Create json = {end_time - start_time}")

    get_creation_time(shippter_path)

    rod = get_shippter_quotes(shippter_path)
    rod_clean = limpiar_base(rod)
    create_roi_dictionary(rod_clean, "ROI M128219")




