import os
import subprocess
from difflib import SequenceMatcher


def build_tests():
    cwd = os.getcwd()
    subfolders = [f.path for f in os.scandir("tests") if f.is_dir()]
    crash = 0
    total = 0
    for folder in subfolders:
        print("-------------------")
        print(folder)
        os.chdir(folder)
        subprocess.check_call(
            "aleo build", shell=True, stdout=subprocess.DEVNULL
        )

        if os.path.isfile("build/main.avm"):
            p = subprocess.Popen(
                "python3 ../../main.py -f build/main.avm".split(" "),
                stdout=subprocess.PIPE,
            )
            f = open("main.aleo")
            content_file = f.readlines()
            content_file = "".join(content_file)
            f.close()
            output, _ = p.communicate()
            output = output.decode("utf-8")
            # print(output)
            # print("----")
            # print(content_file)
            ratio = SequenceMatcher(None, output, content_file).ratio()
            print(ratio)
            total += ratio
        else:
            crash += 1
            print("NO BUILD DIRECTORY")
        os.chdir(cwd)
    print("-------------------------------------------------")
    print(f"Folder that does not build : {crash}")
    print(f"RATIO -- {total/(len(subfolders) - crash)}")


build_tests()
