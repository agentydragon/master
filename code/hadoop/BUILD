package(default_visibility = ["//visibility:public"])

java_binary(
    name = "WikiSplit",
    srcs = [
        "WikiSplit.java",
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
    name = "CoreNLPInterface",
    srcs = [
        "CoreNLPInterface.java",
    ],
    deps = [
        "//:edu_stanford_nlp_stanford_corenlp",
        # TODO: must be installed separately
        "@corenlp_models//jar",
        "@corenlp_srparser_model//jar",
        # TODO: what about models?
        # "//:org_apache_hadoop_hadoop_mapreduce_client_core",
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
        ":CoreNLPInterface",
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
    name = "ParseXmlsToProtos",
    srcs = [
        "ParseXmlsToProtos.java",
        "//:Sentence.java",
    ],
    deps = [
        "//:com_google_protobuf_protobuf_java",
        "@javax_xml_parsers_jaxp_api//jar",
    ],
)

java_library(
    name = "AnnotateCoreferences",
    srcs = [
        "AnnotateCoreferences.java",
        "//:Sentence.java",
    ],
    deps = [
        ":DBpediaClient",
        "//:com_google_protobuf_protobuf_java",
        "//:org_json_json",
        "//:log4j_log4j",
    ],
)

java_library(
    name = "Relations",
    srcs = [
        "Relations.java",
    ],
)

java_library(
    name = "GetTrainingSamples",
    srcs = [
        "GetTrainingSamples.java",
        "//:Sentence.java",
        "//:TrainingSamples.java",
    ],
    deps = [
        "//:com_google_protobuf_protobuf_java",
        "//:org_json_json",
        ":WikidataClient",
        ":Relations",
        "//:log4j_log4j",
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

java_test(
    name = "ParseXmlsToProtosTest",
    srcs = [
        "ParseXmlsToProtosTest.java",
        "//:Sentence.java",
    ],
    deps = [
        ":ParseXmlsToProtos",
        "//:com_google_protobuf_protobuf_java",
        "@javax_xml_parsers_jaxp_api//jar",
    ],
    data = [
        "//testdata:Obama.txt.out",
        "//testdata:Obama.txt",
    ],
    test_class = "ParseXmlsToProtosTest",
)

java_library(
    name = "GenerateTrainingSamplesMapper",
    srcs = [
        "GenerateTrainingSamplesMapper.java",
        "//:Sentence.java",
        "//:TrainingSamples.java",
    ],
    deps = [
        "//:org_apache_hadoop_hadoop_common",
        "//:org_apache_hadoop_hadoop_mapreduce_client_core",
        "//:org_json_json",
        ":WikidataClient",
        ":GetTrainingSamples",
        ":AnnotateCoreferences",
        ":ParseXmlsToProtos",
    ]
)

java_test(
    name = "GenerateTrainingSamplesMapperTest",
    srcs = [
        "GenerateTrainingSamplesMapperTest.java",
    ],
    deps = [
        ":GenerateTrainingSamplesMapper",
        ":WikidataClient",
        ":DocumentProcessorMapper",
        ":ParseXmlsToProtos",
        "//:log4j_log4j",
    ],
    data = [
        "//testdata:tharde.json",
        "//testdata:obama-short.json",
    ],
    test_class = "GenerateTrainingSamplesMapperTest",
    timeout = "eternal",
)

java_binary(
    name = "GenerateTrainingSamples",
    srcs = [
        "GenerateTrainingSamples.java",
    ],
    main_class = "GenerateTrainingSamples",
    deps = [
        ":GenerateTrainingSamplesMapper",
        "//:org_apache_hadoop_hadoop_common",
        "//:org_apache_hadoop_hadoop_mapreduce_client_core",
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
        "//:edu_stanford_nlp_stanford_corenlp",
        "//:commons_io_commons_io",
        # TODO: must be installed separately
        "@corenlp_models//jar",
        "@corenlp_srparser_model//jar",
    ],
)

java_library(
    name = "DocumentProcessorMapper",
    srcs = [
        "DocumentProcessorMapper.java",
    ],
    deps = [
        ":SpotlightConnection",
        "//:org_apache_hadoop_hadoop_common",
        "//:org_apache_hadoop_hadoop_mapreduce_client_core",
        "//:edu_stanford_nlp_stanford_corenlp",
        # TODO: must be installed separately
        "@corenlp_models//jar",
        "@corenlp_srparser_model//jar",
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
