java_binary(
    name = "make_training_samples",
    srcs = [
        "MakeTrainingSamples.java",
    ],
    main_class = "MakeTrainingSamples",
    deps = [
        "//prototype:ArticleRepository",
        "//prototype:SampleRepository",
        "//:org_json_json",
        "//hadoop:GenerateTrainingSamples",
        "//hadoop:WikidataClient",
        "//:log4j_log4j",
    ],
)
