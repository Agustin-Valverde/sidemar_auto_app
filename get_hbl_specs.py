from pathlib import Path
import re
import fitz
import pprint 
import get_hbl_paths
from datetime import datetime


def make_text(words):

    """
    Return textstrings output of get_text("words")
    words return a list of tuples, where each tuple look like
    (x0, y0, x1, y1, 'string', 'blocknumber', 'linenumber', 'wordnumber')
    Word items are sorted for reading sequence left to right
    """
    line_dict = {} # key: vertical coordinate, value: list of words
    for w in words:
        coords = w[0:4]
        word = w[4] # word
        line_dict[word] = coords
    return line_dict


def get_marks_description(path):
    """Returns a dictionary with marks and description of Ivy HBL"""
    marks_coords = (30, 330, 85, 490)
    description_coords = (87, 340, 405, 470)

    hbl_path = Path(path)
    hbl_open = fitz.open(hbl_path)[0]
    marks_description_dict = {}

    marks = hbl_open.get_textbox(marks_coords)
    marks_description_dict["marks"] = marks

    description = hbl_open.get_textbox(description_coords).split("\n")
    description_filtered = [element for element in description if len(re.findall(r'/', element)) < 1]
    marks_description_dict["description"] = description_filtered

    return marks_description_dict


def get_containers_info(path):
    """
    Returns a list of dictionaries
    Each dictiony has the main info of each container
    Sometimes container info is in a bad format
    We use a try except block for those situations
    """
    container_types = {
    "40HQ": "45G0",
    "20GP": "22G0",
    "40GP": "42G0",
    "40NOR": "45R0"
    }

    containers_coords = (35, 360, 490, 550)

    hbl_path = Path(path)
    hbl_open = fitz.open(hbl_path)[0]
    containers_list_final = []

    try:
        containers_list = hbl_open.get_textbox(containers_coords).split("\n")
        containers_list_filtered = [cont for cont in containers_list if len(re.findall(r'/', cont)) > 1]
        if len(re.findall(r'/', containers_list_filtered[0])) < 4:
            containers_list_filtered = ["".join(containers_list_filtered)]

        for number, container in enumerate(containers_list_filtered):
            container_dict = {}
            container_info = container.split('/')

            container_dict["sigla"] = container_info[0][0:4]
            container_dict["numero"] = container_info[0][4:10]
            container_dict["codigo"] = container_info[0][-1]

            container_dict["sello"] = container_info[1]

            container_type = container_types.get(container_info[2]) # Usamos el diccionario de arriba para conseguir el codigo
            container_dict["tipo_cont"] = container_type


            container_dict["peso_cont"] = "".join(filter(lambda x: not x.isalpha(), container_info[4])) # Dejamos solo numeros en el peso
            containers_list_final.append(container_dict)       
    except:
        print("Error in container syntax")
        filler_dict = {
            "sigla": " ",
            "numero": " ",
            "codigo": " ",
            "tipo_cont": " ",
            "peso_cont": " "
        }
        containers_list_final.append(filler_dict)

    return containers_list_final


def get_emission_date(path):
    """Returns a list with a single value with the emission date of HBL"""
    date_coords = (45, 600, 500, 800)

    hbl_path = Path(path)
    hbl_open = fitz.open(hbl_path)[0]

    date_list = hbl_open.get_textbox(date_coords).split("\n")
    date_list_filtered = [element for element in date_list if len(re.findall(r'-', element)) == 2]
    if len(date_list_filtered) > 1:
        date_list_filtered = date_list_filtered[0]
    
    if isinstance(date_list_filtered, list):
        date_list_filtered = date_list_filtered[0]

    fecha_datetime = datetime.strptime(date_list_filtered, '%Y-%m-%d').strftime('%d-%m-%Y')
    
    return fecha_datetime


def get_main_stats(path):
    """Returns a dictionary with main weight and volume"""
    main_stats_coords = (400, 310, 560, 345)
    hbl_path = Path(path)
    hbl_open = fitz.open(hbl_path)[0]
    main_stats_dict = {}

    main_stats_list = hbl_open.get_textbox(main_stats_coords).split("\n")
    if len(list(main_stats_list)) == 1:
        main_stats_list = main_stats_list[0].split(" ")

    main_weight = str(round(float("".join(filter(lambda x: not x.isalpha(), main_stats_list[0]))), 2))
    main_volume = str(round(float("".join(filter(lambda x: not x.isalpha(), main_stats_list[1]))), 2))

    main_stats_dict["main_weight"] = main_weight
    main_stats_dict["main_volume"] = main_volume

    return main_stats_dict



path = Path("BL/FCLVY20231235  TEX.pdf")
hbl_path = Path(path)
#pprint.pprint(make_text(fitz.open(hbl_path)[0].get_text("words")))
#pprint.pprint(get_containers_info(hbl_path, CONTAINERS_COORDS))

if __name__ == "__main__":

    hbl_files = get_hbl_paths.obtain_paths_docs("BL")
    print(hbl_files)
    files_info_dict = {}

    for file in hbl_files:
        print(f"Working in {file}")
        print(f"width = {fitz.open(file)[0].rect.width}")
        print(f"height = {fitz.open(file)[0].rect.height}")
        marks_desciption_dict = get_marks_description(file)
        files_info_dict[file] = marks_desciption_dict
        pprint.pprint(marks_desciption_dict)
        pprint.pprint(get_main_stats(file))
        print(get_emission_date(file))
        pprint.pprint(get_containers_info(file), sort_dicts=False)
        print("\n")


    #pprint.pprint(files_info_dict)
