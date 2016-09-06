package(default_visibility = ["//visibility:public"])

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

py_library(
    name = "article_repo_lib",
    srcs = [
        "article_repo.py",
    ],
    deps = [
        "//py:file_util_lib",
    ],
)
