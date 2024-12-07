import zipfile


class VirtualFileSystem:
    def __init__(self, zip_path):
        self.zip_path = zip_path
        self.file_system = {}
        self.current_dir = '.'
        self.load_files()

    def load_files(self):
        with zipfile.ZipFile(self.zip_path, 'r') as zip_ref:
            self.file_system['.'] = []
            for file_info in zip_ref.infolist():
                file = ''
                if file_info.filename.count('/') == 0:
                    self.file_system['.'].append(file_info.filename)
                    continue
                if file_info.filename[-1] != '/':
                    file = file_info.filename.split('/')[-1]
                path_parts = file_info.filename.split('/')[:-1]

                current = '.'
                for part in path_parts:
                    if part not in self.file_system:
                        self.file_system[part] = []
                    if part not in self.file_system[current]:
                        self.file_system[current].append(part)
                    current = part
                if file:
                    self.file_system[current].append(file)

    def execute_command(self, command):
        args = command.strip().split()
        if not args:
            return

        cmd = args[0]
        if cmd == 'ls':
            current_dir = self.current_dir
            if len(args) == 2:
                self.cd(args[1])
            self.ls()
            self.current_dir = current_dir
        elif cmd == 'cd':
            if len(args) == 2:
                self.cd(args[1])
        elif cmd == 'touch':
            if len(args) < 2:
                print('touch: missing file operand')
            else:
                self.touch(args[1])
        elif cmd == 'mv':
            if len(args) < 3:
                print('Usage: mv <source> <destination>')
            else:
                self.mv(args[1], args[2])
        elif cmd == 'exit':
            print('Exiting...')
            exit()
        else:
            print(f"Unknown command: {cmd}")

    def ls(self):
        print(' '.join(self.file_system[self.current_dir.split('/')[-1]]))

    def cd(self, args):
        dir_path = [i for i in args.split('/') if i != '']
        start_current = self.current_dir
        while dir_path:
            current = dir_path[0]
            if current == '..':
                if self.current_dir.count('/') != 0:
                    if self.current_dir.count('/') == 1:
                        self.current_dir = '.'
                    else:
                        self.current_dir = '/'.join(self.current_dir.split('/')[:-1])
            elif current != '.':
                if current in self.file_system[self.current_dir.split('/')[-1]]:
                    if self.current_dir == '.':
                        self.current_dir = ''
                    self.current_dir += '/' + current
                else:
                    print(f"Directory {args} does not exist")
                    self.current_dir = start_current
                    return
            dir_path = dir_path[1:]

    def touch(self, filename):
        current_dir = self.current_dir
        if filename.count('/') != 0:
            self.cd('/'.join(filename.split('/')[:-1]))
            filename = filename.split('/')[-1]
        if filename not in self.file_system[self.current_dir.split('/')[-1]]:
            self.file_system[self.current_dir.split('/')[-1]].append(filename)
        self.current_dir = current_dir

    def mv(self, filename, new_path):
        old_path = '.'
        if filename.count('/') != 0:
            old_path = '/'.join(filename.split('/')[:-1])
            filename = filename.split('/')[-1]
        current_dir = self.current_dir
        self.cd(old_path)
        try:
            i = self.file_system[self.current_dir.split('/')[-1]].index(filename)
            self.file_system[self.current_dir.split('/')[-1]].pop(i)
            self.current_dir = current_dir
            self.touch((new_path + '/' + filename).replace('//', '/'))
        except Exception as e:
            print('No such file.')
            self.current_dir = current_dir


if __name__ == "__main__":
    vfs = VirtualFileSystem("vfs.zip")

    with open("start.sh", 'r') as script_file:
        commands = [i.strip() for i in script_file.readlines()]
        for command in commands:
            vfs.execute_command(command)

    while True:
        current_dir = vfs.current_dir if vfs.current_dir != '.' else ''
        command = input(f"computer@user:~{current_dir}$ ")
        vfs.execute_command(command)
