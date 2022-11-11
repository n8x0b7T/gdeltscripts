import time
# import csv
from googletrans import Translator
import argparse
import random
import pandas as pd
from alive_progress import alive_bar
from concurrent.futures import ThreadPoolExecutor, as_completed


parser = argparse.ArgumentParser()
parser.add_argument('-i',
                    '--input', help='CSV of extracted websites',  required=True)
parser.add_argument('-o',
                    '--output',  help='where to write output')
parser.add_argument('--no-filter-lang', default=False, action='store_true')
args = parser.parse_args()

translator = Translator(
    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0')

accepted_lang = 'ar'


def translate_text(row):
    # time.sleep(.5)
    try:
        t = translator.translate(f"{row['title']}>>>>{row['body']}", dest='en')
        split = t.text.split('>>>>')

        row['body_tr'] = split[-1]
        row['title_tr'] = split[0]

        if t.src == accepted_lang and not args.no_filter_lang:
            return pd.DataFrame.from_dict(row, orient='index').T
        else:
            return pd.DataFrame.from_dict(row, orient='index').T

    except Exception as e:
        # print(e)
        pass
    except KeyboardInterrupt:
        exit()
    return None


if __name__ == '__main__':
    df = pd.read_csv(args.input)
    df = df.sample(30)
    dfs = []
    with alive_bar(len(df), dual_line=True, title="Extracting Text") as bar:
        with ThreadPoolExecutor(max_workers=1) as pool:
            futures = [pool.submit(translate_text, work)
                       for work in df.to_dict('records')]
            for result in as_completed(futures):
                dfs.append(result.result())
                bar()
    dfs = [i for i in dfs if i is not None]
    out = pd.concat(dfs)

    print(out)
    if args.output is not None:
        out.to_csv(args.output, index=False)
    else:
        out.to_csv(input("Save file to: "), index=False)
    print(f"Wrote {len(out)} entries.")
