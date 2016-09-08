package(default_visibility = ["//visibility:public"])

py_binary(
    name = "find_persons",
    srcs = [
        "find_persons.py",
    ],
    deps = [
        "//py:wikidata_lib",
    ],
    default_python_version = "PY3",
    srcs_version = "PY3",
)

py_library(
    name = "article_repo_lib",
    srcs = [
        "article_repo.py",
    ],
    deps = [
        "//py:file_util_lib",
    ],
)

java_library(
    name = "ArticleRepository",
    srcs = [
        "ArticleRepository.java",
    ],
    deps = [
        "//:commons_io_commons_io",
        "//:org_json_json",
    ],
)

java_library(
    name = "SampleRepository",
    srcs = [
        "SampleRepository.java",
        "//:TrainingSamples.java",
    ],
    deps = [
        "//:commons_io_commons_io",
        "//:org_json_json",
        "//:com_google_protobuf_protobuf_java",
    ],
)

py_binary(
    name = "data_stats",
    srcs = [
        "data_stats.py",
    ],
    deps = [
        ":article_repo_lib",
        "//py:paths_lib",
    ],
)
