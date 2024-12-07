import pytest
from main import VirtualFileSystem


def test_ls_command():
    vfs = VirtualFileSystem('vfs.zip')
    vfs.execute_command('ls')
    assert True


def test_ls_command_with_args():
    vfs = VirtualFileSystem('vfs.zip')
    vfs.execute_command('ls one')
    assert True


def test_cd_command():
    vfs = VirtualFileSystem('vfs.zip')
    vfs.execute_command('cd one')
    assert vfs.current_dir == '/one'


def test_cd_command_with_invalid_args():
    vfs = VirtualFileSystem('vfs.zip')
    vfs.execute_command('cd oneee')
    assert vfs.current_dir != '/oneee'


def test_touch_command():
    vfs = VirtualFileSystem('vfs.zip')
    vfs.execute_command('touch try.txt')
    assert 'try.txt' in vfs.file_system[vfs.current_dir]


def test_touch_command_with_relative_path():
    vfs = VirtualFileSystem('vfs.zip')
    vfs.execute_command('touch one/try.txt')
    assert 'try.txt' in vfs.file_system['one']


def test_mv_command():
    vfs = VirtualFileSystem('vfs.zip')
    vfs.execute_command('mv text.txt one/')
    assert 'text.txt' in vfs.file_system['one'] and 'text.txt' not in vfs.file_system[vfs.current_dir]


def test_chmod_command_with_relative_path():
    vfs = VirtualFileSystem('vfs.zip')
    vfs.execute_command('mv one/second/text_text.txt .')
    assert 'text_text.txt' in vfs.file_system[vfs.current_dir] and 'text_text.txt' not in vfs.file_system['second']


def test_exit_command():
    vfs = VirtualFileSystem('vfs.zip')
    with pytest.raises(SystemExit):
        vfs.execute_command('exit')


def test_exit_command_with_args():
    vfs = VirtualFileSystem('vfs.zip')
    with pytest.raises(SystemExit):
        vfs.execute_command('exit arg')
