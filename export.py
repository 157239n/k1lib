#!/usr/bin/env python3

import json, fire, os
os.chdir(os.path.dirname(os.path.realpath(__file__)))

def export(nb:str) -> None:
    """
    Exports cells in a notebook that has the "#export" tab in the first line into
    a regular python file. If `filename` is not given, will take the file name of
    the notebook. The root directory will always be that of the klib library.
    """
    answer = ["# AUTOGENERATED FILE! PLEASE DON'T EDIT"]
    stub = f"k1lib"
    #filename = f"{stub}/{filename or nb.split('/')[-1].replace('.ipynb', '.py')}"
    print(f"Current dir: {os.getcwd()}, {__file__}")
    #print(f"File: {filename}")
    for cell in json.loads(open(f"{stub}/{nb}.ipynb").read())["cells"]:
        if cell["cell_type"] != "code": continue
        source = cell["source"]
        if len(source) <= 0: continue
        if not source[0].startswith("#export"): continue
        answer.append("".join(source[1:]))
    with open(f"{stub}/{nb}.py", 'w+') as f: f.write("\n".join(answer))
    os.system("rm -r build dist k1lib.egg-info __pycache__")
    os.system("pip uninstall -y k1lib")
    os.system(f"./setup.py install")

if __name__ == "__main__": fire.Fire(export)