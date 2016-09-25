py_binary(
    name = "add_spotlight",
    srcs = [
        "add_spotlight.py",
    ],
    deps = [
        "//:paths_lib",
        "//prototype/lib:spotlight_lib",
        "//prototype/lib:article_repo_lib",
    ],
)

py_binary(
    name = "launch",
    srcs = [
        "launch.py",
    ],
    data = [
        ":add_spotlight",
        "//prototype/lib:mapper_lib",
        "//prototype/lib:article_set_lib",
        "//prototype/lib:flags_lib",
    ],
)
