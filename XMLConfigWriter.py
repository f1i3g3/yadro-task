import os
import xml.etree.ElementTree as ET


class XMLConfigWriter:
    @staticmethod
    def __find_root(classes_list):  # Assuming there is one root
        for class_l in classes_list:
            if class_l["isRoot"] == "true":
                return class_l["class"]

        raise ValueError("There is no roots")

    @staticmethod
    def write_xml_config(classes_list, config_path):
        try:
            bts = ET.Element(XMLConfigWriter.__find_root(classes_list))



            ET.SubElement(bts, "id").text = "uint32"
            ET.SubElement(bts, "name").text = "string"

            mgmt = ET.SubElement(bts, "MGMT")
            metric_job = ET.SubElement(mgmt, "MetricJob")
            ET.SubElement(metric_job, "isFinished").text = "boolean"
            ET.SubElement(metric_job, "jobId").text = "uint32"

            # Пустые элементы с пробелом внутри
            cplane = ET.SubElement(mgmt, "CPLANE")
            cplane.text = " "  # Пробел вместо пустого текста

            hwe = ET.SubElement(bts, "HWE")
            ru = ET.SubElement(hwe, "RU")
            ET.SubElement(ru, "hwRevision").text = "string"
            ET.SubElement(ru, "id").text = "uint32"
            ET.SubElement(ru, "ipv4Address").text = "string"
            ET.SubElement(ru, "manufacturerName").text = "string"

            comm = ET.SubElement(bts, "COMM")
            comm.text = " "  # Пробел вместо пустого текста

            # Форматируем XML с отступами (через замену строк)
            xml_str = ET.tostring(bts, encoding="utf-8").decode()
            xml_str = xml_str.replace("<CPLANE> </CPLANE>", "<CPLANE> </CPLANE>")  # На всякий случай
            xml_str = xml_str.replace("<COMM> </COMM>", "<COMM> </COMM>")

            # Записываем в файл
            with open(config_path, "w", encoding="utf-8") as f:
                f.write(xml_str)

        except Exception as e:
            raise e
