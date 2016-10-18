py_binary(
    name = "predict",
    srcs = [
        "predict.py",
    ],
    deps = [
        ":prediction_lib",
        "//src/prototype/lib:article_set_lib",
        "//src/prototype/lib:sample_repo_lib",
        "//src/prototype/lib:flags_lib",
        "//src/prototype/lib:sample_generation_lib",
        "//src/prototype/lib:relations_lib",
        "//src/prototype/fusion:fuser_lib",
        "//src/prototype/extraction:feature_extraction_lib",
        "//src/prototype/extraction:model_lib",
    ],
)

py_binary(
    name = "evaluate",
    srcs = [
        "evaluate.py",
    ],
    deps = [
        ":prediction_lib",
        "//src/prototype/lib:flags_lib",
    ],
)

py_library(
    name = "prediction_lib",
    srcs = [
        "prediction.py",
    ],
)

py_binary(
    name = "add_labels",
    srcs = [
        "add_labels.py",
    ],
    deps = [
        ":prediction_lib",
        "//src/prototype/lib:flags_lib",
        "//src/prototype/lib:wikidata_lib",
    ],
)
