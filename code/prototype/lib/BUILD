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

java_library(
    name = "ArticlesTable",
    srcs = [
        "ArticlesTable.java",
    ],
    deps = [
        "//:org_apache_hbase_hbase_common",
    ],
)

java_library(
    name = "SavedDocument",
    srcs = [
        "SavedDocument.java",
    ],
    deps = [
        ":ArticlesTable",
        "//:org_json_json",
        "//:org_apache_hbase_hbase_common",
        "//:org_apache_hbase_hbase_client",
    ],
)

py_library(
    name = "training_sample_lib",
    srcs = [
        "training_sample.py",
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
    data = [
        "@cpulimit//:cpulimit_bin",
    ],
)

py_library(
    name = "pbs_util_lib",
    #srcs_version = "PY3",
    srcs = [
        "pbs_util.py",
    ],
    deps = [
        "//:paths_lib",
        ":file_util_lib",
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
    name = "relations_lib",
    srcs = [
        "relations.py",
    ],
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

java_library(
    name = "DBpediaClient",
    srcs = [
        "DBpediaClient.java",
    ],
    deps = [
        "//:org_apache_jena_jena_core",
        "//:org_apache_jena_jena_base",
        "//:org_apache_jena_jena_arq",
        # NOTE: undeclared deps >[
        "//:org_apache_httpcomponents_httpcore",
        "//:org_apache_httpcomponents_httpclient",
    ],
)

java_test(
    name = "DBpediaClientTest",
    srcs = [
        "DBpediaClientTest.java",
    ],
    deps = [
        ":DBpediaClient",
    ],
    test_class = "DBpediaClientTest",
)

java_test(
    name = "WikidataClientTest",
    srcs = [
        "WikidataClientTest.java",
    ],
    deps = [
        ":WikidataClient",
    ],
    test_class = "WikidataClientTest",
)

java_library(
    name = "WikidataClient",
    srcs = [
        "WikidataClient.java",
    ],
    deps = [
        "//:org_apache_jena_jena_core",
        "//:org_apache_jena_jena_base",
        "//:org_apache_jena_jena_arq",
        # NOTE: undeclared deps >[
        "//:org_apache_httpcomponents_httpcore",
        "//:org_apache_httpcomponents_httpclient",
    ],
)
