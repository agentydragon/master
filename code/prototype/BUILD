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
    name = "visualize_article",
    srcs = [
        "visualize_article.py",
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
