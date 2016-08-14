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
        "@corenlp_models//jar",
        # TODO: what about models?
        # "//:org_apache_hadoop_hadoop_mapreduce_client_core",
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
