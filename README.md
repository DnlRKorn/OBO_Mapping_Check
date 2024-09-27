# OBO_Mapping_Check
Directory to gather all of the OBO files present in KG-HUB and some scripts to check consistency between the various mappings provided.

This consistency is checked in three ways.

## Consistency 1
OBO provides KGX files which map relations onto biolink predicates. (As an example; in LABO the relation **BFO:0000051** is mapped onto **biolink:has_part**.) We want to go through all 200+ OBO and ensure **within** an OBO file no relation is mapped onto more than one predicate. (E.g. if within LABO **BFO:0000051** was mapped onto **biolink:has_part** for one edge but mapped onto **biolink:part_of** in another.)
## Consistency 2
Check how these relation->predicate mappings are handled **across** OBO mappings. It may be the case that the same relation is given different biolink predicates in different OBO datasets. (At the time of writing it is the case that LABO has  **BFO:0000051** -> **biolink:has_part**, while CHEBI has **BFO:0000051** -> **biolink:related_to**)
## Consistency 3
Check if the CURIEs provided in one OBO dataset are resolvable within the appropriate namespace for that CURIE (e.g. make sure **BFO:0000051** has an entry in the OBO BFO entry.)
