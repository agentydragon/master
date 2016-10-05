from thirdparty.jena import jena
from prototype.lib import file_util
import paths
# import wget

import sys
import subprocess
import os.path

import os
assert 'SCRATCHDIR' in os.environ

# print("downloading json dump")
# WIKIDATA_JSON_DUMP_URL = 'https://dumps.wikimedia.org/wikidatawiki/entities/' + WIKIDATA_DUMP_DATE + '/' + WIKIDATA_JSON_DUMP_FILENAME
# wget.download(
#     url = WIKIDATA_JSON_DUMP_URL,
#     out = WIKIDATA_JSON_DUMP_FILE,
# )

dataset_path = paths.WORK_DIR + '/fuseki-datasets/merged'

wikidata_dump_date = '20160801'
wikidata_dump_dir = (paths.DUMP_DIR + '/wikidata')

dbpedia_dump_dir = (paths.DUMP_DIR + '/dbpedia/2015-04')
file_util.ensure_dir(dbpedia_dump_dir)
INTERLANGUAGE_LINKS_FILE = dbpedia_dump_dir + "/interlanguage-links_en.ttl"
WIKIPEDIA_LINKS_FILE = dbpedia_dump_dir + "/wikipedia_links_en.ttl"

wikidata_ttl_dump_unpacked_filename = ('wikidata-%s-all-BETA.ttl' % wikidata_dump_date)
WIKIDATA_DUMP_DATE = wikidata_dump_date
WIKIDATA_TTL_DUMP_FILENAME = "wikidata-" + wikidata_dump_date + '-all-BETA.ttl.bz2'
WIKIDATA_TTL_DUMP_FILE = wikidata_dump_dir + '/' + WIKIDATA_TTL_DUMP_FILENAME
WIKIDATA_TTL_DUMP_UNPACKED_FILE = wikidata_dump_dir + '/' + wikidata_ttl_dump_unpacked_filename

def bunzip(packed_file):
    rv = subprocess.call([
        "bunzip2",
        packed_file
    ])
    assert rv == 0

def download(url, out):
    commandline = [
        "wget",
        "-O" + out,
        # "--no-verbose",
        # "--progress=bar",
        "--continue",
        url,
    ]
    print(commandline)
    rv = subprocess.call(commandline)
    assert rv == 0

def download_wikidata_dump():
    print("downloading wikidata dumps")
    file_util.ensure_dir(wikidata_dump_dir)

    # print("downloading ttl dump")
    # WIKIDATA_TTL_DUMP_URL = 'https://dumps.wikimedia.org/wikidatawiki/entities/' + WIKIDATA_DUMP_DATE + '/' + WIKIDATA_TTL_DUMP_FILENAME
    # download(
    #     url = WIKIDATA_TTL_DUMP_URL,
    #     out = WIKIDATA_TTL_DUMP_FILE,
    # )

    # # TODO: bzcat only if needed
    # print("bunzipping ttl dump (this will take a long time, 67 gigs incoming)")
    # bunzip(WIKIDATA_TTL_DUMP_FILE) # XXX: > $WIKIDATA_TTL_DUMP_UNPACKED_FILE

    if not os.path.isfile(WIKIDATA_TTL_DUMP_UNPACKED_FILE):
        print("NOTE: bunzipping wikidata dump needs to be done manually, the dump's broken")
        print("NOTE: Place the dump at", WIKIDATA_TTL_DUMP_UNPACKED_FILE)
        sys.exit(1)

    if (os.path.isfile(INTERLANGUAGE_LINKS_FILE) and not
            os.path.isfile(INTERLANGUAGE_LINKS_FILE + ".bz2")):
        print("already got dbpedia interlanguage interlinks")
    else:
        print("downloading dbpedia interlanguage links")
        download(
            url = "http://downloads.dbpedia.org/2015-04/core-i18n/en/interlanguage-links_en.ttl.bz2",
            out = INTERLANGUAGE_LINKS_FILE + ".bz2",
        )
        print("bunzipping dbpedia interlanguage interlinks")
        bunzip(INTERLANGUAGE_LINKS_FILE + ".bz2")

    if (os.path.isfile(WIKIPEDIA_LINKS_FILE) and not
            os.path.isfile(WIKIPEDIA_LINKS_FILE + ".bz2")):
        print("already got dbpedia wikipedia links")
    else:
        print("downloading dbpedia wikipedia links")
        download(
            url = "http://downloads.dbpedia.org/2015-10/core-i18n/en/wikipedia_links_en.ttl.bz2",
            out = WIKIPEDIA_LINKS_FILE + ".bz2",
        )
        print("bunzipping dbpedia wikipedia links")
        bunzip(WIKIPEDIA_LINKS_FILE + ".bz2")

def main():
    download_wikidata_dump()

    print("cleaning output")
    subprocess.call([
        "rm",
        "-rf",
        dataset_path,
    ])

    file_util.ensure_dir(dataset_path)

    # TODO: Needs lots of RAM and scratch space
    print("loading...")
    jena.load_ttl_file(
        dataset_path,
        ttl_file_paths=[
            WIKIDATA_TTL_DUMP_UNPACKED_FILE,
            INTERLANGUAGE_LINKS_FILE, # links DBpedia to Wikidata
            WIKIPEDIA_LINKS_FILE, # links DBpedia to Wikipedia
        ],
    )

if __name__ == '__main__':
    main()
