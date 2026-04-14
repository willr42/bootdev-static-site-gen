from os import getcwd
from pathlib import Path

from build import build_output_dir


def main():
    cwd = getcwd()
    inp_path = Path(cwd, "static")
    out_path = Path(cwd, "public")
    build_output_dir(inp_path, out_path)


main()
