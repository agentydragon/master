py_binary(
    name = "run_fuseki",
    srcs = [
        "run_fuseki.py",
    ],
    deps = [
        ":fuseki_lib",
        ":fuseki_config_lib",
        "//src:paths_lib",
        "//src/prototype/lib:zk_lib",
    ],
)

py_library(
    name = "fuseki_config_lib",
    srcs = [
        "fuseki_config.py",
    ],
    visibility = ["//visibility:public"],
)

py_library(
    name = "fuseki_lib",
    srcs = [
        "fuseki.py",
    ],
    data = [
        "@jena_fuseki//:everything",
    ],
    deps = [
        "//src/prototype/lib:pbs_util_lib",
    ],
)

py_library(
    name = "jena_lib",
    srcs = [
        "jena.py",
    ],
    data = [
        "@jena//:everything",
    ],
)

py_binary(
    name = "fill_fuseki_dataset",
    srcs = [
        "fill_fuseki_dataset.py",
    ],
    deps = [
        ":jena_lib",
        "//src/prototype/lib:file_util_lib",
        "//src:paths_lib",
    ],
)

py_binary(
    name = "launch_fill_fuseki_dataset",
    srcs = [
        "launch_fill_fuseki_dataset.py",
    ],
    deps = [
        "//src/prototype/lib:pbs_util_lib",
        "//src:paths_lib",
    ],
    data = [
        ":fill_fuseki_dataset",
    ],
)
