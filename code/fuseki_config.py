def write_config(path, dataset):
    with open(path, 'w') as f:
        f.write(get_config(dataset))

def get_config(dataset):
    # TODO: timeout as seconds
    return ("""
@prefix fuseki: <http://jena.apache.org/fuseki#> .
@prefix rdf:    <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs:   <http://www.w3.org/2000/01/rdf-schema#> .
@prefix tdb:    <http://jena.hpl.hp.com/2008/tdb#> .
@prefix ja:     <http://jena.hpl.hp.com/2005/11/Assembler#> .
@prefix :       <#> .

[] rdf:type fuseki:Server ;
   fuseki:services (<#service-merged>) .

# Declaration additional assembler items.
[] ja:loadClass "org.apache.jena.tdb.TDB" .

# TDB
tdb:DatasetTDB  rdfs:subClassOf  ja:RDFDataset .
tdb:GraphTDB    rdfs:subClassOf  ja:Model .

# fuseki:serviceReadGraphStore      "get" ;      # SPARQL Graph store protocol (read only)

<#service-merged> rdf:type fuseki:Service ;
    fuseki:name         "merged" ; # http://host:port/merged
    fuseki:serviceQuery "query" ;    # SPARQL query service
    fuseki:dataset      <#dataset-merged> ; .

<#dataset-merged> rdf:type tdb:DatasetTDB ; tdb:location "%s" ;
    # Query timeout on this dataset (20min, 1200000 milliseconds)
    ja:context [ ja:cxtName "arq:queryTimeout" ;  ja:cxtValue "1200000" ] ;
    .
""") % (dataset)
