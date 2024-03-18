from movement_funcs import *
import time
from get_hbl_specs import get_containers_info


MBL = "MAEU1KT970471"
HBL = '(H)FCLVY20241279A1'
SHIPPTER_RUT = '76507313-8'
SHIPPTER_NAME = 'SHIPPTER SPA'
EMISSION_DATE = '30-01-2024'

marks_description = {'marks': 'N/M', 'description': ['32 CARTONS', 'MOVEABLE BLOWER,', 'LOW NOISE INTERMEDIATE PRESSURE BLOWER']}
main_stats = {'main_weight': '1408.0', 'main_volume': '6.24'}
tipo_bulto = "74"
bultos = "1"
containers_info = get_containers_info("BL\z_11.pdf")


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def login():
    """Looks and fills Si"""    
    get_image_coords(resource_path("sidemar_images/main_login.png"),
                      "No se encuentra el login de Sidemar")
    move_click(858, 677)
    move_click_write(935, 461, '*W2FZN9P')
    move_click(992, 676)
    get_image_coords(resource_path("sidemar_images/sidemar_main_menu.png"),
                     "Sidemar cargando...")
    print("Sidemar Listo!")


def search_reference(MBL):

    move_click(1156, 691) # Buscar Referncia
    move_click(1259, 292) # Buscar

    move_click(958, 326) # Tipo
    move_click(941, 343) # BL
    move_click(845, 360) # Especifica

    move_click_write(892, 413, MBL)
    move_click(907, 796) # Aceptar

    get_image_coords(resource_path("sidemar_images/reference/reference_pattern.png"),
                     "Elemento cargando...") # look for ref_pattern
    move_click(838, 353)
    move_click(1335, 294)
    move_click(972, 594)
    move_click(909, 560)
    move_click(1025, 584)

    get_image_coords(resource_path("sidemar_images/sidemar_main_menu.png"),
                     "Cargando Referencia...")
    print("Listo para continuar")


def fill_header_info(HBL):
    move_click_write(702, 240, HBL)
    move_click(700, 299)
    move_click(678, 325)
    move_click(991, 239)
    move_click(989, 271)


def fill_emission_date(emission_date):
    move_click(727, 519)
    pyautogui.press('tab', presses=3, interval=0.1)
    pyautogui.press('enter')
    move_click(693, 520)
    pyautogui.press('backspace', presses=10)
    pyautogui.write(emission_date)


def fill_shippter_info(shippter_rut, shippter_name):    
    coords = [
        {"x": 723, "y": 350},
        {"x": 794, "y": 341}
    ]

    for tab in coords:
        move_click(tab["x"], tab["y"])
        move_click_write(732, 386, shippter_rut)
        move_click(793, 392)
        pyautogui.press('down')
        pyautogui.press('enter')
        move_click_write(986, 388, shippter_name)


def fill_location_info(origin, origin_name, destination, dest_name):
    emission = "CNSNZ"
    emission_name = "Shenzhen"

    # PE
    move_click(1044, 492)
    move_click_write(930, 526, emission)
    move_click_write(930, 548, emission_name)
    move_click(914, 604)

    # PO
    move_click(1044, 492)
    move_click(928, 498)
    pyautogui.press('down')
    pyautogui.press('enter')
    move_click_write(930, 526, origin)
    move_click_write(930, 548, origin_name)
    move_click(914, 604)

    # PD
    move_click(1044, 492)
    move_click(928, 498)
    pyautogui.press('down', presses=2)
    pyautogui.press('enter')
    move_click_write(930, 526, destination)
    move_click_write(930, 548, dest_name)
    move_click(914, 604)


def add_main_item(marks, bultos, tipo_bulto, description, main_weight, main_volume):
    move_click(617, 151)
    move_click(590, 194)
    pyautogui.press('tab')
    pyautogui.write(marks)
    with pyautogui.hold('ctrl'):
        pyautogui.press('tab')
    pyautogui.press('tab')
    pyautogui.write(bultos)
    pyautogui.press('tab')
    pyautogui.write(tipo_bulto)
    pyautogui.press('tab', presses=2)

    for item in description:
        pyautogui.write(item)
        pyautogui.press('enter')

    with pyautogui.hold('ctrl'):
        pyautogui.press('tab')
    pyautogui.write(main_weight)
    pyautogui.press('tab', presses=2)
    pyautogui.write(main_volume)
    pyautogui.press('tab')
    pyautogui.press('down')
    pyautogui.press('tab', presses=3)
    pyautogui.press("enter")


def add_containers_info(containers_info, shippingcompany):

    ycoords_seals = (445, 464, 483, 503)
    move_click(582, 246)
    for number, container_dict in enumerate(containers_info):

        # Add new container
        move_click(973, 193)
        pyautogui.press('tab', presses=2)
        pyautogui.write(container_dict["sigla"])
        pyautogui.press('tab')
        pyautogui.write(container_dict["numero"])
        pyautogui.press('tab')
        pyautogui.write(container_dict["codigo"])
        pyautogui.press('tab')
        pyautogui.write(container_dict["tipo_cont"])
        pyautogui.press('tab', presses=2)
        pyautogui.write(container_dict["peso_cont"])
        pyautogui.press('tab', presses=2)
        pyautogui.write(shippingcompany)
        pyautogui.press(['tab', 'down', 'down', 'tab', 'enter'])

        # Add seal
        move_click(592, ycoords_seals[number])
        move_click(1297,396)
        pyautogui.press('tab', presses=3)
        pyautogui.write(container_dict["sello"])
        pyautogui.press('tab')
        pyautogui.write("CA")
        pyautogui.press('tab', presses=2)
        pyautogui.write('COMPAQUIA')
        pyautogui.press(['tab', 'enter'])

if __name__ == "__main__":
    print(f"{containers_info = }")
    add_containers_info(containers_info, "MAEU")