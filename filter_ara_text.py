import argparse
import pandas as pd


parser = argparse.ArgumentParser()
parser.add_argument('-i',
                    '--input', help='CSV of extracted websites',  required=True)
parser.add_argument('-o',
                    '--output',  help='where to write output')
parser.add_argument('--no-filter-lang', default=False, action='store_true')
args = parser.parse_args()


accepted_lang = 'ar'



def is_arabic_char(ch):
    if ('\u0600' <= ch <= '\u06FF' or
        '\u0750' <= ch <= '\u077F' or
        '\u08A0' <= ch <= '\u08FF' or
        '\uFB50' <= ch <= '\uFDFF' or
        '\uFE70' <= ch <= '\uFEFF' or
        '\U00010E60' <= ch <= '\U00010E7F' or
            '\U0001EE00' <= ch <= '\U0001EEFF'):
        return True
    else:
        return False


def is_arabic(s):
    for i in s[:20]:
        if is_arabic_char(i):
            return True
    return False


if __name__ == '__main__':
    df = pd.read_csv(args.input)
    print(len(df))

    # filter for arabic
    df['is_arabic'] = df.apply(lambda row: is_arabic(row['body']), axis=1)
    index_names = df[df['is_arabic'] == False].index
    df.drop(index_names, inplace=True)
    df.drop(['is_arabic'], axis=1, inplace=True)

    print(df)

    if args.output is not None:
        df.to_csv(args.output, index=False)
    else:
        df.to_csv(input("Save file to: "), index=False)
    print(f"Wrote {len(out)} entries.")
