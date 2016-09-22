package(default_visibility = ["//visibility:public"])

py_library(
    name = "article_repo_lib",
    srcs = [
        "article_repo.py",
    ],
    deps = [
        "//py:file_util_lib",
    ],
)

py_library(
    name = "sample_repo_lib",
    srcs = [
        "sample_repo.py",
    ],
    deps = [
        ":article_repo_lib",
        ":training_sample_lib",
        "//py:file_util_lib",
    ],
)

java_library(
    name = "ArticleRepository",
    srcs = [
        "ArticleRepository.java",
    ],
    deps = [
        "//:commons_io_commons_io",
        "//:org_json_json",
    ],
)

java_library(
    name = "SampleRepository",
    srcs = [
        "SampleRepository.java",
        "//:TrainingSamples.java",
    ],
    deps = [
        "//:commons_io_commons_io",
        "//:org_json_json",
        "//:com_google_protobuf_protobuf_java",
    ],
)

py_library(
    name = "sentence_lib",
    srcs = [
        "sentence.py",
    ],
)

py_library(
    name = "training_sample_lib",
    srcs = [
        "training_sample.py",
    ],
)

py_library(
    name = "parse_xmls_to_protos_lib",
    srcs = [
        "parse_xmls_to_protos.py",
        #"//:sentence_pb2.py",
        ":dbpedia_lib",
    ],
    deps = [
        ":sentence_lib",
    ],
)

py_library(
    name = "dbpedia_lib",
    srcs = [
        "dbpedia.py",
    ],
    deps = [
        #":json_cache_lib",
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

py_test(
    name = "parse_xmls_to_protos_test",
    srcs = [
        "parse_xmls_to_protos_test.py",
    ],
    deps = [
        ":parse_xmls_to_protos_lib",
    ],
    data = [
        "//testdata:Obama.txt",
        "//testdata:Obama.txt.out",
        "//testdata:Obama.spotlight.json",
    ],
    srcs_version = "PY3",
    default_python_version = "PY3",
)

py_library(
    name = "sample_generation_lib",
    srcs = [
        "sample_generation.py",
    ],
    deps = [
        "//py:paths_lib",
        ":dbpedia_lib",
        ":training_sample_lib",
        ":parse_xmls_to_protos_lib",
    ],
)

py_library(
    name = "mapper_lib",
    srcs = [
        "mapper.py",
    ],
    deps = [
        "//py:paths_lib",
        "//py:file_util_lib",
        "//py:pbs_util_lib",
    ],
)

py_library(
    name = "feature_extraction_lib",
    srcs = [
        "feature_extraction.py",
    ],
    deps = [
    ],
)

py_library(
    name = "wikidata_lib",
    srcs = [
        "wikidata.py",
    ],
    deps = [
        # ":json_cache_lib",
        ":sparql_client_lib",
        ":wikidata_util_lib",
    ],
    #srcs_version = "PY3",
)

py_test(
    name = "wikidata_test",
    srcs = [
        "wikidata_test.py",
    ],
    deps = [
        ":wikidata_lib",
    ],
    srcs_version = "PY3",
    default_python_version = "PY3",
)

py_library(
    name = "wikidata_util_lib",
    srcs = [
        "wikidata_util.py",
    ],
    #srcs_version = "PY3",
)

py_library(
    name = "sparql_client_lib",
    srcs = [
        "sparql_client.py",
    ],
    #srcs_version = "PY3",
)
