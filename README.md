# RUSSIR'16 Entity linking exercise

This exercise was given as part of the Entity Linking lecture at the 10th Russian Summer School in Information Retrieval (RuSSIR 2016).

Presentation slides: [http://bit.ly/russir2016-el](http://bit.ly/russir2016-el)  

## Tasks

  - Complete the missing parts in [el_cmn.py](nordlys/el_cmn.py) to implement a simple commonness baseline.
    * I.e., link each mention to the entity with the highest commonness score.
    * Sample solution: [el_commonness.py](nordlys/el_cmn_sol.py)
  - Implement TAGME's voting approach for disambiguation by completing [el_tagme.py](nordlys/el_tagme.py). 
  - Optionally, you can implement any other disambiguation approach (including novel ideas of your own).
  - The input documents are found in [data/snippets.txt](data/snippets.txt); the first column is the docID
  - The results (one annotation per line) need to be written in a file using the following format: `docID score entityID mention page-id`
    * where score is the annotation confidence score and the last column is the string 'page-id'
    * see [data/output_cmn.txt](data/output_cmn.txt) for an example
  - Evaluation: `evaluator_annot.py <qrel_file> <result_file> [score_threshold]`
    * If `score_threshold` is provided, the evaluation script will only consider annotations from the output file with scores above the given threshold (and ignore lower confidence annotations).
    

## Code

See the code files under the [nordlys](nordlys/) directory.

Python v2.7 is required.


## Data files

  - [mention_entity.tsv](data/mention_entity.tsv): number of times a mention refers to a given entity
    * Format: `mention entity frequency`
    * When entity="_total" it means the total number of times the mention was linked (to any entity) 
  - [entity_inlinks.tsv](data/entity_inlinks.tsv): total number of inlinks an entity has 
    * Format: `entity frequency`
  - [entity_pairs_inlinks.tsv](data/entity_pairs_inlinks.tsv): number of inlinks two entities have in common
    * Format: `entity1 entity2 frequency`
  - [snippets.txt](data/snippets.txt): 20 input text snippets (to be annotated)
    * Format: `id text`
  - [qrels.txt](data/qrels.txt) ground truth annotations corresponding to snippets.txt
    * Format: `id 1 entityID mention tmpID`


## Evaluation results

| Method | Prec | Recall | F1 |
| :--- | ---: | ---: | ---: | 
| Commonness, 0 threshold | 0.3565 | 0.6025 | 0.4480 | 
| Commonness, 0.7 threshold | 0.4533 | 0.4675 | 0.4603 | 
| Commonness, 0.9 threshold | 0.6000 | 0.3532 | 0.4446 | 


## Credits

This exercise was created from the [TAGME reproducibility code](https://github.com/hasibi/TAGME_Reproducibility) developed by [Faegheh Hasibi](http://hasibi.com/). 
