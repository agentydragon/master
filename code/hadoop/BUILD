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

java_binary(
    name = "SpotlightAnnotator",
    srcs = [
        "SpotlightAnnotator.java",
    ],
    main_class = "SpotlightAnnotator",
    deps = [
        ":SpotlightServer",
        #"//:org_apache_hadoop_hadoop_common",
        #"//:org_apache_hadoop_hadoop_mapreduce_client_core",
    ],
)

java_library(
    name = "SpotlightServer",
    srcs = [
        "SpotlightServer.java",
    ],
    deps = [
    #    "@org_apache_httpcomponents_httpclient//jar",
    #    "@org_apache_httpcomponents_httpcore//jar",
    ],
    data = [
        "//spotlight:Spotlight",  # this binary is launched
    ],
)

java_binary(
    name = "CoreNLPViaQsub",
    srcs = [
        "CoreNLPViaQsub.java",
    ],
    main_class = "CoreNLPViaQsub",
    deps = [
        "//:org_apache_hadoop_hadoop_common",
        "//:org_apache_hadoop_hadoop_mapreduce_client_core",
    ],
)
