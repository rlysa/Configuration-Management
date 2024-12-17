import argparse
import re
import sys
import xml.etree.ElementTree as ET
import xml.dom.minidom


class SyntaxErrorException(Exception):
    pass


class ConfigParser:
    def __init__(self):
        self.constants = {}
        self.dictionaries = {}

    def parse(self, input_text):
        self.check_syntax(input_text)
        self.parse_multiline_comments(input_text)
        self.parse_let_statements(input_text)
        self.parse_dictionaries(input_text)

    def check_syntax(self, text):
        let_pattern = r'let\s+([a-zA-Z][a-zA-Z0-9]*)\s*=\s*([^;\n]*)'
        for line_num, line in enumerate(text.splitlines(), 1):
            if 'let' in line and not re.search(let_pattern, line):
                raise SyntaxErrorException(f"Синтаксическая ошибка: строка {line_num}: {line.strip()}")

    def parse_multiline_comments(self, text):
        return re.sub(r'=begin.*?=end', '', text, flags=re.DOTALL)

    def parse_let_statements(self, text):
        let_pattern = r'let\s+([a-zA-Z][a-zA-Z0-9]*)\s*=\s*(.+)'
        for match in re.finditer(let_pattern, text):
            name, value = match.groups()
            self.constants[name] = self.parse_value(value.strip())

    def parse_dictionaries(self, text):
        dict_pattern = r'\{\s*((?:[a-zA-Z][a-zA-Z0-9]*\s*->\s*.*?\s*\.?)+)\s*\}'
        for match in re.finditer(dict_pattern, text):
            dict_content = match.group(1)
            dictionary = {}
            dict_content = [i.strip() for i in dict_content.split('.') if i.strip() != '']
            for item in dict_content:
                key_value = item.split('->')
                if len(key_value) != 2:
                    raise SyntaxErrorException(f"Некорректное определение словаря: {item.strip()}")
                key, value = key_value
                dictionary[key.strip()] = self.parse_value(value.strip())
            self.dictionaries[match.start()] = dictionary

    def parse_value(self, value):
        if re.match(r"^\d+$", value):
            return int(value)
        elif re.match(r'^\[\[(.* )\]\]$', value):
            return value[3:-3]
        elif value in self.constants:
            return self.constants[value]
        elif value.startswith('{'):
            return self.parse_dictionaries(value)
        elif value.startswith('!(') and value.endswith(')'):
            values = value[2:-1].split()
            for i in range(0, 2):
                if values[i] in self.constants:
                    values[i] = self.constants[values[i]]
                elif values[i].isnumeric():
                    values[i] = float(values[i])
                else:
                    raise ValueError(f"Неизвестное значение: {value}")
            if len(values) == 3:
                if values[-1] == "pow()":
                    return pow(values[0], values[1])
                elif values[-1] == "+":
                    return values[0] + values[1]
                elif values[-1] == "-":
                    return values[0] - values[1]
                elif values[-1] == "*":
                    return values[0] * values[1]
            elif len(values) == 2 and values[-1] == "chr()":
                return chr(values[0])
            else:
                raise ValueError(f"Неизвестное значение: {value}")
        else:
            raise ValueError(f"Неизвестное значение: {value}")

    def to_xml(self):
        root = ET.Element("Configuration")
        if self.constants.items():
            constants_element = ET.SubElement(root, "Constants")
            for name, value in self.constants.items():
                constant_element = ET.SubElement(constants_element, "Constant", name=name)
                constant_element.text = str(value)

        if self.dictionaries.items():
            dictionaries_element = ET.SubElement(root, "Dictionaries")
            for dictionary, items in self.dictionaries.items():
                dict_element = ET.SubElement(dictionaries_element, "Dictionary")
                for key, value in items.items():
                    item_element = ET.SubElement(dict_element, "Item", key=key)
                    item_element.text = str(value)
        log_data = ET.tostring(root, encoding='unicode')
        dom = xml.dom.minidom.parseString(log_data)
        log = f"<?xml version=\"1.0\" encoding=\"utf-8\"?>\n" + dom.toprettyxml(newl="\n")[23:]
        return log


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Парсинг конфигурационного языка в XML.')
    parser.add_argument('file_input', help='Путь к входному файлу с конфигурацией')
    args = parser.parse_args()

    try:
        with open(args.file_input, 'r') as f:
            input_text = f.read()

        config_parser = ConfigParser()
        config_parser.parse(input_text)
        xml_output = config_parser.to_xml()
        print(xml_output)

    except SyntaxErrorException as e:
        sys.stderr.write(f"Ошибка: {e}\n")
        exit(1)

    except Exception as e:
        sys.stderr.write(f"Неизвестная ошибка: {e}\n")
        exit(1)
