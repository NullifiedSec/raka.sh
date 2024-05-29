import sys
import os
from pathlib import Path
class Shell:
    def __init__(self):
        self.builtins = {
            "echo": self.shell_echo,
            "exit": self.shell_exit,
            "type": self.shell_type,
            "pwd": self.shell_pwd,
            "cd": self.shell_cd,
        }
    def shell_echo(self, args):
        print(" ".join(args))
    def shell_exit(self, args):
        try:
            exit_code = int(args[0]) if args else 0
        except ValueError:
            exit_code = 0
        sys.exit(exit_code)
    def shell_type(self, args):
        if not args:
            return
        command = args[0]
        if command in self.builtins:
            print(f"{command} is a shell builtin")
        elif command_path := self.find_command_in_path(command):
            print(f"{command} is {command_path}")
        else:
            print(f"{command} not found")
    def find_command_in_path(self, command):
        path_dirs = os.environ.get("PATH", "").split(os.pathsep)
        for dir in path_dirs:
            potential_path = os.path.join(dir, command)
            if os.path.isfile(potential_path) and os.access(potential_path, os.X_OK):
                return potential_path
        return None
    def executable_exists(self, path):
        p = Path(path)
        if p.exists():
            return p.as_posix()
        return None
    def shell_pwd(self, args=None):
        print(f"{os.getcwd()}")
    def shell_cd(self, args):
        directory = args[0]
        try:
            os.chdir(os.path.expanduser(directory))
        except OSError:
            print(f"cd: {directory}: No such file or directory")
    def execute_command(self, command_line):
        parts = command_line.split()
        if not parts:
            return
        cmd_name = parts[0]
        cmd_args = parts[1:]
        if cmd_name in self.builtins:
            self.builtins[cmd_name](cmd_args)
        elif "_exe" in cmd_name:
            if location := self.executable_exists(self.find_command_in_path(cmd_name)):
                try:
                    with os.popen(f"{location} {cmd_args[0]}") as _exec:
                        sys.stdout.write(_exec.read())
                except Exception as e:
                    sys.stdout.write(f"Failed with Error: {e}")
        else:
            print(f"{cmd_name}: command not found")
    def run(self):
        while True:
            sys.stdout.write("$ ")
            sys.stdout.flush()
            try:
                command_line = input().strip()
                self.execute_command(command_line)
            except (EOFError, KeyboardInterrupt):
                print()
                break
if __name__ == "__main__":
    shell = Shell()
    shell.run()