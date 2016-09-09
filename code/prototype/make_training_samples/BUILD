#java_binary(
#    name = "make_training_samples",
#    srcs = [
#        "MakeTrainingSamples.java",
#    ],
#    main_class = "MakeTrainingSamples",
#    deps = [
#        "//prototype:ArticleRepository",
#        "//prototype:SampleRepository",
#        "//:org_json_json",
#        "//hadoop:GenerateTrainingSamples",
#        "//hadoop:WikidataClient",
#        "//:log4j_log4j",
#    ],
#)

py_binary(
    name = "make_training_samples",
    srcs = [
        "make_training_samples.py",
    ],
    deps = [
        "//prototype/lib:article_repo_lib",
        "//prototype/lib:sample_repo_lib",
        "//prototype/lib:parse_xmls_to_protos_lib",
        "//py:paths_lib",
        "//py:wikidata_lib",
    ],
)
