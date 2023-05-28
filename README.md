# Interlingua (USR) based machine translation for Indian languages
_This repository contains the code and related files, from the work I did at the Language Technologies Research Centre(LTRC), IIIT Hyderabad as a research intern under the guidance of Dr. Sukhada(IIT BHU) and Dr. Soma Paul (IIIT-H)._

Indian languages are syntactically and morphologically complex, in addition to them being low resource. The objective of the project is to create effective methods for neural machine translation with limited resources. This can be achieved by combining developments in deep learning combined with heuristics from traditional linguistic and grammatical knowledge. 

The main focus is to design an interlingua(USR, Universal Semantic Representation), based on the Pāṇinian Sanskrit grammatical framework, which will serve as a comprehensible intermediary representation for all the languages included in the translation process. We focused on Hindi, Sanskrit and English(for proof of concept) as part of our experiments.

My undertakings can be broadly categorized into the following:

### Dataset creation and processing:

**Concept dictionary creation**: Hindi and Sanskrit bilingual dictionaries from various sources([1](https://dsal.uchicago.edu/dictionaries/),[2](https://www.sanskrit-lexicon.uni-koeln.de/),[3](https://sanskrit.inria.fr/DICO/index.en.html)) were scraped to build a [concept dictionary repository](https://github.com/adiparashar/LTRC/tree/main/concept%20dictionaries) which maps words to their semantic concepts(single or compund word meanings in a common language, say English) for both the languages. 

**USR generation**: Universal Semantic Representation (USR) captures the meaning expressed by a sentence in the discourse. It has rows corresponding to properties of the sentence and its concept words. These properties are the concepts(and TAM (tense-aspect-modality) specification on the verb), semantic category of nouns, GNP (Gender, Number, Person) information, dependency relations, anaphora,speaker’s view-points, sentence type etc. The USR acts as the interlingua in our translation process.


### Sentence generation:

**Neural generation**: To generate the sentence back from a given USR two kinds of approaches were considered, namely the hybrid and the direct approach depending on the proportion of deep learning and linguistics they invloved. 
* The hybrid approach used a linguistic rule-based approach to generate the sentences. Since the USRs did not have postposition related details, so these generated sentences were often devoid of/contained incorrect postpositions. To generate sentences with the postpositions, LLMs were finetuned on the mask prediction task for Hindi sentences, where the masks were the unknown postpositions.

* For the direct approach the USRs were converted into AMR(Abstract Meaning Representation) inspired graphs. These USR graphs were then linearized using a DFS based approachm, to get sequences. We finetuned different seq2seq LLMs to generate the sentences back from these USR linearizations.

