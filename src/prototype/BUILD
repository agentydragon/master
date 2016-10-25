py_binary(
    name = "find_persons",
    srcs = [
        "find_persons.py",
    ],
    deps = [
        "//src/prototype/lib:wikidata_lib",
        "//src/prototype/lib:flags_lib",
        "//src:paths_lib",
    ],
    default_python_version = "PY3",
    srcs_version = "PY3",
)


py_binary(
    name = "data_stats",
    srcs = [
        "data_stats.py",
    ],
    deps = [
        "//src/prototype/lib:article_repo_lib",
        "//src/prototype/lib:article_set_lib",
        "//src/prototype/lib:flags_lib",
        "//src:paths_lib",
    ],
)

py_binary(
    name = "visualize_article",
    srcs = [
        "visualize_article.py",
    ],
    deps = [
        "//src/prototype/lib:article_repo_lib",
        "//src:paths_lib",
    ],
    default_python_version = "PY3",
    srcs_version = "PY3",
)

py_binary(
    name = "visualize_relation",
    srcs = [
        "visualize_relation.py",
    ],
    deps = [
        "//src/prototype/lib:sample_repo_lib",
        "//src:paths_lib",
        "//src/prototype/lib:wikidata_lib",
    ],
    default_python_version = "PY3",
    srcs_version = "PY3",
)

sh_binary(
    name = "run_on_hadoop",
    srcs = [
        "run_on_hadoop.sh",
    ],
    data = [
        ":HBaseToJSON_deploy.jar",
        ":HBaseToJSON.jar",
    ],
)

java_binary(
    name = "HBaseToJSON",
    srcs = [
        "HBaseToJSON.java",
    ],
    main_class = "HBaseToJSON",
    deps = [
        "//src/prototype/lib:ArticleRepository",
        "//src/prototype/lib:ArticlesTable",
        "//src/prototype/lib:ArticleSet",
        "//src/prototype/lib:SavedDocument",
        "//:org_json_json",
        "//:org_apache_hadoop_hadoop_common",
        "//:org_apache_hbase_hbase_common",
        "//:org_apache_hbase_hbase_client",
        "//:org_apache_hbase_hbase_server",
    ],
)
