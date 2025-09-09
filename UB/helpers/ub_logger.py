
import time
import os
from operator import truediv


class Logger:

    def __init__(self, file_name = "logs.txt" , path = "./UB/logs/"):
        file_name = os.path.basename(file_name).replace(".csv", ".log")
        self.file_name = file_name
        self.path = path
        self.has_writen = False

    def _write(self, level: str, msg: str):
        ts = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        line = f"{ts} | {level.upper():<5} | {msg}\n"

        file_path = self.path + os.sep + self.file_name
        with open(file_path, "a", encoding="utf-8") as f:
            f.write(line)

        if not self.has_writen:
            self.has_writen = True
            print(f"Writing logs  to {file_path}")

    def info(self, msg: str):
        self._write("INFO", msg)

    def warning(self, msg: str):
        self._write("WARN", msg)

    def error(self, msg: str):
        self._write("ERROR", msg)
