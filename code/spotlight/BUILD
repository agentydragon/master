java_binary(
    name = "Spotlight",
    srcs = [
        "Spotlight.java",
    ],
    main_class = "Spotlight",
    deps = [
        "@dbpedia_spotlight//jar",
        ":spotlight_extracted_model",
    ],
)

filegroup(
    name = "spotlight_extracted_model",
    srcs = [
        "en/fsa_dict.mem",
        "en/model.properties",
        "en/spotter_thresholds.txt",
        "en/stopwords.list",
        "en/README.txt",
        "en/model/candmap.mem",
        "en/model/context.mem",
        "en/model/quantized_counts.mem",
        "en/model/res.mem",
        "en/model/sf.mem",
        "en/model/tokens.mem",
    ],
)

genrule(
    name = "spotlight_models",
    srcs = [
        "@dbpedia_spotlight_model_en//file",
    ],
    cmd = "tar xpf $(location @dbpedia_spotlight_model_en//file) -C $(GENDIR)",
    outs = [
        "en/fsa_dict.mem",
        "en/model.properties",
        "en/spotter_thresholds.txt",
        "en/stopwords.list",
        "en/README.txt",
        "en/model/candmap.mem",
        "en/model/context.mem",
        "en/model/quantized_counts.mem",
        "en/model/res.mem",
        "en/model/sf.mem",
        "en/model/tokens.mem",
    ],
)
