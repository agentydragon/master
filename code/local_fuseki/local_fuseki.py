import paths
from thirdparty.fuseki import fuseki
from prototype.lib import flags
import subprocess
import datetime
import os

scratch_dir = os.environ['SCRATCHDIR']

print("Copying Wikidata to local disk...", datetime.datetime.now())
rv = subprocess.call([
    "cp",
    "-rv",
    paths.WORK_DIR + '/fuseki-datasets/wikidata',
    scratch_dir + '/wikidata'
])
print("Copied.")
assert rv == 0

print("Copying DBpedia to local disk...", datetime.datetime.now())
rv = subprocess.call([
    "cp",
    "-rv",
    paths.WORK_DIR + '/fuseki-datasets/dbpedia-sameas',
    scratch_dir + '/dbpedia-sameas'
])
print("Copied.")
assert rv == 0

print("Starting Wikidata Fuseki...", datetime.datetime.now())
config = """
@prefix fuseki:  <http://jena.apache.org/fuseki#> .
@prefix rdf:     <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs:    <http://www.w3.org/2000/01/rdf-schema#> .
@prefix tdb:     <http://jena.hpl.hp.com/2008/tdb#> .
@prefix ja:      <http://jena.hpl.hp.com/2005/11/Assembler#> .
@prefix :        <#> .

[] rdf:type fuseki:Server ;
   fuseki:services (
     <#service-wikidata>
     <#service-dbpedia-sameas>
   ) .

# Declaration additional assembler items.
[] ja:loadClass "org.apache.jena.tdb.TDB" .

# TDB
tdb:DatasetTDB  rdfs:subClassOf  ja:RDFDataset .
tdb:GraphTDB    rdfs:subClassOf  ja:Model .

# fuseki:serviceReadGraphStore      "get" ;      # SPARQL Graph store protocol (read only)
# Query timeout on this dataset (1s, 1000 milliseconds)
# ja:context [ ja:cxtName "arq:queryTimeout" ;  ja:cxtValue "1000" ] ;
# fuseki:serviceReadGraphStore      "get" ;      # SPARQL Graph store protocol (read only)

<#service-wikidata> rdf:type fuseki:Service ;
    fuseki:name                       "wikidata" ; # http://host:port/wikidata
    fuseki:serviceQuery               "query" ;    # SPARQL query service
    fuseki:dataset                   <#dataset-wikidata> ;

<#service-dbpedia-sameas> rdf:type fuseki:Service ;
    fuseki:name                       "dbpedia-sameas" ; # http://host:port/dbpedia-sameas
    fuseki:serviceQuery               "query" ;    # SPARQL query service
    fuseki:dataset                   <#dataset-dbpedia-sameas> ;
    .
<#dataset-wikidata> rdf:type tdb:DatasetTDB ; tdb:location "%s" ;
<#dataset-dbpedia-sameas> rdf:type tdb:DatasetTDB ; tdb:location "%s" ; .
""" % (scratch_dir + '/wikidata', scratch_dir + '/dbpedia-sameas')

with open(scratch_dir + '/fuseki-config.ttl', 'w') as f:
    f.write(config)

fuseki.spawn(
    config = scratch_dir + '/fuseki-config.ttl',
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
