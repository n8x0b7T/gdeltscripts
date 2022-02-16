from rake_nltk import Rake

import nltk
nltk.download('stopwords')
nltk.download('punkt')


r = Rake()
text = '''The lawyer for Hutchins' family argues that Baldwin and other producers engaged in 'reckless conduct and cost-cutting measures', which resulted in the death of photographer \xa0 The family of, the woman who died for sued for wrongful death to the actor, who fired the gun. She was rehearsing on a New Mexico set in October a scene with a revolver with Halyna Hutchins, the film's cinematographer, when a gunshot fatally wounded her. Attorney Brian Parnish, at a news conference Tuesday, argued that and other producers of the western engaged in "reckless conduct and cost-cutting measures," which led to Hutchins' death. The Attorney Representing M'''
text = '''Working with continuing to pay their wages " . In addition, the democratic current issued a statement stating that " the decision to dissolve the Supreme Council of the Judiciary is an additional step in the process of disassemblying the State and beating its institutions by the power of the coup and destroying the achievements of the Tunisian people, which are accompanied by successive generations, defending the rights of Tunisians and Tunisians in a State that respects the rights and freedoms guaranteed by an independent judicial authority " , reaffirming its clear right to encroach the executive power of the executive branch, which is bound by the President of the President of the President of the President of Justice. The party stated that " Mr. Kiss Saeed was more likely to authorize the transfer of corruption and illicit enrichment files in which judges were implicated to the Ministry of Justice public inspectorate and then to the Supreme Council of the Judiciary, rather than merely to politicize public opinion against the Council in preparation for its resolution.'''

r.extract_keywords_from_text(text)

print(r.get_ranked_phrases_with_scores()[0:10])

