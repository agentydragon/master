load("@io_bazel_rules_docker//python:image.bzl", "py_image")
load("@io_bazel_rules_docker//docker:docker.bzl", "docker_build")
load(
  "@io_bazel_rules_python//python:python.bzl",
  "py_binary", "py_library", "py_test",
)
load("@io_bazel_rules_docker//container:push.bzl", "container_push")

load("@my_deps//:requirements.bzl", "requirement")

py_image(
    name = "upload_to_storage_py",
    srcs = ["upload_to_storage.py"],
    # base = "//python2.7:python27",
    main = "upload_to_storage.py",
    deps = [
        requirement("google-cloud-storage"),
        requirement("google-cloud-logging"),
        requirement("google-cloud-error_reporting"),
        requirement("oauth2client"),
        requirement("six"),
    ],
)

docker_build(
    name = "upload_to_storage",
    base = ":upload_to_storage_py",
)

container_push(
    name = "push_upload_to_storage",
    image = ":upload_to_storage",
    format = "Docker",
    registry = "gcr.io",
    repository = "extended-atrium-198523/upload_to_storage",
)

py_image(
    name = "create_single_file_py",
    srcs = ["create_single_file.py"],
    main = "create_single_file.py",
    deps = [
        requirement("google-cloud-storage"),
        requirement("google-cloud-logging"),
        requirement("google-cloud-error_reporting"),
        requirement("oauth2client"),
        requirement("six"),
    ],
)

docker_build(
    name = "create_single_file",
    base = ":create_single_file_py",
)

container_push(
    name = "push_create_single_file",
    image = ":create_single_file",
    format = "Docker",
    registry = "gcr.io",
    repository = "extended-atrium-198523/create_single_file",
)
