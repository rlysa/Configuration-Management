import argparse
import xml.etree.ElementTree as ET
import xml.dom.minidom


class Assembler:
    def __init__(self, path_to_code_file, path_to_binary_file, path_to_log_file):
        self.path_binary = path_to_binary_file
        self.path_code = path_to_code_file
        self.path_log = path_to_log_file
        self.bytes = []
        self.log_root = ET.Element("log")

    def assemble(self):
        with open(self.path_code, 'rt') as code:
            for line in code:
                line = line.split('\n')[0].strip()
                if not line: continue
                command, *args = line.split()
                match command:
                    case "LOAD":
                        if len(args) != 2:
                            raise SyntaxError(f"{line}\nУ операции \"Загрузка константы\" должно быть 2 аргумента")
                        self.bytes.append(self.load(int(args[0]), int(args[1])))
                    case "READ":
                        if len(args) != 2:
                            raise SyntaxError(f"{line}\nУ операции \"Чтение значения из памяти\" должно быть 2 аргумента")
                        self.bytes.append(self.read(int(args[0]), int(args[1])))
                    case "WRITE":
                        if len(args) != 1:
                            raise SyntaxError(f"{line}\nУ операции \"Запись значения в память\" должен быть 1 аргумент")
                        self.bytes.append(self.write(int(args[0])))
                    case "SUM":
                        if len(args) != 2:
                            raise SyntaxError(f"{line}\nУ операции \"Бинарная операция: сложение\" должно быть 2 аргумента")
                        self.bytes.append(self.sum(int(args[0]), int(args[1])))
                    case _:
                        raise SyntaxError(f"{line}\nНеизвестная операция")
        with open(self.path_binary, 'wb') as binary:
            for byte in self.bytes:
                binary.write(byte)
        log_data = ET.tostring(self.log_root, encoding="unicode", method="xml").encode()
        dom = xml.dom.minidom.parseString(log_data)
        log = f"<?xml version=\"1.0\" encoding=\"utf-8\"?>\n" + dom.toprettyxml(newl="\n")[23:]
        with open(self.path_log, 'w', encoding="utf-8") as f: f.write(log)

    def load(self, A, B):
        if A != 104: raise ValueError("Параметр А должен быть равен 104")
        if not (0 <= B < (1 << 23)): raise ValueError("Адрес B должен быть в пределах от 0 до 8388607 (2^23-1)")
        bits = (B << 7) | A
        bits = bits.to_bytes(4, byteorder="little")
        element = ET.SubElement(self.log_root, "LOAD")
        element.attrib["A"] = str(A)
        element.attrib["B"] = str(B)
        element.text = bits.hex()
        return bits

    def read(self, A, B):
        if A != 45: raise ValueError("Параметр А должен быть равен 45")
        if not (0 <= B < (1 << 21)): raise ValueError("Адрес B должен быть в пределах от 0 до 2097151 (2^21-1)")
        bits = (B << 7) | A
        bits = bits.to_bytes(4, byteorder="little")
        element = ET.SubElement(self.log_root, "READ")
        element.attrib["A"] = str(A)
        element.attrib["B"] = str(B)
        element.text = bits.hex()
        return bits

    def write(self, A):
        if A != 8: raise ValueError("Параметр А должен быть равен 8")
        bits = A
        bits = bits.to_bytes(4, byteorder="little")
        element = ET.SubElement(self.log_root, "WRITE")
        element.attrib["A"] = str(A)
        element.text = bits.hex()
        return bits

    def sum(self, A, B):
        if A != 91: raise ValueError("Параметр А должен быть равен 91")
        if not (0 <= B < (1 << 12)): raise ValueError("Адрес B должен быть в пределах от 0 до 4095 (2^12-1)")
        bits = (B << 7) | A
        bits = bits.to_bytes(4, byteorder="little")
        element = ET.SubElement(self.log_root, "SUM")
        element.attrib["A"] = str(A)
        element.attrib["B"] = str(B)
        element.text = bits.hex()
        return bits


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("asm_file", help="Входной файл (*.asm)")
    parser.add_argument("bin_file", help="Выходной файл (*.bin)")
    parser.add_argument("-l", "--log_file", help="Лог файл (*.xml)")
    args = parser.parse_args()
    assembler = Assembler(args.asm_file, args.bin_file, args.log_file)
    try:
        assembler.assemble()
        print(f"Ассемблирование выполнено успешно. Выходной файл: {args.bin_file}")
    except ValueError as error:
        print(f"Ошибка:\n{error}")
