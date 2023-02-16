import pandas as pd
from camel_tools.utils.dediac import dediac_ar

class pre_process:
    def process(s):
        return "saf"

if __name__ == "__main__":
    import sys
    file = sys.argv[1]
    df = pd.read_csv(file)

    print(pre_process.process(""))