py_binary(
    name = "find_persons",
    srcs = [
        "find_persons.py",
    ],
    deps = [
        "//prototype/lib:wikidata_lib",
        "//prototype/lib:flags_lib",
    ],
    default_python_version = "PY3",
    srcs_version = "PY3",
)

py_library(
    name = "feature_extraction_lib",
    srcs = [
        "feature_extraction.py",
    ],
)

py_binary(
    name = "data_stats",
    srcs = [
        "data_stats.py",
    ],
    deps = [
        "//prototype/lib:article_repo_lib",
        "//prototype/lib:article_set_lib",
        "//prototype/lib:flags_lib",
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
        "//prototype/lib:wikidata_lib",
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
        "//prototype:feature_extraction_lib",
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
        "//prototype/lib:file_util_lib",
        "//prototype:feature_extraction_lib",
        "//prototype/lib:sample_repo_lib",
        "//prototype/lib:wikidata_lib",
        "//prototype/lib:sample_generation_lib",
        "//prototype/lib:zk_lib",
        "//prototype/lib:article_set_lib",
        "//:paths_lib",
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
        "//:paths_lib",
        "//prototype:feature_extraction_lib",
        "//prototype/lib:file_util_lib",
        "//prototype/lib:relations_lib",
        "//prototype/lib:sample_generation_lib",
        "//prototype/lib:sample_repo_lib",
        "//prototype/lib:wikidata_lib",
    ],
    default_python_version = "PY3",
    srcs_version = "PY3",
)
