py_binary(
    name = "get_pra_data",
    srcs = [
        "get_pra_data.py",
    ],
    deps = [
        "//src:paths_lib",
        "//src/prototype/lib:wikidata_lib",
        "//src/prototype/lib:wikidata_util_lib",
        "//src/prototype/lib:flags_lib",
        "//src/prototype/lib:file_util_lib",
    ],
)

py_library(
    name = "paths_lib",
    #srcs_version = "PY3",
    srcs = [
        "paths.py",
    ],
    visibility = ["//visibility:public"],
)

java_library(
    name = "paths_java_lib",
    srcs = [
        "Paths.java",
    ],
    visibility = ["//visibility:public"],
)

sh_library(
    name = "paths_sh_lib",
    srcs = [
        "paths.sh",
    ],
    visibility = ["//visibility:public"],
)

genrule(
    name = "paths_genrule",
    srcs = [
        "paths_gen.py",
    ],
    outs = [
        "paths.py",
        "paths.sh",
        "Paths.java",
    ],
    cmd = "python3 ./paths_gen.py --python_out=$(GENDIR)/paths.py --sh_out $(GENDIR)/paths.sh --java_out $(GENDIR)/Paths.java",
)
