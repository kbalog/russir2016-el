# RUSSIR'16 Entity linking exercise

This exercise was given as part of the Entity Linking lecture at the 10th Russian Summer School in Information Retrieval (RuSSIR 2016).

Presentation slides: [http://bit.ly/russir2016-el](http://bit.ly/russir2016-el)  

## Tasks

  - Complete the missing parts in [el_cmn.py](nordlys/el_cmn.py) to implement a simple commonness baseline.
    * I.e., link each mention to the entity with the highest commonness score.
    * Sample solution: [el_cmn_sol.py](nordlys/el_cmn_sol.py)
  - Implement TAGME's voting approach for disambiguation by completing [el_tagme.py](nordlys/el_tagme.py). 
    * This builds on the previous exercise and already includes commonness computation.
    * We note that the original TAGME approach includes additional pruning steps, which are disregarded here (those would make a big difference in performance though). 
    * Sample solution: [el_tagme_sol.py](nordlys/el_tagme_sol.py)
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

| Method | Score threshold | Prec | Recall | F1 |
| :--- | :--- | ---: | ---: | ---: | 
| Commonness | 0.5  | 0.4407 | 0.5629 | 0.4944 | 
| Commonness | 0.7 | 0.4533 | 0.4675 | 0.4603 | 
| Commonness | 0.9 | 0.6000 | 0.3532 | 0.4446 | 
| TAGME | 0.5  | 0.4634 | 0.4929 | 0.4777 | 
| TAGME | 0.7  | 0.4763 | 0.4233 | 0.4483 | 
| TAGME | 0.9  | 0.5857 | 0.3357 | 0.4268 | 


## Credits

This exercise was created based on the [TAGME reproducibility code](https://github.com/hasibi/TAGME_Reproducibility) developed by [Faegheh Hasibi](http://hasibi.com/). 
