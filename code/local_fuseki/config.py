def write_config(path, wikidata_dataset, dbpedia_sameas_dataset):
    with open(path, 'w') as f:
        f.write(get_config(wikidata_dataset, dbpedia_sameas_dataset))

def get_config(wikidata_dataset, dbpedia_sameas_dataset):
    return ("""
@prefix fuseki: <http://jena.apache.org/fuseki#> .
@prefix rdf:    <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs:   <http://www.w3.org/2000/01/rdf-schema#> .
@prefix tdb:    <http://jena.hpl.hp.com/2008/tdb#> .
@prefix ja:     <http://jena.hpl.hp.com/2005/11/Assembler#> .
@prefix :       <#> .

[] rdf:type fuseki:Server ;
   fuseki:services (<#service-wikidata> <#service-dbpedia-sameas>) .

# Declaration additional assembler items.
[] ja:loadClass "org.apache.jena.tdb.TDB" .

# TDB
tdb:DatasetTDB  rdfs:subClassOf  ja:RDFDataset .
tdb:GraphTDB    rdfs:subClassOf  ja:Model .

# fuseki:serviceReadGraphStore      "get" ;      # SPARQL Graph store protocol (read only)
# Query timeout on this dataset (1s, 1000 milliseconds)
# ja:context [ ja:cxtName "arq:queryTimeout" ;  ja:cxtValue "1000" ] ;

<#service-wikidata> rdf:type fuseki:Service ;
    fuseki:name         "wikidata" ; # http://host:port/wikidata
    fuseki:serviceQuery "query" ;    # SPARQL query service
    fuseki:dataset      <#dataset-wikidata> ; .

<#service-dbpedia-sameas> rdf:type fuseki:Service ;
    fuseki:name         "dbpedia-sameas" ; # http://host:port/dbpedia-sameas
    fuseki:serviceQuery "query" ;    # SPARQL query service
    fuseki:dataset      <#dataset-dbpedia-sameas> ; .

<#dataset-wikidata> rdf:type tdb:DatasetTDB ; tdb:location "%s" ; .
<#dataset-dbpedia-sameas> rdf:type tdb:DatasetTDB ; tdb:location "%s" ; .
""") % (wikidata_dataset, dbpedia_sameas_dataset)
