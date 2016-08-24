# RUSSIR'16 Entity linking exercise

This small exercise was given as part of the Entity Linking lecture at the 10th Russian Summer School in Information Retrieval (RuSSIR 2016).

Presentation slides: __to-be-added__ 

## Task

Complete the missing parts in [tagme.py](nordlys/tagme.py). 

  - First, implement a commonness-based baseline. [solution](nordlys/tagme_sol1.py)
  - Then, implement TAGME's voting approach.

Output (result) file format: `docID score entityID mention page-id`

Evaluation:
`evaluator_annot.py <qrel_file> <result_file> [score_threshold]`

  - If score_threshold is provided, the evaluation script will only consider annotations from the output file with scores above the given threshold.   
    

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


## Credits

This exercise was created from the [TAGME reproducibility code](https://github.com/hasibi/TAGME_Reproducibility) developed by [Faegheh Hasibi](http://hasibi.com/). 
