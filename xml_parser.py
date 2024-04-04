import xml.etree.ElementTree as ET

def parse_xml_file(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    popular_names = []
    for entry in root.findall('.//popular-name-table-entry'):
        name_data = {}
        name_data['popular_name'] = entry.find('popular-name').text if entry.find('popular-name') is not None else ''
        name_data['cite'] = entry.find('cite').text if entry.find('cite') is not None else ''
        name_data['short_title'] = entry.find('short-title-ref').get('usckey') if entry.find('short-title-ref') is not None else ''
        popular_names.append(name_data)

    return popular_names