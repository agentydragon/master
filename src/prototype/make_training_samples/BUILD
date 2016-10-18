py_binary(
    name = "make_training_samples",
    srcs = [
        "make_training_samples.py",
    ],
    deps = [
        "//src/prototype/lib:article_repo_lib",
        "//src/prototype/lib:sample_repo_lib",
        "//src/prototype/lib:wikidata_lib",
        "//src/prototype/lib:sample_generation_lib",
        "//src/prototype/lib:zk_lib",
        "//src:paths_lib",
    ],
    visibility = ["//visibility:public"]
)

py_binary(
    name = "launch",
    srcs = [
        "launch.py",
    ],
    deps = [
        "//src:paths_lib",
        "//src/prototype/lib:file_util_lib",
        "//src/prototype/lib:mapper_lib",
        "//src/prototype/lib:article_set_lib",
        "//src/prototype/lib:zk_lib",
    ],
    data = [
        ":make_training_samples",
    ],
    default_python_version = "PY3",
    srcs_version = "PY3",
)
