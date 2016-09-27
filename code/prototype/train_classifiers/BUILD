py_binary(
    name = "train_classifiers",
    srcs = [
        "train_classifiers.py",
    ],
    deps = [
        "//:paths_lib",
        "//prototype:feature_extraction_lib",
        "//prototype/lib:file_util_lib",
        "//prototype/lib:sample_repo_lib",
        "//prototype/lib:wikidata_lib",
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
        "//prototype/lib:relations_lib",
    ],
    data = [
        ":train_classifiers",
        "@cpulimit//:cpulimit_bin",
    ],
    default_python_version = "PY3",
    srcs_version = "PY3",
)
