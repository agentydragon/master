py_library(
    name = "split_wiki_lib",
    srcs = [
        "split_wiki.py",
    ],
    deps = [
        "//py:file_util_lib",
        "//prototype:article_repo_lib",
    ],
)

py_binary(
    name = "split_wiki_main",
    srcs = [
        "split_wiki_main.py",
    ],
    deps = [
        ":split_wiki_lib",
    ],
)

py_test(
    name = "split_wiki_test",
    srcs = [
        "split_wiki_test.py",
    ],
    deps = [
        ":split_wiki_lib",
    ],
)

py_binary(
    name = "launch",
    srcs = [
        "launch.py",
    ],
    deps = [
        "//prototype/lib:pbs_util_lib",
        "//:paths_lib",
    ],
    data = [
        ":split_wiki_main",
    ],
    default_python_version = "PY3",
    srcs_version = "PY3",
)
