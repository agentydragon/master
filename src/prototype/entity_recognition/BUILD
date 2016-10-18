py_binary(
    name = "entity_recognition",
    srcs = [
        "entity_recognition.py",
    ],
    deps = [
        ":spotlight_lib",
        "//src:paths_lib",
        "//src/prototype/lib:article_repo_lib",
    ],
    data = [
        ":spotlight_server",
    ],
)

py_binary(
    name = "launch",
    srcs = [
        "launch.py",
    ],
    data = [
        ":entity_recognition",
        "//src/prototype/lib:mapper_lib",
        "//src/prototype/lib:article_set_lib",
        "//src/prototype/lib:flags_lib",
    ],
)

py_library(
    name = "spotlight_lib",
    #srcs_version = "PY3",
    srcs = [
        "spotlight.py",
    ],
    deps = [
        "//src/prototype/lib:zk_lib",
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

py_binary(
    name = "launch_servers",
    default_python_version = "PY3",
    srcs_version = "PY3",
    srcs = [
        "launch_servers.py",
    ],
    deps = [
        ":spotlight_lib",
        "//src/prototype/lib:pbs_util_lib",
        "//src/prototype/lib:flags_lib",
        "//src/prototype/lib:zk_lib",
        "//src:paths_lib",
    ],
    data = [
        "@cpulimit//:cpulimit_bin",
        ":spotlight_server",
    ]
)

java_binary(
    name = "spotlight_server",
    srcs = [
        "SpotlightServer.java",
    ],
    main_class = "SpotlightServer",
    deps = [
        "@dbpedia_spotlight//jar",
    ],
    data = [
        ":spotlight_models",
    ],
)

genrule(
    name = "spotlight_models",
    srcs = [
        "@dbpedia_spotlight_model_en//file",
    ],
    cmd = ("tar xpf $(location @dbpedia_spotlight_model_en//file) " +
           "-C $(GENDIR)/prototype/entity_recognition"),
    outs = [
        "en/model.properties",
        "en/spotter_thresholds.txt",
        "en/stopwords.list",
        "en/model/candmap.mem",
        "en/model/context.mem",
        "en/model/res.mem",
        "en/model/res.mem_",
        "en/model/sf.mem",
        "en/model/tokens.mem",
        "en/opennlp/chunker.bin",
        "en/opennlp/pos-maxent.bin",
        "en/opennlp/sent.bin",
        "en/opennlp/token.bin",
    ],
)

java_binary(
    name = "SpotlightAnnotator",
    srcs = [
        "SpotlightAnnotator.java",
        "SpotlightAnnotatorMapper.java",
    ],
    main_class = "SpotlightAnnotator",
    deps = [
        ":SpotlightConnection",
        "//src/prototype/lib:ArticlesTable",
        "//:org_apache_hadoop_hadoop_common",
        "//:org_apache_hadoop_hadoop_mapreduce_client_core",
        "//:org_apache_hbase_hbase_common",
        "//:org_apache_hbase_hbase_client",
        "//:org_apache_hbase_hbase_server",
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

sh_binary(
    name = "run_on_hadoop",
    srcs = [
        "run_on_hadoop.sh",
    ],
    data = [
        ":SpotlightAnnotator_deploy.jar",
        ":SpotlightAnnotator.jar",
    ],
)
