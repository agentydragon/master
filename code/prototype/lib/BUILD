package(default_visibility = ["//visibility:public"])

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

py_library(
    name = "parse_xmls_to_protos_lib",
    srcs = [
        "parse_xmls_to_protos.py",
        "//:sentence_pb2.py",
        "//py:dbpedia_lib",
    ],
)

py_test(
    name = "parse_xmls_to_protos_test",
    srcs = [
        "parse_xmls_to_protos_test.py",
    ],
    deps = [
        ":parse_xmls_to_protos_lib",
    ],
    data = [
        "//testdata:Obama.txt",
        "//testdata:Obama.txt.out",
        "//testdata:Obama.spotlight.json",
    ],
    srcs_version = "PY3",
    default_python_version = "PY3",
)
