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
    name = "get_training_samples_lib",
    srcs = [
        "get_training_samples.py",
    ],
    deps = [
        ":file_util_lib",
    ]
)

py_binary(
    name = "get_training_samples_main",
    srcs = [
        "get_training_samples_main.py",
        "get_training_samples.py",
        "sentence_pb2.py",
        "training_samples_pb2.py",
    ],
    deps = [
        ":wikidata_lib",
    ],
)

py_library(
    name = "wikidata_lib",
    srcs = [
        "wikidata.py",
        "json_cache.py",
        "wikidata_util.py",
        "sparql_client.py",
    ]
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
