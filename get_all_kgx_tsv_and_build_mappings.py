import tarfile
import tempfile
import sys
import requests
import csv
import os.path
from collections import defaultdict

argc = len(sys.argv)
print(argc)
print(sys.argv)
if(argc<2):
    resource_url = "https://kg-hub.berkeleybop.io/kg-obo/labo/2021-06-08/labo_kgx_tsv.tar.gz"
else:
    resource_url = sys.argv[1]
print(resource_url)

obo_name = resource_url.split('/')[4]
edge_file_name = f"{obo_name}_kgx_tsv_edges.tsv"


def getEdgeTsv(resource_url):
    tmp_file = tempfile.TemporaryFile('w+b')
    request = requests.get(resource_url)
    
    tmp_file.write(request.content)
    tmp_file.seek(0)
    obo_tar = tarfile.open(fileobj=tmp_file, mode='r')
    
    #labo_kgx_tsv_nodes.tsv
    edge_file_name = f"{obo_name}_kgx_tsv_edges.tsv"
    obo_tar.extractall(path="TSV_FILES",members=[edge_file_name])
    print(f"Downloaded and extracted edge file to TSV_FILES/{edge_file_name}")
    return


if(not os.path.isfile(f"TSV_FILES/{edge_file_name}")):
    getEdgeTsv(resource_url)
    if(not os.path.isfile(f"TSV_FILES/{edge_file_name}")):
        raise ValueError(f"Could not get {edge_file_name} from {resource}.")


#print(keys(test))

rel_pred_cnt = defaultdict(int)
rel_test = {}
with open(f"TSV_FILES/{edge_file_name}") as edge_file:
    dreader = csv.DictReader(edge_file, delimiter='\t')
    for row in dreader:
        rel = row['relation']
        pred = row['predicate']
        rel_pred_cnt[(rel,pred)]+=1
        if(rel not in rel_test):rel_test[rel] = pred
        if(rel_test[rel]!=pred): raise ValueError(f"{edge_file_name},{rel},{rel_test[rel]},{pred}")
print(f"Read through {edge_file_name}, found no errors. Writing to OUTPUT/{obo_name}_mappings.tsv")

with open(f"OUTPUT/{obo_name}_mappings.tsv",'w') as f:
    writer = csv.writer(f,delimiter='\t')
    writer.writerow(["relation","predicate","count"])
    for (rel,pred) in sorted(rel_pred_cnt.keys()):
        writer.writerow([rel,pred,rel_pred_cnt[(rel,pred)]])
