py_binary(
    name = "local_fuseki_launch",
    srcs = [
        "local_fuseki_launch.py",
    ],
    deps = [
        "//prototype/lib:pbs_util",
    ],
    data = [
        "@cpulimit//:cpulimit",
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
    ],
)
