sh_binary(
    name = "prepare",
    srcs = [
        "prepare.sh",
    ],
    deps = [
        "//:paths_sh_lib",
    ],
    data = [
        "//thirdparty:wiki2text",
    ],
)

py_binary(
    name = "fill_fuseki_dataset",
    srcs = [
        "fill_fuseki_dataset.py",
    ],
    deps = [
        "//thirdparty/jena:jena_lib",
        "//prototype/lib:file_util_lib",
        "//:paths_lib",
    ],
)

py_binary(
    name = "launch_fill_fuseki_dataset",
    srcs = [
        "launch_fill_fuseki_dataset.py",
    ],
    deps = [
        "//prototype/lib:pbs_util_lib",
        "//:paths_lib",
    ],
    data = [
        ":fill_fuseki_dataset",
    ],
)
