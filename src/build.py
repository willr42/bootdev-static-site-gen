import os
from pathlib import Path
import shutil


def build_output_dir(inp: Path, out: Path):
    clear_dir(out)
    recursive_copy(inp, out)
    return


def clear_dir(p: Path):
    if p.exists():
        shutil.rmtree(p)
    os.mkdir(p)


def recursive_copy(inp: Path, out: Path):
    for res in inp.iterdir():
        inp_fp = res.relative_to(inp)
        out_fp = Path(out, inp_fp)
        print(f"processing {res}")
        if os.path.isfile(res):
            print(f"copying {inp_fp} to {out_fp}")
            shutil.copy(res, out_fp)
        if os.path.isdir(res):
            print(f"making dir at {out_fp}")
            out_fp.mkdir()
            recursive_copy(Path(inp, res), out_fp)
