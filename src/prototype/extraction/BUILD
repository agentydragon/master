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
        "//src:paths_lib",
    ],
    visibility = ["//visibility:public"],
)

py_binary(
    name = "apply_classifiers",
    srcs = [
        "apply_classifiers.py",
    ],
    deps = [
        "//src:paths_lib",
        ":feature_extraction_lib",
        "//src/prototype/lib:file_util_lib",
        "//src/prototype/lib:flags_lib",
        "//src/prototype/lib:relations_lib",
        "//src/prototype/lib:sample_generation_lib",
        "//src/prototype/lib:sample_repo_lib",
        "//src/prototype/lib:wikidata_lib",
    ],
    default_python_version = "PY3",
    srcs_version = "PY3",
)
