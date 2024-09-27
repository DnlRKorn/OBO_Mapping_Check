from collections import defaultdict
import os.path
import csv
from oaklib import get_adapter


#help(os)
#help(os.path)

mappings = [x for x in os.listdir("OUTPUT") if x.endswith("_mappings.tsv")]
#print(mappings)

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

relmap = defaultdict(lambda : defaultdict(set))

for mapping in mappings:
    mappingDict = getMappingDict("OUTPUT/" + mapping)
    mapping_dataset = mapping.replace("_mappings.tsv","")

    for (relation,predicate) in mappingDict.items():
        #relmap[relation][predicate] = relmap[relation][predicate].add(mapping_dataset)
        relmap[relation][predicate].add(mapping_dataset)

adapater = get_adapter("ubergraph:")
#print(adapater.label("BFO:0000050"))

with open("mapping_conflicts.tsv",'w') as f:
    writer = csv.writer(f,delimiter='\t')    
    writer.writerow(['relation','relation_label_(from_Ubergraph)','biolink_predicate','obo_dataset_mapping_found_in'])
    for relation in relmap:
        if(len(relmap[relation])>1):
            relation_label = adapater.label(relation)
            sortedMapTuples = [(pred,sorted(list(s))) for (pred,s) in relmap[relation].items()]
#            print(x,sorted(sortedMapTuples))
            for (i, (predicate,datasets)) in enumerate(sorted(sortedMapTuples)):
                if(i==0):writer.writerow([relation,relation_label,predicate,*datasets])
                else:writer.writerow([None,None,predicate,*datasets])
    #    for y in relmap[x]:
    #        print(x,y,relmap[x][y])
