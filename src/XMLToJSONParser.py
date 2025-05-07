import json
import xml.etree.ElementTree as ET


class XMLToJSONParser:
    INF_FLAG = -2
    MISSING_FLAG = -1

    @staticmethod
    def __parse_number(num_str):
        if num_str == "*":
            return XMLToJSONParser.INF_FLAG  # inf flag
        try:
            return int(num_str)
        except ValueError:
            raise ValueError("Error during parser number")

    @staticmethod
    def __parse_multiplicity(mul_str):
        if not mul_str:
            raise ValueError("Parsing multiplicity error")

        if ".." in mul_str:
            vals = mul_str.split("..")
            if len(vals) != 2:
                raise ValueError("Parsing .. error")

            min_val = XMLToJSONParser.__parse_number(vals[0])
            max_val = XMLToJSONParser.__parse_number(vals[1])

            # Assuming 1..1, 2..1 and *..1 as incorrect formats
            if min_val < 0 or ((max_val == XMLToJSONParser.INF_FLAG) and (min_val == max_val)):
                raise ValueError("Incorrect first value")
            elif max_val < 0:
                raise ValueError("Incorrect second value")
            elif min_val < max_val or max_val == XMLToJSONParser.INF_FLAG:
                return min_val, max_val  # right case
            else:
                raise ValueError("Incorrect borders")

        num = XMLToJSONParser.__parse_number(mul_str)
        if num < 0:
            raise ValueError("Incorrect value")

        return num, XMLToJSONParser.MISSING_FLAG

    @staticmethod
    def get_from_xml(path):
        try:
            doc = ET.parse(path)
            root = doc.getroot()

            classes_list = []

            for class_el in root.findall('Class'):
                class_entry = {
                    "class": class_el.attrib['name'],
                    "documentation": class_el.attrib['documentation'],
                    "isRoot": class_el.attrib['isRoot'],
                    "parameters": [{"name": attr.attrib['name'], "type": attr.attrib['type']}
                                   for attr in class_el.findall('Attribute')]
                }

                classes_list.append(class_entry)

            for aggregation_el in root.findall('Aggregation'):
                sourceMul = aggregation_el.attrib['sourceMultiplicity']
                targetMul = aggregation_el.attrib['targetMultiplicity']

                source_min, source_max = XMLToJSONParser.__parse_multiplicity(sourceMul)
                target_min, target_max = XMLToJSONParser.__parse_multiplicity(targetMul)
                if target_min != 1 or target_max != XMLToJSONParser.MISSING_FLAG:
                    raise ValueError("Many-to-many is not supported")

                for class_l in classes_list:
                    # TODO: check classes for existing ?
                    if class_l["class"] == aggregation_el.attrib['target']:
                        class_l["parameters"].append({"name": aggregation_el.attrib['source'], "type": "class"})

                    if class_l["class"] == aggregation_el.attrib['source']:
                        class_l["min"] = source_min
                        if source_max != XMLToJSONParser.INF_FLAG:
                            if source_max == XMLToJSONParser.MISSING_FLAG:
                                source_max = source_min
                            class_l["max"] = source_max

            return classes_list
        except Exception as e:
            raise e

    @staticmethod
    def write_to_json(result, path):
        with open(path, 'w', encoding='utf-8') as file:
            json.dump(result, file, ensure_ascii=False, indent=4)
