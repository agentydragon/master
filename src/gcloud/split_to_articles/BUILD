java_binary(
    name = "demo",
    srcs = [
        "Demo.java",
    ],
    main_class = "Demo",
    deps = [
        "//3rdparty/jvm/com/google/cloud/bigtable:bigtable_hbase_2_x",
    ],
)

java_binary(
    name = "split_to_articles",
    srcs = [
        "SplitToArticles.java",
    ],
    main_class = "SplitToArticles",
    deps = [
        "//3rdparty/jvm/com/google/cloud/bigtable:bigtable_hbase_2_x",
	"//3rdparty/jvm/com/google/cloud:google_cloud_storage",
	"//3rdparty/jvm/info/bliki/wiki:bliki_core",
    ],
)
