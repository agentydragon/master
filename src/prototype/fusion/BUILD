py_library(
    name = "fuser_lib",
    srcs = [
        "fuser.py",
    ],
    deps = [
        "//src/prototype/lib:file_util_lib",
        "//src:paths_lib",
    ],
    visibility = ["//visibility:public"],
)

py_binary(
    name = "make_fuser_data",
    srcs = [
        "make_fuser_data.py",
    ],
    deps = [
	":fuser_lib",
        "//src/prototype/extraction:model_lib",
        "//src/prototype/lib:file_util_lib",
        "//src/prototype/lib:article_set_lib",
        "//src/prototype/lib:flags_lib",
        "//src/prototype/lib:relations_lib",
        "//src/prototype/lib:sample_generation_lib",
        "//src/prototype/lib:sample_repo_lib",
    ],
    default_python_version = "PY3",
    srcs_version = "PY3",
)

py_binary(
    name = "fuser_train",
    srcs = [
        "fuser_train.py",
    ],
    deps = [
        ":fuser_lib",
        "//src:paths_lib",
        "//src/prototype/lib:article_set_lib",
        "//src/prototype/lib:flags_lib",
        "//src/prototype/lib:relations_lib",
        "//src/prototype/lib:file_util_lib",
        "//src/prototype/lib:sample_generation_lib",
        "//src/prototype/lib:sample_repo_lib",
        "//src/prototype/lib:wikidata_lib",
        "//src/prototype/lib:plot_lib",
    ],
    default_python_version = "PY3",
    srcs_version = "PY3",
)
