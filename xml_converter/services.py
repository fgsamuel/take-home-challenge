import logging
import xml.etree.ElementTree as ET

from xml_converter.exceptions import XMLConverterError

logger = logging.getLogger(__name__)


def _get_recursive_element_value(element):
    if len(element) == 0:
        return {element.tag: element.text or ""}

    result = {element.tag: []}

    for child_element in element:
        result[element.tag].append(_get_recursive_element_value(child_element))

    return result


def parse_xml_string(xml_string):
    try:
        root = ET.fromstring(xml_string)
        return _get_recursive_element_value(root)
    except Exception:
        logger.exception("Error parsing XML", exc_info=True)
        raise XMLConverterError("Invalid XML")
