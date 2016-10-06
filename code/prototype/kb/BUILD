py_binary(
    name = "run_fuseki",
    srcs = [
        "run_fuseki.py",
    ],
    deps = [
        ":fuseki_lib",
        ":fuseki_config_lib",
        "//:paths_lib",
        "//prototype/lib:zk_lib",
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
        "//prototype/lib:pbs_util_lib",
    ],
)

py_binary(
    name = "local_fuseki_launch",
    srcs = [
        "local_fuseki_launch.py",
    ],
    deps = [
        "//prototype/lib:pbs_util_lib",
        "//prototype/lib:mapper_lib",
        "//prototype/lib:article_set_lib",
        "//prototype/lib:flags_lib",
    ],
    data = [
        ":local_fuseki",
    ],
)

py_binary(
    name = "local_fuseki",
    srcs = [
        "local_fuseki.py",
    ],
    deps = [
        ":fuseki_lib",
        ":fuseki_config_lib",
        "//:paths_lib",
        "//prototype/lib:flags_lib",
    ],
    data = [
        "//prototype/make_training_samples:make_training_samples",
    ],
)
