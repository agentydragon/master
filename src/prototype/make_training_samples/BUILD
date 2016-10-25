java_binary(
    name = "MakeTrainingSamples",
    srcs = [
        "MakeTrainingSamples.java",
        "MakeTrainingSamplesMapper.java",
        "MakeTrainingSamplesReducer.java",
    ],
    main_class = "MakeTrainingSamples",
    deps = [
        "//src/prototype/lib:JSONUtils",
        "//src/prototype/lib:SampleGeneration",
        "//src/prototype/lib:TrainingSample",
        "//src/prototype/lib:SavedDocument",
        "//src/prototype/lib:ArticlesTable",
        "//src/prototype/lib:WikidataClient",
        "//src/prototype/lib:ArticleSet",
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
