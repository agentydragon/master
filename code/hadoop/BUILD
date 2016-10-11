package(default_visibility = ["//visibility:public"])

java_binary(
    name = "WikiSplit",
    srcs = [
        "WikiSplit.java",
        "ArticleSplitterMapper.java",
    ],
    main_class = "WikiSplit",
    deps = [
        "//:org_apache_hadoop_hadoop_common",
        "//:org_apache_hadoop_hadoop_mapreduce_client_core",
        "//:org_apache_hbase_hbase_common",
        "//:org_apache_hbase_hbase_client",
        "//:org_apache_hbase_hbase_server",
    ],
)

java_binary(
    name = "TestHBase",
    srcs = [
        "TestHBase.java",
    ],
    main_class = "TestHBase",
    deps = [
        "//:org_apache_hadoop_hadoop_common",
        "//:org_apache_hbase_hbase_common",
        "//:org_apache_hbase_hbase_client",
        "//:org_apache_hbase_hbase_server",
    ],
)

java_library(
    name = "RandomSelectorMapper",
    srcs = [
        "RandomSelectorMapper.java",
    ],
    deps = [
        "//:org_apache_hadoop_hadoop_common",
        "//:org_apache_hadoop_hadoop_mapreduce_client_core",
    ],
)

java_binary(
    name = "RandomSelector",
    srcs = [
        "RandomSelector.java",
    ],
    main_class = "RandomSelector",
    deps = [
        ":RandomSelectorMapper",
        "//:org_apache_hadoop_hadoop_common",
        "//:org_apache_hadoop_hadoop_mapreduce_client_core",
    ],
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
    name = "WikidataClientTest",
    srcs = [
        "WikidataClientTest.java",
    ],
    deps = [
        ":WikidataClient",
    ],
    test_class = "WikidataClientTest",
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

java_library(
    name = "Relations",
    srcs = [
        "Relations.java",
    ],
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

java_binary(
    name = "DocumentProcessor",
    srcs = [
        "DocumentProcessor.java",
    ],
    main_class = "DocumentProcessor",
    deps = [
        ":DocumentProcessorMapper",
        "//:org_apache_hadoop_hadoop_common",
        "//:org_apache_hadoop_hadoop_mapreduce_client_core",
        "//:commons_io_commons_io",
    ],
)

java_library(
    name = "DocumentProcessorMapper",
    srcs = [
        "DocumentProcessorMapper.java",
    ],
    deps = [
        ":SpotlightConnection",
        "//prototype/parse:CoreNLPInterface",
        "//:org_apache_hadoop_hadoop_common",
        "//:org_apache_hadoop_hadoop_mapreduce_client_core",
        "//:org_json_json",
    ],
)

java_binary(
    name = "SpotlightAnnotator",
    srcs = [
        "SpotlightAnnotator.java",
    ],
    main_class = "SpotlightAnnotator",
    deps = [
        ":SpotlightConnection",
        "//:org_apache_hadoop_hadoop_common",
        "//:org_apache_hadoop_hadoop_mapreduce_client_core",
    ],
)

java_library(
    name = "SpotlightConnection",
    srcs = [
        "SpotlightConnection.java",
        "SpotlightSingleConnection.java",
        "SpotlightPooledConnection.java",
    ],
)

java_binary(
    name = "CoreNLP",
    srcs = [
        "CoreNLP.java",
    ],
    main_class = "CoreNLP",
    deps = [
        "//:org_apache_hadoop_hadoop_common",
        "//:org_apache_hadoop_hadoop_mapreduce_client_core",
        "//prototype/parse:CoreNLPInterface",
    ],
)
