import SPARQLWrapper
import re
import time
import urllib
import urllib.error
from prototype.lib import flags
import http.client

PREFIXES = {
    'owl': 'http://www.w3.org/2002/07/owl#',
    'rdfs': 'http://www.w3.org/2000/01/rdf-schema#',
    'wd': 'http://www.wikidata.org/entity/',
    'wdp': 'http://www.wikidata.org/prop/direct/',
    'dbr': 'http://dbpedia.org/resource/',
}

STANDARD_PREFIXES = ""
for key, url in PREFIXES.items():
    STANDARD_PREFIXES += "PREFIX %s: <%s>\n" % (key, url)

r = re.compile('^[a-zA-Z_]*$')

def url_to_query(url):
    for key, prefix in PREFIXES.items():
        if url.startswith(prefix):
            suffix = url[len(prefix):]
            if r.match(suffix):
                return key + ':' + suffix
    return '<%s>' % url

"""
# get entity name
SELECT *
WHERE { wd:Q1 rdfs:label ?b FILTER (langMatches(lang(?desc),"en")) }
"""

flags.add_argument('--log_queries', type=bool, default=False)

class SPARQLClient(object):
    def __init__(self, endpoint):
        self.client = SPARQLWrapper.SPARQLWrapper(endpoint)
        self.client.setReturnFormat(SPARQLWrapper.JSON)
        self.client.setMethod('POST')
        self.client.setRequestMethod(SPARQLWrapper.POSTDIRECTLY)

    def get_results(self, query, retry=4):
        query_for_printing = ' '.join(map(str.strip, query.split('\n')))

        if flags.parse_args().log_queries:
            print("Getting results:", query_for_printing)

        try:
            self.client.setQuery(STANDARD_PREFIXES + query)
            results = self.client.query().convert()
            if 'results' in results:
                # print("Got %d results." % len(results['results']['bindings']))
                pass
            return results
        except (ConnectionResetError, OSError, urllib.error.URLError,
                SPARQLWrapper.SPARQLExceptions.EndPointInternalError,
                http.client.BadStatusLine) as e:
            error = e
            if not retry:
                raise
        # Try retrying in case of transient failures
        time_to_sleep = 10 * (2 ** (4 - retry))
        print(error, "Retrying in %d seconds (retries left:" % time_to_sleep, retry, ")")
        time.sleep(time_to_sleep)
        return self.get_results(query, retry=retry-1)

    def get_result_values(self, query):
        """More friendly API around get_results."""
        results = self.get_results(query)
        results = results['results']['bindings']
        values = []

        for row in results:
            row_values = {}
            for key in row:
                row_values[key] = row[key]['value']
            values.append(row_values)

        return values
