from movement_main_func import *
from get_hbl_specs import *
from api_shippter_ops import *

ROI = "ROI M128380"
HBL = "BL/ROI M128380.pdf"
SHIPPTER_RUT = '76507313-8'
SHIPPTER_NAME = 'SHIPPTER SPA'

shippter_path = Path(resource_path("data/rod_op.json"))


rod = limpiar_base(get_shippter_quotes(shippter_path))


roi_info = create_roi_dictionary(rod, ROI)
emission_date = get_emission_date(HBL)
marks_description = get_marks_description(HBL)
main_stats = get_main_stats(HBL)
containers_info = get_containers_info(HBL)


def rellenar_sidemar():
    search_reference(roi_info["mblCode"])
    fill_header_info(roi_info["blCode"])
    fill_emission_date(emission_date)
    fill_shippter_info(SHIPPTER_NAME, SHIPPTER_RUT)
    fill_location_info(roi_info["origin"], roi_info["origin_name"],
                       roi_info["destination"], roi_info["dest_name"])
    #fill cnee and shipper info

    add_main_item(marks_description["marks"], roi_info["bultos"], roi_info["tipo_bulto"],
                  marks_description["description"], main_stats["main_weight"], main_stats["main_volume"])
    add_containers_info(containers_info, roi_info["shippingCompany2"])

def main():
    login()
    rellenar_sidemar()

if __name__ == "__main__":
    print("")
    main()