load("@io_bazel_rules_docker//java:image.bzl", "java_image")
load("@io_bazel_rules_docker//container:push.bzl", "container_push")

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

java_image(
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

container_push(
    name = "push_split_to_articles",
    image = ":split_to_articles",
    format = "Docker",
    registry = "gcr.io",
    repository = "extended-atrium-198523/split_to_articles",
)
