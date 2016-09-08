py_binary(
    name = "find_persons",
    srcs = [
        "find_persons.py",
    ],
    deps = [
        "//py:wikidata_lib",
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
        "//py:paths_lib",
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
    ],
    default_python_version = "PY2",
    srcs_version = "PY2ONLY",
)
