py_binary(
    name = "make_training_samples",
    srcs = [
        "make_training_samples.py",
    ],
    deps = [
        "//prototype/lib:article_repo_lib",
        "//prototype/lib:sample_repo_lib",
        "//prototype/lib:wikidata_lib",
        "//prototype/lib:sample_generation_lib",
        "//prototype/lib:zk_lib",
        "//:paths_lib",
    ],
)

py_binary(
    name = "launch",
    srcs = [
        "launch.py",
    ],
    deps = [
        "//:paths_lib",
        "//prototype/lib:file_util_lib",
        "//prototype/lib:mapper_lib",
    ],
    data = [
        ":make_training_samples",
    ],
    default_python_version = "PY3",
    srcs_version = "PY3",
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
