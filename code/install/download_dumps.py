import paths

def download_wikipedia_dump():
    print("downloading wikipedia dump")
    file_util.ensure_dir(paths.WIKIPEDIA_DUMP_DIR)
	WIKIPEDIA_DUMP_URL = 'https://dumps.wikimedia.org/enwiki/' + paths.WIKIPEDIA_DUMP_DATE + '/' + paths.WIKIPEDIA_DUMP_FILENAME
    subprocess.call([
        "wget",
        WIKIPEDIA_DUMP_URL,
        "-O" + paths.WIKIPEDIA_DUMP_FILE,
        "--no-verbose",
        "--show-progress",
        "--continue"
    ])

def download_wikidata_dump():
    print("downloading wikidata dump")
    file_util.ensure_dir(paths.WORK_DIR + '/wikidata')
	print("downloading json dump")
	WIKIDATA_JSON_DUMP_URL = 'https://dumps.wikimedia.org/wikidatawiki/entities/' + paths.WIKIDATA_DUMP_DATE + '/' + paths.WIKIDATA_JSON_DUMP_FILENAME
    subprocess.call([
        "wget",
        WIKIDATA_JSON_DUMP_URL,
        "-O" + paths.WIKIDATA_JSON_DUMP_FILE,
        "--no-verbose",
        "--show-progress",
        "--continue"
    ])

	print("downloading ttl dump")
	WIKIDATA_TTL_DUMP_URL = 'https://dumps.wikimedia.org/wikidatawiki/entities/' + paths.WIKIDATA_DUMP_DATE + '/' + paths.WIKIDATA_TTL_DUMP_FILENAME
	subprocess.call([
        "wget",
        WIKIDATA_TTL_DUMP_URL,
        "-O" + paths.WIKIDATA_TTL_DUMP_FILE,
        "--no-verbose",
        "--show-progress",
        "--continue"
    ])

	# TODO: bzcat only if needed

	print("bunzipping ttl dump (this will take a long time, 67 gigs incoming)")
    subprocess.call([
        "bunzip2",
        paths.WIKIDATA_TTL_DUMP_FILE # XXX: > $WIKIDATA_TTL_DUMP_UNPACKED_FILE
    ])

def main():
    download_wikipedia_dump()
    download_wikidata_dump()

if __name__ == '__main__':
    main()
