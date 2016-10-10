import json
import os.path
from prototype.entity_recognition import spotlight
from prototype.lib import article_repo
from prototype.lib import flags
import sys
import time
import subprocess
import datetime

import random

spotlight_port = None
spotlight_process = None
spotlight_address = None

def launch_spotlight():
    global spotlight_port
    global spotlight_process
    global spotlight_address

    print("Starting Spotlight server")

    spotlight_port = 2222 + random.randint(0, 100)

    # Tell Java launcher script which Java path to use explicitly.
    # Otherwise, it would default to the Java of the Bazel installation,
    # which is probably a broken symlink anywhere but on the machine
    # Bazel is running on.
    env = dict(os.environ)
    env['JAVABIN'] = '/packages/run/jdk-8/current/bin/java'
    spotlight_process = subprocess.Popen([
        'prototype/entity_recognition/spotlight_server',
        str(spotlight_port),
    ], env=env)
    spotlight_address = "http://localhost:%d/rest/annotate" % spotlight_port

    # TODO: Timeout after some time.

    wait_seconds = 60

    while True:
        assert spotlight_process.returncode is None, "Spotlight server died"

        try:
            client = spotlight.SpotlightClient(spotlight_address)
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

def main():
    start = datetime.datetime.now()

    flags.add_argument('--articles', action='append')
    flags.add_argument('--force_redo')
    flags.make_parser(description='Look up articles in Spotlight')
    args = flags.parse_args()

    launch_spotlight()
    print("Spotlight launched in", (datetime.datetime.now() - start))

    # TODO: skip if finished

    spotlight_client = spotlight.SpotlightClient(spotlight_address)
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

    print("Terminating Spotlight...")
    spotlight_process.terminate()
    time.sleep(5)
    print("Killing Spotlight...")
    spotlight_process.kill()
    spotlight_process.wait()
    print("Joined. Done.")

    print("Finished %d articles in" % len(args.articles), (datetime.datetime.now() - start))
    print('not_exist:', not_exist)
    print('already_done:', already_done)
    print('empty:', empty)

if __name__ == '__main__':
    main()
