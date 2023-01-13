import os
from os.path import sep

if __name__ == "__main__":
    if not os.getcwd().split(sep)[-1] == "docs":
        try:
            os.chdir("docs")
        except FileNotFoundError:
            print("docs folder not found")

    os.system(
        "pdoc3 --html --config latex_math=True --output-dir . .." + sep + "PyFrame")

    print(os.getcwd().split(sep)[-1])

    for file in os.listdir("PyFrame"):
        os.replace(os.getcwd() + sep + "PyFrame" +
                  sep + file, os.getcwd() + sep + file)

    os.rmdir("PyFrame")
    os.chdir("..")
    
    print(os.getcwd().split(sep)[-1])
