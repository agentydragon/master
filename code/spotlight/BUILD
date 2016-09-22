py_binary(
    name = "launch_spotlight_servers",
    default_python_version = "PY3",
    srcs_version = "PY3",
    srcs = [
        "launch_spotlight_servers.py",
    ],
    deps = [
        "//prototype/lib:spotlight_lib",
        "//py:pbs_util_lib",
        "//:paths_lib",
    ],
    data = [
        ":Spotlight",
    ]
)

java_binary(
    name = "Spotlight",
    srcs = [
        "Spotlight.java",
    ],
    main_class = "Spotlight",
    deps = [
        "@dbpedia_spotlight//jar",
        # ":spotlight_extracted_model",
    ],
    data = [
        ":spotlight_models",
    ],
    visibility = ["//visibility:public"],
)

java_binary(
    name = "SpotlightAnnotator",
    srcs = [
        "SpotlightAnnotator.java",
    ],
    main_class = "SpotlightAnnotator",
    deps = [
        "//:org_apache_hadoop_hadoop_common",
        "//:org_apache_hadoop_hadoop_mapreduce_client_core",
        ":SpotlightServer",
    ],
    data = [
        ":spotlight_models",
    ],
)

java_library(
    name = "SpotlightServer",
    srcs = [
        "SpotlightServer.java",
    ],
    deps = [
        "@dbpedia_spotlight//jar",
    ],
)

filegroup(
    name = "spotlight_extracted_model",
    srcs = [
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

genrule(
    name = "spotlight_models",
    srcs = [
        "@dbpedia_spotlight_model_en//file",
    ],
    cmd = "tar xpf $(location @dbpedia_spotlight_model_en//file) -C $(GENDIR)/spotlight",
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
