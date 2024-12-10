import pytest
from interpreter import Interpreter


@pytest.fixture
def setup_binary_file(tmp_path):
    binary_file = tmp_path / "test.bin"
    result_file = tmp_path / "test_result.xml"
    return binary_file, result_file


def test_load(setup_binary_file):
    binary_file, result_file = setup_binary_file
    binary_file.write_bytes(bytes([0x68, 0xCC, 0x01, 0x00]))
    interpreter = Interpreter(str(binary_file), str(result_file), "0:1")
    interpreter.interpret()
    assert interpreter.stack.pop() == 920


def test_read(setup_binary_file):
    binary_file, result_file = setup_binary_file
    binary_file.write_bytes(bytes([0xAD, 0x7F, 0x00, 0x00]))
    interpreter = Interpreter(str(binary_file), str(result_file), "0:300")
    interpreter.registers[255] = 1
    interpreter.interpret()
    assert interpreter.stack.pop() == 1


def test_write(setup_binary_file):
    binary_file, result_file = setup_binary_file
    binary_file.write_bytes(bytes([0x08, 0x00, 0x00, 0x00]))
    interpreter = Interpreter(str(binary_file), str(result_file), "0:10")
    interpreter.stack.append(8)
    interpreter.interpret()
    with open(result_file, "r", encoding="utf-8") as f:
        assert "<register address=\"8\">8</register>" in f.read()


def test_sum(setup_binary_file):
    binary_file, result_file = setup_binary_file
    binary_file.write_bytes(bytes([0xDB, 0xA9, 0x00, 0x00]))
    interpreter = Interpreter(str(binary_file), str(result_file), "0:400")
    interpreter.stack.append(10)
    interpreter.registers[349] = 15
    interpreter.interpret()
    assert interpreter.stack.pop() == 25
