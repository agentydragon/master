py_binary(
    name = "metacentrum_get_training_samples",
    srcs = [
        "metacentrum_get_training_samples.py",
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
