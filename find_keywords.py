from rake_nltk import Rake

import nltk
nltk.download('stopwords')
nltk.download('punkt')


r = Rake()
text = '''The lawyer for Hutchins' family argues that Baldwin and other producers engaged in 'reckless conduct and cost-cutting measures', which resulted in the death of photographer \xa0 The family of, the woman who died for sued for wrongful death to the actor, who fired the gun. She was rehearsing on a New Mexico set in October a scene with a revolver with Halyna Hutchins, the film's cinematographer, when a gunshot fatally wounded her. Attorney Brian Parnish, at a news conference Tuesday, argued that and other producers of the western engaged in "reckless conduct and cost-cutting measures," which led to Hutchins' death. The Attorney Representing M'''
r.extract_keywords_from_text(text)

print(r.get_ranked_phrases_with_scores()[0:10])

