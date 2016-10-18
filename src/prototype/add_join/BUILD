py_binary(
    name = "add_join",
    srcs = [
        "add_join.py",
    ],
    deps = [
        "//src:paths_lib",
        "//src/prototype/lib:article_repo_lib",
        "//src/prototype/lib:dbpedia_lib",
    ],
)

py_binary(
    name = "launch",
    srcs = [
        "launch.py",
    ],
    data = [
        ":add_join",
        "//src/prototype/lib:mapper_lib",
        "//src/prototype/lib:article_set_lib",
        "//src/prototype/lib:dbpedia_lib",
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
        "//src/prototype/lib:ArticlesTable",
        "//src/prototype/lib:SavedDocument",
        "//src/prototype/lib:DBpediaClient",
        "//:org_apache_hadoop_hadoop_common",
        "//:org_apache_hadoop_hadoop_mapreduce_client_core",
        "//:org_apache_hbase_hbase_common",
        "//:org_apache_hbase_hbase_client",
        "//:org_apache_hbase_hbase_server",
    ],
)

sh_binary(
    name = "run_on_hadoop",
    srcs = [
        "run_on_hadoop.sh",
    ],
    data = [
        ":AddJoin_deploy.jar",
        ":AddJoin.jar",
    ],
)
