def download_wikipedia_dump():
    print("downloading wikipedia dump")
    file_util.ensure_dir(paths.WIKIPEDIA_DUMP_DIR)
	WIKIPEDIA_DUMP_URL = 'https://dumps.wikimedia.org/enwiki/' + paths.WIKIPEDIA_DUMP_DATE + '/' + paths.WIKIPEDIA_DUMP_FILENAME
    wget.download(
        url = WIKIPEDIA_DUMP_URL,
        out = paths.WIKIPEDIA_DUMP_FILE,
    )

def main():
    download_wikipedia_dump()

if __name__ == '__main__':
    main()
