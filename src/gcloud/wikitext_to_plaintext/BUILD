java_binary(
    name = "wikitext_to_plaintext",
    srcs = [
        "WikitextToPlaintext.java",
    ],
    main_class = "WikitextToPlaintext",
    deps = [
        # "//3rdparty/jvm/com/google/cloud/bigtable:bigtable_hbase_2_x",
        "//3rdparty/jvm/info/bliki/wiki:bliki_core",
        "//3rdparty/jvm/org/apache/beam:beam_runners_google_cloud_dataflow_java",
        "//3rdparty/jvm/org/apache/hbase:hbase_client",
        "//3rdparty/jvm/com/google/cloud/bigtable:bigtable_hbase_beam",
        # TODO: Add the Cloud Bigtable connector.
    ],
)
