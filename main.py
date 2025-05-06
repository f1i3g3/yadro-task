import os.path

from XMLConfigWriter import XMLConfigWriter
from XMLToJSONParser import XMLToJSONParser


if __name__ == '__main__':
    input_path = os.path.join("input", "test_input.xml")

    dataList = XMLToJSONParser.get_from_xml(input_path)

    meta_path = os.path.join("out", "meta.json")
    XMLToJSONParser.write_to_json(dataList, meta_path)

    config_path: str = os.path.join("out", "config.xml")
    XMLConfigWriter.write_xml_config(dataList, config_path)
    # TODO: aggregation check, classes storage, output generation
    # JSON - probably initially

    print('Done!')

