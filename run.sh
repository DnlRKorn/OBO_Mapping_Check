#Get all of the OBO links; check for consistency in single kgx relation mapping
# and build an output file which generalizes relation->biolink mappings. 
for obo_link in $(python get_kg_obo_links.py); do 
    python get_kgx_tsv_and_build_mappings.py $obo_link; 
done

#Check across all OBO mappings files for conflicts.
python check_for_mapping_conflicts.py

