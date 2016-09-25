import paths
from thirdparty.fuseki import fuseki
from prototype.lib import flags
import subprocess
import datetime
import os

scratch_dir = os.environ['SCRATCHDIR']

wikidata_dataset_source = paths.WORK_DIR + '/fuseki-datasets/wikidata'
dbpedia_sameas_dataset_source = paths.WORK_DIR + '/fuseki-datasets/dbpedia-sameas'

def copy_dataset(dataset_from, dataset_to, name):
    print("Copying %s dataset to local disk..." % name, datetime.datetime.now())
    rv = subprocess.call([
        "cp",
        "-rv",
        dataset_from,
        dataset_to
    ])
    print("Copied.")
    assert rv == 0

# wikidata_dataset = wikidata_dataset_source
# dbpedia_sameas_dataset = dbpedia_sameas_dataset_source

wikidata_dataset = scratch_dir + '/wikidata'
dbpedia_sameas_dataset = scratch_dir + '/dbpedia-sameas'
copy_dataset(wikidata_dataset_source, wikidata_dataset,
             name="Wikidata")
copy_dataset(dbpedia_sameas_dataset_source, dbpedia_sameas_dataset,
             name="DBpedia owl:sameAs")

print("Starting Wikidata Fuseki...", datetime.datetime.now())
config = """
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
""" % (wikidata_dataset, dbpedia_sameas_dataset)

config_file_path = scratch_dir + '/fuseki-config.ttl'
with open(config_file_path, 'w') as f:
    f.write(config)

fuseki.spawn(
    config = config_file_path,
    port = 3030
)

flags.add_argument('--articles', action='append')
flags.make_parser(description='TODO')
args = flags.parse_args()

cmdline = [
    "prototype/make_training_samples/make_training_samples",
    "--wikidata_endpoint",
    "http://localhost:3030/wikidata/query",
    "--dbpedia_endpoint",
    "http://localhost:3030/dbpedia-sameas/query",
]

for article in args.articles:
    cmdline.extend(['--articles', article])

print(cmdline, datetime.datetime.now())
subprocess.call(cmdline)
