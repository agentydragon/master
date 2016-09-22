py_binary(
    name = "find_persons",
    srcs = [
        "find_persons.py",
    ],
    deps = [
        "//prototype/lib:wikidata_lib",
    ],
    default_python_version = "PY3",
    srcs_version = "PY3",
)

py_binary(
    name = "data_stats",
    srcs = [
        "data_stats.py",
    ],
    deps = [
        "//prototype/lib:article_repo_lib",
        "//:paths_lib",
    ],
)

py_binary(
    name = "visualize",
    srcs = [
        "visualize.py",
    ],
    deps = [
        "//prototype/lib:article_repo_lib",
        "//prototype/lib:parse_xmls_to_protos_lib",
        "//:paths_lib",
    ],
    default_python_version = "PY3",
    srcs_version = "PY3",
)

py_binary(
    name = "visualize_relation",
    srcs = [
        "visualize_relation.py",
    ],
    deps = [
        "//prototype/lib:sample_repo_lib",
        "//:paths_lib",
        "//py:wikidata_lib",
    ],
    default_python_version = "PY3",
    srcs_version = "PY3",
)

py_binary(
    name = "train",
    srcs = [
        "train.py",
    ],
    deps = [
        "//prototype/lib:sample_repo_lib",
    ],
    default_python_version = "PY3",
    srcs_version = "PY3",
)

py_binary(
    name = "train_sk",
    srcs = [
        "train_sk.py",
    ],
    deps = [
        "//prototype/lib:sample_repo_lib",
        "//:paths_lib",
        "//py:file_util_lib",
    ],
    default_python_version = "PY3",
    srcs_version = "PY3",
)

py_binary(
    name = "apply_classifiers",
    srcs = [
        "apply_classifiers.py",
    ],
    deps = [
        "//prototype/lib:sample_repo_lib",
        "//prototype/lib:feature_extraction_lib",
        "//prototype/lib:sample_generation_lib",
        "//prototype/lib:wikidata_lib",
        "//:paths_lib",
        "//py:file_util_lib",
    ],
    default_python_version = "PY3",
    srcs_version = "PY3",
)
