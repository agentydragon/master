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
        "@cpulimit//:cpulimit_bin",
        ":local_fuseki",
    ],
)

py_binary(
    name = "local_fuseki",
    srcs = [
        "local_fuseki.py",
    ],
    deps = [
        "//thirdparty/fuseki:fuseki_lib",
        "//:paths_lib",
        "//prototype/lib:flags_lib",
    ],
    data = [
        "//prototype/make_training_samples:make_training_samples",
    ],
)
