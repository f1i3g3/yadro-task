import xml.etree.ElementTree as ET
from xml.dom import minidom


class XMLConfigWriter:
    @staticmethod
    def __find_class(class_name, classes_list):
        return next((item for item in classes_list if item["class"] == class_name), None)

    @staticmethod
    def __build_xml_element(class_name, classes_list, parent_element=None):
        class_info = XMLConfigWriter.__find_class(class_name, classes_list)
        if not class_info:
            return None

        # If parent element is None, then it is root
        element = ET.Element(class_name) if parent_element is None else ET.SubElement(parent_element, class_name)

        for param in class_info.get("parameters", []):
            if param["type"] == "class":
                XMLConfigWriter.__build_xml_element(param["name"], classes_list, element)
            else:
                param_element = ET.SubElement(element, param["name"])
                param_element.text = param["type"]

        if not class_info.get("parameters"):  # <tag> </tag>
            element.text = " "

        return element

    @staticmethod
    def write_xml_config(classes_list, config_path):
        root = next(item for item in classes_list if item.get("isRoot") == "true")  # Assuming there is one root
        xml_root = XMLConfigWriter.__build_xml_element(root["class"], classes_list)

        xml_str = ET.tostring(xml_root, encoding="utf-8").decode()
        pretty_xml = '\n'.join(minidom.parseString(xml_str).toprettyxml(indent="  ").split('\n')[1:])
        with open(config_path, "w", encoding="utf-8") as file:
            file.write(pretty_xml)
