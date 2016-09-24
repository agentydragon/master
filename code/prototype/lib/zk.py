from kazoo import client as kazoo_client

kz = kazoo_client.KazooClient()

def start():
    kz.start()

def get_wikidata_endpoint():
    if kz.client_state != 'CONNECTED':
        print('WARN: Kazoo client not connected')
        return None

    wikidata_endpoint_node = '/user/prvak/thesis/wikidata-service'

    if kz.exists(wikidata_endpoint_node):
        return kz.get(wikidata_endpoint_node).decode('UTF-8')
    else:
        return None

def get_dbpedia_endpoint():
    if kz.client_state != 'CONNECTED':
        print('WARN: Kazoo client not connected')
        return None

    dbpedia_endpoint_node = '/user/prvak/thesis/dbpedia-service'

    if kz.exists(dbpedia_endpoint_node):
        return kz.get(dbpedia_endpoint_node).decode('UTF-8')
    else:
        return None
