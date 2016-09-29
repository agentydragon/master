py_library(
    name = "fuser_lib",
    srcs = [
	"fuser.py",
    ],
    deps = [
        "//prototype/lib:file_util_lib",
	"//:paths_lib",
    ],
)

py_binary(
    name = "make_fuser_data",
    srcs = [
        "make_fuser_data.py",
    ],
    deps = [
	":fuser_lib",
        "//prototype/extraction:model_lib",
        "//prototype/lib:file_util_lib",
        "//prototype/lib:article_set_lib",
        "//prototype/lib:flags_lib",
        "//prototype/lib:relations_lib",
        "//prototype/lib:sample_generation_lib",
        "//prototype/lib:sample_repo_lib",
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
        "//:paths_lib",
        "//prototype/lib:article_set_lib",
        "//prototype/lib:flags_lib",
        "//prototype/lib:relations_lib",
        "//prototype/lib:sample_generation_lib",
        "//prototype/lib:sample_repo_lib",
        "//prototype/lib:wikidata_lib",
        "//prototype/lib:plot_lib",
    ],
    default_python_version = "PY3",
    srcs_version = "PY3",
)
