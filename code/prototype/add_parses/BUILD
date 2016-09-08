java_binary(
    name = "add_parses",
    srcs = [
        "AddParses.java",
    ],
    main_class = "AddParses",
    deps = [
        "//prototype/lib:ArticleRepository",
        "//hadoop:CoreNLPInterface",
        "//:org_json_json",
    ],
)

py_binary(
    name = "launch",
    srcs = [
        "launch.py",
    ],
    data = [
        ":add_parses",
        "//py:pbs_util_lib",
    ],
)
