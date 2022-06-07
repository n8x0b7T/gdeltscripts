#!/usr/bin/env python3

from rake_nltk import Rake

import nltk

nltk.download('stopwords')
nltk.download('punkt')

r = Rake()
text = ''''''

r.extract_keywords_from_text(text)

print(r.get_ranked_phrases_with_scores()[0:10])
