from collections import defaultdict
import os.path
import csv
from oaklib import get_adapter


#help(os)
#help(os.path)

mappings = [x for x in os.listdir("OUTPUT") if x.endswith("_mappings.tsv")]
obos = [x.replace("_mappings.tsv","") for x in mappings]

def getMappingDict(mapping_file_path):
    mapping = {}
    with open(mapping_file_path) as csvfile:
        dreader = csv.DictReader(csvfile,delimiter='\t')
        for row in dreader:
            if(row["relation"] in mapping): raise ValueError(mapping_file_path)
            #mapping[row["relation"]] = (row["predicate"],int(row["count"]))
            mapping[row["relation"]] = row["predicate"]
    return mapping

mappingDict = getMappingDict("OUTPUT/" + mappings[5])
#print(mappingDict)

# PredMap: Predicate -> [DATASET_WHICH_USES]
# RelMap: Relation -> [PredMaps]

curies = defaultdict(lambda : defaultdict(set))

for mapping in mappings:
    mappingDict = getMappingDict("OUTPUT/" + mapping)
    mapping_dataset = mapping.replace("_mappings.tsv","")

    for (relation,predicate) in mappingDict.items():
        if(relation.split(":")[0].lower() in obos):
            relation = relation.upper()
            curie_prefix = relation.split(":")[0].lower()
            curies[curie_prefix][relation].add(mapping_dataset)

import urllib
import sqlite3
#adapater = get_adapter("ubergraph:")
adapter = get_adapter("sqlite:obo:ro")
seen_curies = sorted(list([x.upper() for x in curies["ro"]]))
#for curie_prefix in curies:
for curie_prefix in sorted([x.lower() for x in curies]):
    print(f"--{curie_prefix.upper()}--")
    seen_curies = sorted(list([x.upper() for x in curies[curie_prefix]]))
    try:
        adapter = get_adapter(f"sqlite:obo:{curie_prefix}")
    except urllib.error.HTTPError:
        print(f"Unable to get sqlite:obo:{curie_prefix} via oaklib")
        continue
    try:
        obsoletes = list([x.upper() for x in adapter.obsoletes()])
    except Exception as e:
        print(f"Got an sqlite3.OperationalError trying to look up obsolete in"
                + f"sqlite:obo:{curie_prefix} via oaklib:adapter.obsoletes()/f{str(e)}")
        continue
    valid_entities = list([x.upper() for x in adapter.entities(filter_obsoletes=False)])
    good_curies = [curie for curie in seen_curies if curie in valid_entities and curie \
            not in obsoletes] 
    print(f"---VALID:{curie_prefix.upper()}|{len(good_curies)}---")
    obsoletes_curies = [curie for curie in seen_curies if curie in curie in obsoletes] 
    print(f"---OBSOLETE:{curie_prefix.upper()}|{len(obsoletes_curies)}---")
    for curie in obsoletes_curies:
        relation_label = adapter.label(curie)
        print(curie + '\t' + relation_label + '\t' + ','.join(sorted(list(curies[curie_prefix][curie]))))
    missing_curies = [curie for curie in seen_curies if curie in curie not in
            valid_entities] 
    print(f"---MISSING:{curie_prefix.upper()}|{len(missing_curies)}---") 
    for curie in missing_curies:
        relation_label = adapter.label(curie)
        print(curie + '\t' + str(relation_label) + '\t' + ','.join(sorted(list(curies[curie_prefix][curie]))))
