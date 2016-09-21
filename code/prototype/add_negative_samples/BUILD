py_binary(
    name = "add_negative_samples",
    srcs = [
        "add_negative_samples.py",
    ],
    deps = [
        "//prototype/lib:sample_repo_lib",
        "//prototype/lib:sample_generation_lib",
        "//py:wikidata_lib",
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
        ":add_negative_samples",
    ],
    default_python_version = "PY3",
    srcs_version = "PY3",
)
