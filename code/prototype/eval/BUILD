py_binary(
    name = "predict",
    srcs = [
        "predict.py",
    ],
    deps = [
        "//prototype/lib:article_set_lib",
        "//prototype/lib:sample_repo_lib",
        "//prototype/lib:flags_lib",
        "//prototype/lib:sample_generation_lib",
        "//prototype/lib:relations_lib",
        "//prototype/lib:wikidata_lib",
        "//prototype/fusion:fuser_lib",
        "//prototype/extraction:feature_extraction_lib",
        "//prototype/extraction:model_lib",
    ],
)

py_binary(
    name = "evaluate",
    srcs = [
        "evaluate.py",
    ],
    deps = [
        "//prototype/lib:flags_lib",
    ],
)
