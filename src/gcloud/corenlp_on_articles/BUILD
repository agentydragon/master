load("@pip_dependencies//:requirements.bzl", "requirement")

py_binary(
    name = "corenlp_on_articles_bin",
    srcs = ["corenlp_on_articles.py"],
    main = "corenlp_on_articles.py",
    deps = [
        requirement("google-cloud-dataflow"),
        requirement("pycorenlp"),
    ],
)
