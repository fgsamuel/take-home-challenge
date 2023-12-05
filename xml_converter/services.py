import xml.etree.ElementTree as ET


def _get_recursive_element_value(element):
    if len(element) == 0:
        return {element.tag: element.text or ""}

    result = {element.tag: []}

    for child_element in element:
        result[element.tag].append(_get_recursive_element_value(child_element))

    return result


def parse_xml_string(xml_string):
    root = ET.fromstring(xml_string)
    return _get_recursive_element_value(root)
