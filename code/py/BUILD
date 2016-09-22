package(default_visibility = ["//visibility:public"])

py_library(
    name = "file_util_lib",
    srcs = [
        "file_util.py",
    ],
)

# TODO: I can make my own wiki2text! With blackjack and hookers!
# genrule(
#     name = "wiki2text",
#     srcs = [
#         "@wiki2text//:wiki2text.nim",
#     ],
#     outs = [
#         "wiki2text",
#     ],
#     cmd = "nim c -d:release --app:console $(location @wiki2text//:wiki2text.nim) && mv wiki2text $(GENDIR)"
# )

py_library(
    name = "pbs_util_lib",
    #srcs_version = "PY3",
    srcs = [
        "pbs_util.py",
    ],
)
