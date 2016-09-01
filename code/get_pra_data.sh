#!/bin/bash
# TODO: and replace for smaller names.
# TODO: and remove UUIDs
query=$(python3 <(cat <<HERE
print('PREFIX wdt: <http://www.wikidata.org/prop/direct/>')
print('SELECT ?a ?b ?c')
print('WHERE {')
properties = [21, 22, 25, 27, 7, 9, 26, 451, 40, 43, 44, 1038, 103, 69, 172, 106, 101, 108, 140, 91, 1066, 802, 185, 53, 512, 552, 734, 1037, 1344, 1340, 1303, 1399, 1416, 54, 413, 1532, 241, 410, 598, 607, 452, 159, 807, 31, 112, 740, 1387, 1313, 1290]
for property in properties[:-1]:
    print('{ ?a wdt:P%s ?c } UNION' % property)
print('{ ?a wdt:P%s ?c }' % properties[-1])
print(' . ?a ?b ?c }')
HERE
))
echo "$query"
/storage/brno7-cerit/home/prvak/fuseki/apache-jena-fuseki-2.4.0/bin/s-query --output=tsv --service=http://hador:3030/wikidata/query "$query" | sed 's#<http://www.wikidata.org/entity/##g; s#<http://www.wikidata.org/prop/direct/##g; s#>##g' | tail -n +2 > result
