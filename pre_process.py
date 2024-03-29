import pandas as pd
import re
from camel_tools.utils.dediac import dediac_ar
from camel_tools.utils.normalize import normalize_alef_maksura_ar
from camel_tools.utils.normalize import normalize_alef_ar
from camel_tools.utils.normalize import normalize_teh_marbuta_ar
from camel_tools.utils.normalize import normalize_unicode
from camel_tools.tokenizers.word import simple_word_tokenize
from camel_tools.utils.charsets import AR_CHARSET

from camel_tools.disambig.mle import MLEDisambiguator

# instantiate the Maximum Likelihood Disambiguator
mle = MLEDisambiguator.pretrained()

stop_words = set(open("stop_words.txt", "r").read().split("\n")[:-1])


def ortho_normalize(text):
    text = normalize_unicode(text)
    text = normalize_alef_maksura_ar(text)
    text = normalize_alef_ar(text)
    text = normalize_teh_marbuta_ar(text)
    return text

def get_diacritized(tokenized_text):
    disambig = mle.disambiguate(tokenized_text)
    try:
        diacritized = [d.analyses[0].analysis['lex'] for d in disambig]
        return diacritized
    except:
        return ""

def remove_stopwords(tokenized_text):
    ar_str = u''.join(AR_CHARSET)
    arabic_re = re.compile(r'^[' + re.escape(ar_str) + r']+$')
    # print(arabic_re.match(tokenized_text[0]) is not None)
    return [i for i in tokenized_text if i not in stop_words
            and arabic_re.match(i) is not None]

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
    for i in s:
        if not is_arabic_char(i):
            return False
    return True


class pre_process:
    def process(text):
        # text = dediac_ar(text)
        # text = ortho_normalize(text)
        
        text = simple_word_tokenize(text)
        text = [i for i in text if is_arabic(i)]

        # print(text)
        # try:
        text = get_diacritized(text)
        text = [i for i in text if i != ""]
        # except Exception as e:
        #     print(e)
        #     print(text)
        #     exit()
        # return ""
        text = remove_stopwords(text)
        # return text
        return " ".join(text)


if __name__ == "__main__":
    import sys
    file = sys.argv[1]
    df = pd.read_csv(file)
    df['pre_processed'] = df.body.apply(pre_process.process)

    # text = df.body.to_list()[0]
    # # print(text, end="\n\n")
    # # print(pre_process.process(text))
    df.to_csv(sys.argv[2],index=False)
