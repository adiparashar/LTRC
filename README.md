# Interlingua (USR) based machine translation for Indian languages
_This repository contains the code and related files, from the work I did at the Language Technologies Research Centre(LTRC), IIIT Hyderabad as a research intern under the guidance of Dr. Sukhada(IIT BHU) and Dr. Soma Paul (IIIT-H)._

Indian languages are syntactically and morphologically complex, in addition to them being low resource. The objective of the project is to create effective methods for neural machine translation with limited resources. This will be achieved by combining the latest developments in deep learning combined with heuristics from traditional linguistic and grammatical knowledge. The main focus is to design an interlingua(USR, Universal Semantic Representation), based on the Pāṇinian Sanskrit grammatical framework, which will serve as a comprehensible intermediary representation for all the languages included in the translation process. We focused on Hindi, Sanskrit and English(for proof of concept) as part of our experiments.

My undertakings can be broadly categorized into the following:

* Dataset creation and processing:
Concept dictionary creation: Hindi and Sanskrit bilingual dictionaries from various sources were scraped to build a concept dictionary repository which maps words to their semantic concepts(single or compund word meanings in a common language, say English) for both the languages. 

* USR generation: Universal Semantic Representation (USR) captures the meaning expressed by a sentence in the discourse. It has rows corresponding to properties of the sentence and its concept words. These properties are the concepts(and TAM (tense-aspect-modality) specification on the verb), semantic category of nouns, GNP (Gender, Number, Person) information, dependency relations, anaphora,speaker’s view-points, sentence type etc.


* Sentence generation:
Neural generation: To generate the sentence back from a given USR they were converted to a AMR like graphs which was then linearized using a DFS based approach. We finetuned different seq2seq LLMs to generate the sentences back from these linearizations.

