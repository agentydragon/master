import paths
from thirdparty import fuseki

fuseki.serve(
    dataset_path = paths.WORK_DIR + '/fuseki-datasets/wikidata',
    namespace = '/wikidata'
)
