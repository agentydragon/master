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
        "//py:paths_lib",
        "//py:wikidata_lib",
        ":sample_generation_lib",
    ],
)

py_binary(
    name = "launch",
    srcs = [
        "launch.py",
    ],
    deps = [
        "//py:pbs_util_lib",
        "//py:paths_lib",
        "//py:file_util_lib",
    ],
    data = [
        ":make_training_samples",
    ],
    default_python_version = "PY3",
    srcs_version = "PY3",
)

py_library(
    name = "sample_generation_lib",
    srcs = [
        "sample_generation.py",
    ],
    deps = [
        "//py:paths_lib",
        "//py:dbpedia_lib",
        "//prototype/lib:training_sample_lib",
        "//prototype/lib:parse_xmls_to_protos_lib",
    ]
)

py_binary(
    name = "make_negative_samples",
    srcs = [
        "make_negative_samples.py",
    ],
    deps = [
        "//prototype/lib:sample_repo_lib",
        ":sample_generation_lib",
        "//py:wikidata_lib",
    ],
)

py_binary(
    name = "join_positives",
    srcs = [
        "join_positives.py",
    ],
    deps = [
        "//prototype/lib:sample_repo_lib",
    ],
)
