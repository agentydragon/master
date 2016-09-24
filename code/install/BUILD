sh_binary(
    name = "prepare",
    srcs = [
        "prepare.sh",
    ],
    deps = [
        "//:paths_sh_lib",
    ],
    data = [
        "//:wiki2text",
    ],
)

py_binary(
    name = "fill_dbpedia",
    srcs = [
        "fill_dbpedia.py",
    ],
    deps = [
        "//thirdparty/jena:jena_lib",
        "//prototype/lib:file_util_lib",
        "//:paths_lib",
    ],
)
