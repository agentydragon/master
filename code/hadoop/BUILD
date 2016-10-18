package(default_visibility = ["//visibility:public"])

java_binary(
    name = "GetKeys",
    srcs = [
        "GetKeys.java",
    ],
    main_class = "GetKeys",
    deps = [
        "//:org_apache_hadoop_hadoop_common",
        "//:org_apache_hbase_hbase_common",
        "//:org_apache_hbase_hbase_client",
        "//:org_apache_hbase_hbase_server",
    ],
)

java_library(
    name = "RandomSelectorMapper",
    srcs = [
        "RandomSelectorMapper.java",
    ],
    deps = [
        "//:org_apache_hadoop_hadoop_common",
        "//:org_apache_hadoop_hadoop_mapreduce_client_core",
    ],
)

java_binary(
    name = "RandomSelector",
    srcs = [
        "RandomSelector.java",
    ],
    main_class = "RandomSelector",
    deps = [
        ":RandomSelectorMapper",
        "//:org_apache_hadoop_hadoop_common",
        "//:org_apache_hadoop_hadoop_mapreduce_client_core",
    ],
)
