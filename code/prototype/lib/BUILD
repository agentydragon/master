package(default_visibility = ["//visibility:public"])

py_library(
    name = "flags_lib",
    srcs = [
        "flags.py",
    ],
)

py_library(
    name = "zk_lib",
    srcs = [
        "zk.py",
    ],
    deps = [
        ":flags_lib",
    ],
)

py_library(
    name = "file_util_lib",
    srcs = [
        "file_util.py",
    ],
)

py_library(
    name = "article_set_lib",
    srcs = [
        "article_set.py",
    ],
    deps = [
        "//:paths_lib",
    ],
)

py_library(
    name = "article_repo_lib",
    srcs = [
        "article_repo.py",
    ],
    deps = [
        "//:paths_lib",
        ":file_util_lib",
        ":flags_lib",
        ":sentence_lib",
    ],
)

py_library(
    name = "sample_repo_lib",
    srcs = [
        "sample_repo.py",
    ],
    deps = [
        "//:paths_lib",
        ":article_repo_lib",
        ":training_sample_lib",
        ":file_util_lib",
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
        "//:paths_java_lib",
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
        ":zk_lib",
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
        ":zk_lib",
    ],
)

py_test(
    name = "parse_xmls_to_protos_test",
    srcs = [
        "parse_xmls_to_protos_test.py",
    ],
    deps = [
        ":parse_xmls_to_protos_lib",
        ":dbpedia_lib",
        ":sentence_lib",
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
        "//:paths_lib",
        ":dbpedia_lib",
        ":training_sample_lib",
        ":relations_lib",
    ],
)

py_library(
    name = "mapper_lib",
    srcs = [
        "mapper.py",
    ],
    deps = [
        "//:paths_lib",
        ":file_util_lib",
        ":pbs_util_lib",
    ],
)

py_library(
    name = "pbs_util_lib",
    #srcs_version = "PY3",
    srcs = [
        "pbs_util.py",
    ],
)

py_library(
    name = "wikidata_lib",
    srcs = [
        "wikidata.py",
    ],
    deps = [
        ":sparql_client_lib",
        ":wikidata_util_lib",
        ":zk_lib",
        ":flags_lib",
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
        ":zk_lib",
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
    deps = [
        ":flags_lib",
    ],
    #srcs_version = "PY3",
)

py_library(
    name = "plot_lib",
    srcs = [
        "plot.py",
    ],
    deps = [
	"//:paths_lib",
    ],
)

py_library(
    name = "spotlight_lib",
    #srcs_version = "PY3",
    srcs = [
        "spotlight.py",
    ],
    deps = [
        ":zk_lib",
    ],
)

py_library(
    name = "relations_lib",
    srcs = [
        "relations.py",
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
    srcs_version = "PY3",
    default_python_version = "PY3",
)

py_test(
    name = "article_repo_test",
    srcs = [
        "article_repo_test.py",
    ],
    deps = [
        ":article_repo_lib",
    ],
    srcs_version = "PY3",
    default_python_version = "PY3",
)
