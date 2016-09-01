py_library(
    name = "split_wiki_lib",
    srcs = [
        "split_wiki.py",
    ],
    deps = [
        ":file_util_lib",
    ],
)

py_binary(
    name = "split_wiki_main",
    srcs = [
        "split_wiki_main.py",
    ],
    deps = [
        ":split_wiki_lib",
    ],
)

py_test(
    name = "split_wiki_test",
    srcs = [
        "split_wiki_test.py",
    ],
    deps = [
        ":split_wiki_lib",
    ],
)

py_binary(
    name = "launch_split_wiki_main",
    srcs = [
        "launch_split_wiki_main.py",
    ],
    deps = [
        ":split_wiki_main",
        ":file_util_lib",
        ":pbs_util_lib",
        ":paths_lib",
    ],
)

py_library(
    name = "paths_lib",
    srcs = [
        "paths.py",
    ],
)

py_library(
    name = "file_util_lib",
    srcs = [
        "file_util.py",
    ],
)

py_binary(
    name = "add_negative_samples_main",
    srcs = [
        "add_negative_samples_main.py",
        "get_training_samples.py",
        "sentence_pb2.py",
        "training_samples_pb2.py",
    ],
    deps = [
        ":wikidata_lib",
        ":file_util_lib",
    ],
)

py_library(
    name = "spotlight_lib",
    srcs = [
        "spotlight.py",
    ],
)

py_test(
    name = "spotlight_test",
    srcs = [
        "spotlight_test.py",
    ],
    deps = [
        ":spotlight_lib",
    ],
)

py_binary(
    name = "launch_nlpize_articles_main",
    srcs = [
        "launch_nlpize_articles_main.py",
    ],
    deps = [
        ":file_util_lib",
        ":paths_lib",
        ":pbs_util_lib",
        ":nlpize_articles_main",
    ],
)

py_binary(
    name = "nlpize_articles_main",
    srcs = [
        "nlpize_articles_main.py",
    ],
    deps = [
        ":file_util_lib",
        ":paths_lib",
    ],
)

sh_binary(
    name = "metacentrum_distant_supervision_train",
    srcs = [
        "metacentrum_distant_supervision_train.sh",
    ],
    deps = [
        ":common",
    ],
    data = [
        ":distant_supervision_train_main",
    ],
)

py_binary(
    name = "distant_supervision_train_main",
    srcs = [
        "distant_supervision_train_main.py",
        "training_samples_pb2.py",
    ],
    deps = [
        ":file_util_lib",
    ]
)

py_binary(
    name = "mr_generate_training_samples",
    srcs = [
        "mr_generate_training_samples.py",
    ],
    deps = [
        ":parse_xmls_to_protos_lib",
        ":annotate_coreferences_lib",
        ":get_training_samples_lib",
    ],
)

py_binary(
    name = "show_training_samples",
    srcs = [
        "show_training_samples.py",
        "training_samples_pb2.py",
    ],
    deps = [
        ":wikidata_lib",
    ],
)

py_library(
    name = "dbpedia_lib",
    srcs = [
        "dbpedia.py",
    ],
    deps = [
        ":json_cache_lib",
        ":sparql_client_lib",
        ":wikidata_util_lib",
    ],
)

py_test(
    name = "dbpedia_test",
    srcs = [
        "dbpedia_test.py",
    ],
    deps = [
        ":dbpedia_lib",
    ],
)

py_library(
    name = "get_training_samples_lib",
    srcs = [
        "get_training_samples.py",
        "sentence_pb2.py",
        "training_samples_pb2.py",
        "relations.py",
    ],
    deps = [
        ":file_util_lib",
    ]
)

py_binary(
    name = "get_training_samples_main",
    srcs = [
        "get_training_samples_main.py",
        "sentence_pb2.py",
    ],
    deps = [
        ":get_training_samples_lib",
        ":wikidata_lib",
        ":file_util_lib",
    ],
)

py_library(
    name = "json_cache_lib",
    srcs = [
        "json_cache.py",
    ],
    deps = [
        ":paths_lib",
        ":file_util_lib",
    ],
)

py_library(
    name = "sparql_client_lib",
    srcs = [
        "sparql_client.py",
    ],
)

py_library(
    name = "wikidata_util_lib",
    srcs = [
        "wikidata_util.py",
    ],
)

py_library(
    name = "wikidata_lib",
    srcs = [
        "wikidata.py",
    ],
    deps = [
        ":json_cache_lib",
        ":sparql_client_lib",
        ":wikidata_util_lib",
    ],
)

py_test(
    name = "wikidata_test",
    srcs = [
        "wikidata_test.py",
    ],
    deps = [
        ":wikidata_lib",
    ]
)

# TODO: I can make my own wiki2text! With blackjack and hookers!
# genrule(
#     name = "wiki2text",
#     srcs = [
#         "@wiki2text//:wiki2text.nim",
#     ],
#     outs = [
#         "wiki2text",
#     ],
#     cmd = "nim c -d:release --app:console $(location @wiki2text//:wiki2text.nim) && mv wiki2text $(GENDIR)"
# )

py_binary(
    name = "launch_get_training_samples_main",
    srcs = [
        "launch_get_training_samples_main.py",
    ],
    deps = [
        ":pbs_util_lib",
        ":paths_lib",
        ":get_training_samples_main",
    ],
)

py_library(
    name = "pbs_util_lib",
    srcs = [
        "pbs_util.py",
    ],
)

sh_binary(
    name = "metacentrum_add_negative_samples",
    srcs = [
        "metacentrum_add_negative_samples.sh",
    ],
    deps = [
        ":common",
    ],
    data = [
        ":add_negative_samples_main",
    ],
)

