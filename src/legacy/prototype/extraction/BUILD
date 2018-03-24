py_library(
    name = "model_lib",
    srcs = [
        "model.py",
    ],
    deps = [
	":feature_extraction_lib",
        "//src:paths_lib",
    ],
    visibility = ["//visibility:public"],
)

py_library(
    name = "feature_extraction_lib",
    srcs = [
        "feature_extraction.py",
    ],
    deps = [
        "//src/prototype/lib:file_util_lib",
        "//src/prototype/lib:article_set_lib",
        "//src/prototype/lib:training_sample_lib",
        "//src:paths_lib",
    ],
    visibility = ["//visibility:public"],
)
