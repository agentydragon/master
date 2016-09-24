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
    visibility = ["//visibility:public"],
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
