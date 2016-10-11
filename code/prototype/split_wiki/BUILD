py_library(
    name = "split_wiki_lib",
    srcs = [
        "split_wiki.py",
    ],
    deps = [
        "//prototype/lib:article_repo_lib",
        "//prototype/lib:sentence_lib",
    ],
)

py_binary(
    name = "split_wiki_main",
    srcs = [
        "split_wiki_main.py",
    ],
    deps = [
        ":split_wiki_lib",
        "//prototype/lib:article_repo_lib",
    ],
)

py_binary(
    name = "launch",
    srcs = [
        "launch.py",
    ],
    deps = [
        "//prototype/lib:pbs_util_lib",
        "//:paths_lib",
    ],
    data = [
        ":split_wiki_main",
    ],
    default_python_version = "PY3",
    srcs_version = "PY3",
)

java_binary(
    name = "WikiSplit",
    srcs = [
        "WikiSplit.java",
        "ArticleSplitterMapper.java",
    ],
    main_class = "WikiSplit",
    deps = [
        "//:org_apache_hadoop_hadoop_common",
        "//:org_apache_hadoop_hadoop_mapreduce_client_core",
        "//:org_apache_hbase_hbase_common",
        "//:org_apache_hbase_hbase_client",
        "//:org_apache_hbase_hbase_server",
    ],
)
