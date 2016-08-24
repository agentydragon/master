java_binary(
    name = "WikiSplit",
    srcs = [
        "WikiSplit.java",
    ],
    main_class = "WikiSplit",
    deps = [
        "//:org_apache_hadoop_hadoop_common",
        "//:org_apache_hadoop_hadoop_mapreduce_client_core",
    ],
)

# genrule(
#     name = "processed_document_proto",
#     srcs = [
#         "processed_document.proto",
#     ],
#     outs = [
#         "ProcessedDocument.java",
#     ],
#     cmd = "protoc -I=. " +
#         "--java_out=$(GENDIR)/ " +
#         "$(location :processed_document.proto)"
# )

java_binary(
    name = "CoreNLP",
    srcs = [
        "CoreNLP.java",
    ],
    main_class = "CoreNLP",
    deps = [
        "//:org_apache_hadoop_hadoop_common",
        "//:org_apache_hadoop_hadoop_mapreduce_client_core",
        "//:edu_stanford_nlp_stanford_corenlp",
        # TODO: must be installed separately
        "@corenlp_models//jar",
        "@corenlp_srparser_model//jar",
        # TODO: what about models?
        # "//:org_apache_hadoop_hadoop_mapreduce_client_core",
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
    ],
    deps = [
        "//:org_apache_hadoop_hadoop_common",
        "//:org_apache_hadoop_hadoop_mapreduce_client_core",
        "//:org_json_json",
    ]
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

java_test(
    name = "SpotlightServerTest",
    srcs = [
        "SpotlightServerTest.java",
    ],
    deps = [
        ":SpotlightServer",
    ],
)

java_library(
    name = "SpotlightServer",
    srcs = [
        "SpotlightServer.java",
    ],
    data = [
        "//spotlight:Spotlight",  # this binary is launched
    ],
)

java_library(
    name = "SpotlightConnection",
    srcs = [
        "SpotlightConnection.java",
    ],
)
