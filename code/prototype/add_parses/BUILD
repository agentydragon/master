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
    deps = [
        "//prototype/lib:mapper_lib",
        "//prototype/lib:flags_lib",
        "//prototype/lib:article_set_lib",
    ],
    data = [
        ":add_parses",
    ],
)
