load("@io_bazel_rules_docker//container:layer.bzl", "container_layer")
load("@io_bazel_rules_docker//container:push.bzl", "container_push")
load("@io_bazel_rules_docker//java:image.bzl", "java_image")

java_import(
    name = "stanford_corenlp_full_jars",
    jars = [
        "@stanford_corenlp_full//:ejml-0.23.jar",
        "@stanford_corenlp_full//:javax.json.jar",
        "@stanford_corenlp_full//:joda-time.jar",
        "@stanford_corenlp_full//:jollyday.jar",
        "@stanford_corenlp_full//:protobuf.jar",
        "@stanford_corenlp_full//:slf4j-api.jar",
        "@stanford_corenlp_full//:slf4j-simple.jar",
        "@stanford_corenlp_full//:stanford-corenlp-3.9.1.jar",
        "@stanford_corenlp_full//:stanford-corenlp-3.9.1-models.jar",
        "@stanford_corenlp_full//:xom.jar",
    ],
    visibility = ["//visibility:public"],
)

container_layer(
    name = "corenlp_layer",
    files = [
        "@stanford_corenlp_full//:everything",
    ],
)

# TODO: For making srparser work.
# container_layer(
#     name = "corenlp_srparser_model_layer",
#     files = [
#         "@stanford_corenlp_srparser_model//:file",
#     ],
# )

java_image(
    name = "corenlp_image",
    main_class = "edu.stanford.nlp.pipeline.StanfordCoreNLPServer",
    runtime_deps = [
        ":stanford_corenlp_full_jars",
    ],
)

container_push(
    name = "push_corenlp_image",
    format = "Docker",
    image = ":corenlp_image",
    registry = "gcr.io",
    repository = "extended-atrium-198523/corenlp",
)

# Kept for posterity:
#load("@io_bazel_rules_docker//container:image.bzl", "container_image")
#java_image(
#    name = "corenlp",
#args = [
#    "\"*\"",
#    "--port",
#    "9000",
#    "--timeout",
#    "10000",
#],
#srcs = [
#    "@stanford_corenlp_full//:stanford_corenlp_full_jars",
#],
#srcs = [
#    ":stanford_corenlp_full_jars",
#],
#args = [
#    "--port",
#    "9000",
#    "--timeout",
#    "10000",
#],
#layers = [":stanford_corenlp_full_jars"],
#main_class = "edu.stanford.nlp.pipeline.StanfordCoreNLPServer",
#ports = ["9000"],
#container_image(
#    name = "corenlp_image",
#    base = "@java_base//image",
#    entrypoint = [
#        "java",
#        "-mx5g",
#        "-cp",
#        "\"*\"",
#        "edu.stanford.nlp.pipeline.StanfordCoreNLPServer",
#        "--port",
#        "9000",
#        "--timeout",
#        "10000",
#    ],
#    layers = [":corenlp_layer"],
#)
#
#py_binary(
#    name = "corenlp_image_test",
#    srcs = ["corenlp_image_test.py"],
#    deps = [":corenlp_image"],
#)
