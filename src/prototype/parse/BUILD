java_binary(
    name = "parse",
    srcs = [
        "Parse.java",
    ],
    main_class = "Parse",
    deps = [
        ":CoreNLPInterface",
        "//src/prototype/lib:ArticleRepository",
        "//:org_json_json",
    ],
)

py_binary(
    name = "launch",
    srcs = [
        "launch.py",
    ],
    deps = [
        "//src/prototype/lib:mapper_lib",
        "//src/prototype/lib:flags_lib",
        "//src/prototype/lib:article_set_lib",
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
        "//src/prototype/lib:ArticlesTable",
        "//:org_apache_hadoop_hadoop_common",
        "//:org_apache_hadoop_hadoop_mapreduce_client_core",
        "//:org_apache_hbase_hbase_common",
        "//:org_apache_hbase_hbase_client",
        "//:org_apache_hbase_hbase_server",
    ],
)

sh_binary(
    name = "run_on_hadoop",
    srcs = [
        "run_on_hadoop.sh",
    ],
    data = [
        ":CoreNLP_deploy.jar",
        ":CoreNLP.jar",
    ],
)
