py_binary(
    name = "train_classifiers",
    srcs = [
        "train_classifiers.py",
    ],
    deps = [
        "//prototype/lib:sample_repo_lib",
        "//prototype/lib:feature_extraction_lib",
        "//prototype/lib:wikidata_lib",
        "//:paths_lib",
        "//py:file_util_lib",
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
        "//prototype/lib:sample_repo_lib",
        "//prototype/lib:mapper_lib",
    ],
    data = [
        ":train_classifiers",
    ],
    default_python_version = "PY3",
    srcs_version = "PY3",
)
