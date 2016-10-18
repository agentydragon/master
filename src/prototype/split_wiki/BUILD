py_library(
    name = "split_wiki_lib",
    srcs = [
        "split_wiki.py",
    ],
    deps = [
        "//src/prototype/lib:article_repo_lib",
        "//src/prototype/lib:sentence_lib",
    ],
)

py_binary(
    name = "split_wiki_main",
    srcs = [
        "split_wiki_main.py",
    ],
    deps = [
        ":split_wiki_lib",
        "//src/prototype/lib:article_repo_lib",
    ],
)

py_binary(
    name = "launch",
    srcs = [
        "launch.py",
    ],
    deps = [
        "//src:paths_lib",
        "//src/prototype/lib:pbs_util_lib",
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
        "//src/prototype/lib:ArticlesTable",
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
        ":WikiSplit_deploy.jar",
        ":WikiSplit.jar",
    ],
)
