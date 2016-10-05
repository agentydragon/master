def write_config(path, datasets):
    with open(path, 'w') as f:
        f.write(get_config(datasets))

def get_config(datasets):
    config = """
        @prefix fuseki: <http://jena.apache.org/fuseki#> .
        @prefix rdf:    <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs:   <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix tdb:    <http://jena.hpl.hp.com/2008/tdb#> .
        @prefix ja:     <http://jena.hpl.hp.com/2005/11/Assembler#> .
        @prefix :       <#> .

        # Declaration additional assembler items.
        [] ja:loadClass "org.apache.jena.tdb.TDB" .

        # TDB
        tdb:DatasetTDB  rdfs:subClassOf  ja:RDFDataset .
        tdb:GraphTDB    rdfs:subClassOf  ja:Model .

        [] rdf:type fuseki:Server ;
           fuseki:services ("""

    for dataset_name in datasets:
       config += (" <#service-%s>" % dataset_name)

    config += """) .  """

    for dataset_name, dataset_path in datasets.items():
        config += ("""
            <#service-%(dataset_name)s> rdf:type fuseki:Service ;
                fuseki:name         "%(dataset_name)" ; # http://host:port/dsname/query
                fuseki:serviceQuery "query" ;
                fuseki:dataset      <#dataset-%(dataset_name)> ; .

            <#dataset-%(dataset_name)> rdf:type tdb:DatasetTDB ; tdb:location "%(dataset_path)s" ;
                ja:context [ ja:cxtName "arq:queryTimeout" ;  ja:cxtValue "%(timeout_ms)d" ] ;
                .
                """ % {
                    'dataset_name': dataset_name,
                    'dataset_path': dataset_path,
                    'timeout_ms': 20 * 60 * 1000,  # 20 minutes
                })
    return config
