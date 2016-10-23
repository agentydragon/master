py_binary(
    name = "make_training_samples",
    srcs = [
        "make_training_samples.py",
    ],
    deps = [
        "//src/prototype/lib:article_repo_lib",
        "//src/prototype/lib:sample_repo_lib",
        "//src/prototype/lib:wikidata_lib",
        "//src/prototype/lib:sample_generation_lib",
        "//src/prototype/lib:zk_lib",
        "//src:paths_lib",
    ],
    visibility = ["//visibility:public"]
)

py_binary(
    name = "launch",
    srcs = [
        "launch.py",
    ],
    deps = [
        "//src:paths_lib",
        "//src/prototype/lib:file_util_lib",
        "//src/prototype/lib:mapper_lib",
        "//src/prototype/lib:article_set_lib",
        "//src/prototype/lib:zk_lib",
    ],
    data = [
        ":make_training_samples",
    ],
    default_python_version = "PY3",
    srcs_version = "PY3",
)

java_binary(
    name = "MakeTrainingSamples",
    srcs = [
        "MakeTrainingSamples.java",
        "MakeTrainingSamplesMapper.java",
    ],
    main_class = "MakeTrainingSamples",
    deps = [
        "//src/prototype/lib:JSONUtils",
        "//src/prototype/lib:SampleGeneration",
        "//src/prototype/lib:TrainingSample",
        "//src/prototype/lib:SavedDocument",
        "//src/prototype/lib:ArticlesTable",
        "//src/prototype/lib:WikidataClient",
        "//:org_apache_hadoop_hadoop_common",
        "//:org_apache_hadoop_hadoop_mapreduce_client_core",
        "//:org_apache_hbase_hbase_common",
        "//:org_apache_hbase_hbase_client",
        "//:org_apache_hbase_hbase_server",
        "//:org_json_json",
    ],
)

sh_binary(
    name = "run_on_hadoop",
    srcs = [
        "run_on_hadoop.sh",
    ],
    data = [
        ":MakeTrainingSamples_deploy.jar",
        ":MakeTrainingSamples.jar",
    ],
)

py_binary(
    name = "to_json",
    srcs = [
        "to_json.py",
    ],
    deps = [
        "//src/prototype/lib:sample_repo_lib",
        "//src/prototype/lib:training_sample_lib",
    ],
)
