import os.path

from src.XMLConfigWriter import XMLConfigWriter
from src.XMLToJSONParser import XMLToJSONParser


if __name__ == '__main__':
    input_path = os.path.join("input", "test_input.xml")

    dataList = XMLToJSONParser.get_from_xml(input_path)

    meta_path = os.path.join("out", "meta.json")
    XMLToJSONParser.write_to_json(dataList, meta_path)

    config_path: str = os.path.join("out", "config.xml")
    XMLConfigWriter.write_xml_config(dataList, config_path)
