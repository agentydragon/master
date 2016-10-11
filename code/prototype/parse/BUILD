java_binary(
    name = "parse",
    srcs = [
        "Parse.java",
    ],
    main_class = "Parse",
    deps = [
        ":CoreNLPInterface",
        "//prototype/lib:ArticleRepository",
        "//:org_json_json",
    ],
)

py_binary(
    name = "launch",
    srcs = [
        "launch.py",
    ],
    deps = [
        "//prototype/lib:mapper_lib",
        "//prototype/lib:flags_lib",
        "//prototype/lib:article_set_lib",
    ],
    data = [
        ":parse",
    ],
)

java_library(
    name = "CoreNLPInterface",
    srcs = [
        "CoreNLPInterface.java",
    ],
    deps = [
        "//:edu_stanford_nlp_stanford_corenlp",
        "@corenlp_models//jar",
        "@corenlp_srparser_model//jar",
    ],
    visibility = ["//visibility:public"],
)

java_binary(
    name = "CoreNLP",
    srcs = [
        "CoreNLP.java",
        "CoreNLPAnnotateMapper.java",
    ],
    main_class = "CoreNLP",
    deps = [
        ":CoreNLPInterface",
        "//:org_apache_hadoop_hadoop_common",
        "//:org_apache_hadoop_hadoop_mapreduce_client_core",
    ],
)
