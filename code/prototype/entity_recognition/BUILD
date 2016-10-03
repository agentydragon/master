py_binary(
    name = "entity_recognition",
    srcs = [
        "entity_recognition.py",
    ],
    deps = [
        ":spotlight_lib",
        "//:paths_lib",
        "//prototype/lib:article_repo_lib",
    ],
)

py_binary(
    name = "launch",
    srcs = [
        "launch.py",
    ],
    data = [
        ":entity_recognition",
        "//prototype/lib:mapper_lib",
        "//prototype/lib:article_set_lib",
        "//prototype/lib:flags_lib",
    ],
)

py_library(
    name = "spotlight_lib",
    #srcs_version = "PY3",
    srcs = [
        "spotlight.py",
    ],
    deps = [
        "//prototype/lib:zk_lib",
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
        "//prototype/lib:pbs_util_lib",
        "//prototype/lib:flags_lib",
        "//prototype/lib:zk_lib",
        "//:paths_lib",
    ],
    data = [
        "@cpulimit//:cpulimit_bin",
        ":spotlight",
    ]
)

java_binary(
    name = "spotlight",
    srcs = [
        "Spotlight.java",
    ],
    main_class = "Spotlight",
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
