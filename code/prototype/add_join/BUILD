py_binary(
    name = "add_join",
    srcs = [
        "add_join.py",
    ],
    deps = [
        "//:paths_lib",
        "//prototype/lib:parse_xmls_to_protos_lib",
        "//prototype/lib:article_repo_lib",
    ],
)

py_binary(
    name = "launch",
    srcs = [
        "launch.py",
    ],
    data = [
        ":add_join",
        "//prototype/lib:mapper_lib",
    ],
)
