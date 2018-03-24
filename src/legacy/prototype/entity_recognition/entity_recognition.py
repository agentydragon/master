import json
import os.path
from src.prototype.entity_recognition import spotlight
from src.prototype.lib import article_repo
from src.prototype.lib import flags
import sys
import time
import subprocess
import datetime

import random

class SpotlightServer(object):
    def __init__(self):
        self.spotlight_port = None
        self.spotlight_process = None

    def make_client(self):
        address = "http://localhost:%d/rest/annotate" % self.spotlight_port
        return spotlight.SpotlightClient(address)

    def launch(self):
        print("Starting Spotlight server")

        self.spotlight_port = 2222 + random.randint(0, 100)
        self.spotlight_process = subprocess.Popen([
            'prototype/entity_recognition/spotlight_server',
            str(self.spotlight_port),
        ])

        # TODO: Timeout after some time.

        wait_seconds = 60

        while True:
            assert self.spotlight_process.poll() is None, "Spotlight server died"

            try:
                client = self.make_client()
                client.annotate_text("Barack Obama is the president of the United States.")
                break
            except:
                waiting = True
                print('not yet OK:', sys.exc_info()[0], 'waiting %d seconds' % wait_seconds)
                print(sys.exc_info()[1])
                sys.stdout.flush()
                time.sleep(wait_seconds)
                continue

        print("Spotlight seems to be running OK.")

    def stop(self):
        print("Terminating Spotlight...")
        self.spotlight_process.terminate()
        time.sleep(5)
        print("Killing Spotlight...")
        self.spotlight_process.kill()
        self.spotlight_process.wait()
        print("Joined. Done.")


def main():
    start = datetime.datetime.now()

    flags.add_argument('--articles', action='append')
    flags.add_argument('--force_redo')
    flags.make_parser(description='Look up articles in Spotlight')
    args = flags.parse_args()

    spotlight_server = SpotlightServer()
    spotlight_server.launch()
    print("Spotlight launched in", (datetime.datetime.now() - start))

    # TODO: skip if finished

    spotlight_client = spotlight_server.make_client()
    repo = article_repo.ArticleRepo()

    not_exist = 0
    already_done = 0
    empty = 0

    for title in args.articles:
        print("Spotlighting", title)

        if not repo.article_exists(title):
            print("Doesn't exist")
            not_exist += 1
            continue

        article_data = repo.load_article(title)

        # Skip if already done.
        if article_data.spotlight_json:
            if not args.force_redo:
                print("Already done")
                already_done += 1
                continue
        plaintext = article_data.plaintext
        if plaintext.strip() == '':
            print("Empty article")
            empty += 1
            continue
        spotlight_json = spotlight_client.annotate_text(plaintext)
        article_data.spotlight_json = spotlight_json
        repo.write_article(title, article_data)
        print("Done")

    spotlight_server.stop()

    print("Finished %d articles in" % len(args.articles), (datetime.datetime.now() - start))
    print('not_exist:', not_exist)
    print('already_done:', already_done)
    print('empty:', empty)

if __name__ == '__main__':
    main()
