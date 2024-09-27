import tarfile
import tempfile
import sys
import requests
import csv
import os.path
from collections import defaultdict


def getEdgeTsv(resource_url):
    tmp_file = tempfile.TemporaryFile('w+b')
    request = requests.get(resource_url)
    
    tmp_file.write(request.content)
    tmp_file.seek(0)
    obo_tar = tarfile.open(fileobj=tmp_file, mode='r')
    
    #Only extract the edge file from the tar.gz archive.
    edge_file_name = f"{obo_name}_kgx_tsv_edges.tsv"
    obo_tar.extractall(path="TSV_FILES", members=[edge_file_name], filter='data')
    print(f"Downloaded and extracted edge file to TSV_FILES/{edge_file_name}")

    return

def getRelationToPredicateDict(edge_file_name):
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
    return rel_pred_cnt

def writeRelationToPredicateTSV(rel_pred_cnt, output_fname):
    with open(f"OUTPUT/{output_fname}",'w') as f:
        writer = csv.writer(f,delimiter='\t')
        writer.writerow(["relation","predicate","count"])
        for (rel,pred) in sorted(rel_pred_cnt.keys()):
            writer.writerow([rel,pred,rel_pred_cnt[(rel,pred)]])

if(__name__=="__main__"):
    if(len(sys.argv)==1): raise RuntimeError("Need to pass a URL of an OBO"
    +"gzipped tar of kgx files")
    resource_url = sys.argv[1]
    obo_name = resource_url.split('/')[4]
    archive_file_name = f"{obo_name}_kgx_tsv.tar.gz"

    edge_file_name = f"{obo_name}_kgx_tsv_edges.tsv"
    #resource_url = "https://kg-hub.berkeleybop.io/kg-obo/labo/2021-06-08/labo_kgx_tsv.tar.gz"
    
    if(not os.path.isfile(f"TSV_FILES/{edge_file_name}")):
        getEdgeTsv(resource_url + '/' + archive_file_name)
        if(not os.path.isfile(f"TSV_FILES/{edge_file_name}")):
            raise ValueError(f"Could not get {edge_file_name} from {resource}.")
    rel_pred_cnt = getRelationToPredicateDict(edge_file_name)
    print(f"Read through {edge_file_name}, found no errors. Writing to OUTPUT/{obo_name}_mappings.tsv")
    output_fname = f"{obo_name}_mappings.tsv"
    writeRelationToPredicateTSV(rel_pred_cnt, output_fname)
