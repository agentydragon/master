java_binary(
    name = "add_parses",
    srcs = [
        "AddParses.java",
    ],
    main_class = "AddParses",
    deps = [
        "//hadoop:CoreNLPInterface",
        "//:commons_io_commons_io",
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
