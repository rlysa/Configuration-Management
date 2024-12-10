import pytest
from assembler import Assembler


@pytest.fixture
def setup_files(tmp_path):
    asm_file = tmp_path / "test.asm"
    bin_file = tmp_path / "test.bin"
    log_file = tmp_path / "test_log.xml"
    return asm_file, bin_file, log_file


def test_load(setup_files):
    asm_file, bin_file, log_file = setup_files
    asm_file.write_text("LOAD 104 920\n")
    assembler = Assembler(str(asm_file), str(bin_file), str(log_file))
    assembler.assemble()
    with open(bin_file, "rb") as f:
        assert f.read() == bytes([0x68, 0xCC, 0x01, 0x00])


def test_read(setup_files):
    asm_file, bin_file, log_file = setup_files
    asm_file.write_text("READ 45 255\n")
    assembler = Assembler(str(asm_file), str(bin_file), str(log_file))
    assembler.assemble()
    with open(bin_file, "rb") as f:
        assert f.read() == bytes([0xAD, 0x7F, 0x00, 0x00])


def test_write(setup_files):
    asm_file, bin_file, log_file = setup_files
    asm_file.write_text("WRITE 8\n")
    assembler = Assembler(str(asm_file), str(bin_file), str(log_file))
    assembler.assemble()
    with open(bin_file, "rb") as f:
        assert f.read() == bytes([0x08, 0x00, 0x00, 0x00])


def test_sum(setup_files):
    asm_file, bin_file, log_file = setup_files
    asm_file.write_text("SUM 91 339\n")
    assembler = Assembler(str(asm_file), str(bin_file), str(log_file))
    assembler.assemble()
    with open(bin_file, "rb") as f:
        assert f.read() == bytes([0xDB, 0xA9, 0x00, 0x00])
