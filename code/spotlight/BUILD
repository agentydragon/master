py_binary(
    name = "launch_servers",
    default_python_version = "PY3",
    srcs_version = "PY3",
    srcs = [
        "launch_servers.py",
    ],
    deps = [
        "//prototype/lib:spotlight_lib",
        "//prototype/lib:pbs_util_lib",
        "//prototype/lib:flags_lib",
        "//prototype/lib:zk_lib",
        "//:paths_lib",
    ],
    data = [
        "@cpulimit//:cpulimit_bin",
        "//thirdparty/spotlight",
    ]
)
