
import time
import os
class Logger:

    def __init__(self, file_name = "logs.txt"):
        self.file_name = file_name
        self.script_dir = os.path.dirname(os.path.abspath(__file__))

    def _write(self, level: str, msg: str):
        ts = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        line = f"{ts} | {level.upper():<5} | {msg}\n"
        with open( self.script_dir + os.sep +  self.file_name, "a", encoding="utf-8") as f:
            f.write(line)

    def info(self, msg: str):
        self._write("INFO", msg)

    def warning(self, msg: str):
        self._write("WARN", msg)

    def error(self, msg: str):
        self._write("ERROR", msg)
