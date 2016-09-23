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

sh_binary(
    name = "fill_dbpedia",
    srcs = [
        "fill_dbpedia.sh",
    ],
    deps = [
        "//:paths_sh_lib",
        "@jena//:everything",
    ],
)
