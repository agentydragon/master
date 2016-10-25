py_binary(
    name = "train_classifiers",
    srcs = [
        "train_classifiers.py",
    ],
    deps = [
        "//src:paths_lib",
        "//src/prototype/extraction:feature_extraction_lib",
        "//src/prototype/extraction:model_lib",
        "//src/prototype/lib:plot_lib",
        "//src/prototype/lib:file_util_lib",
        "//src/prototype/lib:sample_repo_lib",
        "//src/prototype/lib:wikidata_lib",
    ],
    default_python_version = "PY3",
    srcs_version = "PY3",
)

py_binary(
    name = "launch",
    srcs = [
        "launch.py",
    ],
    deps = [
        "//src/prototype/lib:sample_repo_lib",
        "//src/prototype/lib:mapper_lib",
        "//src/prototype/lib:relations_lib",
        "//src/prototype/lib:wikidata_lib",
    ],
    data = [
        ":train_classifiers",
    ],
    default_python_version = "PY3",
    srcs_version = "PY3",
)
