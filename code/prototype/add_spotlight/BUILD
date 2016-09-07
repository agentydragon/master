py_binary(
    name = "add_spotlight",
    srcs = [
        "add_spotlight.py",
    ],
    deps = [
        "//py:paths_lib",
        "//py:spotlight_lib",
        "//prototype:article_repo_lib",
    ],
)

py_binary(
    name = "launch",
    srcs = [
        "launch.py",
    ],
    data = [
        ":add_spotlight",
        "//py:pbs_util_lib",
    ],
)
