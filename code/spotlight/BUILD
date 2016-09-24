py_binary(
    name = "launch_spotlight_servers",
    default_python_version = "PY3",
    srcs_version = "PY3",
    srcs = [
        "launch_spotlight_servers.py",
    ],
    deps = [
        "//prototype/lib:spotlight_lib",
        "//prototype/lib:pbs_util_lib",
        "//:paths_lib",
    ],
    data = [
        "//thirdparty/spotlight",
    ]
)
