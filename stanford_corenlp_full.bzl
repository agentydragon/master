package(default_visibility = ["//visibility:public"])

exports_files(glob(include = ["**/*"]))

filegroup(
    name = "everything",
    srcs = glob(include = ["**/*"]),
)

filegroup(
    name = "jars",
    srcs = glob(include = ["**/*.jar"]),
)
