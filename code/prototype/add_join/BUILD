py_binary(
    name = "add_join",
    srcs = [
        "add_join.py",
    ],
    deps = [
        "//:paths_lib",
        "//prototype/lib:article_repo_lib",
        "//prototype/lib:dbpedia_lib",
    ],
)

py_binary(
    name = "launch",
    srcs = [
        "launch.py",
    ],
    data = [
        ":add_join",
        "//prototype/lib:mapper_lib",
        "//prototype/lib:article_set_lib",
        "//prototype/lib:dbpedia_lib",
    ],
)

java_binary(
    name = "AddJoin",
    srcs = [
        "AddJoin.java",
        "AddJoinMapper.java",
    ],
    main_class = "AddJoin",
    deps = [
        "//prototype/lib:ArticlesTable",
        "//prototype/lib:SavedDocument",
        "//prototype/lib:DBpediaClient",
        "//:org_apache_hadoop_hadoop_common",
        "//:org_apache_hadoop_hadoop_mapreduce_client_core",
        "//:org_apache_hbase_hbase_common",
        "//:org_apache_hbase_hbase_client",
        "//:org_apache_hbase_hbase_server",
    ],
)
