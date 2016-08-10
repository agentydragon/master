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

sh_binary(
    name = "metacentrum_get_training_samples",
    srcs = [
        "metacentrum_get_training_samples.sh",
    ],
    deps = [
        ":common",
    ],
    data = [
        ":get_training_samples_main",
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

sh_library(
    name = "common",
    srcs = [
        "common.sh",
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
    name = "file_util_lib",
    srcs = [
        "file_util.py",
    ],
)

py_library(
    name = "paths_lib",
    srcs = [
        "paths.py",
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
    name = "metacentrum_spotlight_main",
    srcs = [
        "metacentrum_spotlight_main.py",
    ],
    deps = [
        ":spotlight_lib",
        ":paths_lib",
    ]
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

sh_binary(
    name = "annotate_coreferences",
    srcs = [
        "annotate_coreferences.sh",
    ],
    data = [
        ":annotate_coreferences_main",
    ],
    deps = [
        ":common",
    ],
)

py_library(
    name = "annotate_coreferences_lib",
    srcs = [
        "annotate_coreferences.py",
        "sentence_pb2.py",
    ],
    deps = [
        ":dbpedia_lib",
    ],
)

py_binary(
    name = "annotate_coreferences_main",
    srcs = [
        "annotate_coreferences_main.py",
    ],
    deps = [
        ":annotate_coreferences_lib",
        ":paths_lib",
        ":file_util_lib",
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

genrule(
    name = "sentence_proto",
    srcs = [
        "sentence.proto",
    ],
    outs = [
        "sentence_pb2.py",
    ],
    cmd = "protoc -I=. --python_out=$(GENDIR)/ $(location :sentence.proto)"
)

genrule(
    name = "training_samples_proto",
    srcs = [
        "training_samples.proto",
    ],
    outs = [
        "training_samples_pb2.py",
    ],
    cmd = "protoc -I=. --python_out=$(GENDIR)/ $(location :training_samples.proto)"
)

sh_binary(
    name = "nlpize_articles",
    srcs = [
        "nlpize_articles.sh",
    ],
    deps = [
        ":common",
    ],
    data = [
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

py_binary(
    name = "launch_nlpize_articles_main",
    srcs = [
        "launch_nlpize_articles_main.py",
    ],
    deps = [
        ":file_util_lib",
        ":paths_lib",
        ":nlpize_articles_main",
    ],
)

py_test(
    name = "annotate_coreferences_test",
    srcs = [
        "annotate_coreferences_test.py",
    ],
    deps = [
        ":get_training_samples_lib",
        ":annotate_coreferences_lib",
        ":parse_xmls_to_protos_lib",
    ],
)

py_library(
    name = "parse_xmls_to_protos_lib",
    srcs = [
        "parse_xmls_to_protos.py",
        "sentence_pb2.py",
    ],
)

py_binary(
    name = "parse_xmls_to_protos_main",
    srcs = [
        "parse_xmls_to_protos_main.py",
    ],
    deps = [
        ":parse_xmls_to_protos_lib",
    ],
)
