py_library(
    name = "model_lib",
    srcs = [
        "model.py",
    ],
    deps = [
	":feature_extraction_lib",
        "//:paths_lib",
    ],
    visibility = ["//visibility:public"],
)

py_library(
    name = "feature_extraction_lib",
    srcs = [
        "feature_extraction.py",
    ],
    deps = [
        "//prototype/lib:file_util_lib",
        "//prototype/lib:article_set_lib",
        "//:paths_lib",
    ],
    visibility = ["//visibility:public"],
)

py_binary(
    name = "apply_classifiers",
    srcs = [
        "apply_classifiers.py",
    ],
    deps = [
        "//:paths_lib",
        ":feature_extraction_lib",
        "//prototype/lib:file_util_lib",
        "//prototype/lib:flags_lib",
        "//prototype/lib:relations_lib",
        "//prototype/lib:sample_generation_lib",
        "//prototype/lib:sample_repo_lib",
        "//prototype/lib:wikidata_lib",
    ],
    default_python_version = "PY3",
    srcs_version = "PY3",
)
