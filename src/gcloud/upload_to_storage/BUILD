load("@io_bazel_rules_docker//python:image.bzl", "py_image")
load("@io_bazel_rules_docker//docker:docker.bzl", "docker_build")
load("@io_bazel_rules_docker//container:push.bzl", "container_push")
load("@pip_dependencies//:requirements.bzl", "requirement")

py_image(
    name = "upload_to_storage_py",
    srcs = ["upload_to_storage.py"],
    main = "upload_to_storage.py",
    deps = [
        requirement("google-cloud-storage"),
    ],
)

docker_build(
    name = "upload_to_storage",
    base = ":upload_to_storage_py",
)

container_push(
    name = "push_upload_to_storage",
    format = "Docker",
    image = ":upload_to_storage",
    registry = "gcr.io",
    repository = "extended-atrium-198523/upload_to_storage",
)

py_binary(
    name = "create_single_file_bin",
    srcs = ["create_single_file.py"],
    main = "create_single_file.py",
    deps = [
        requirement("google-cloud-storage"),
    ],
    # TODO(#5): Adding legacy_create_init = False might allow us to get rid
    # of the sys.path hack in create_single_file.py.
    # legacy_create_init = False
)

py_image(
    name = "create_single_file_py",
    srcs = ["create_single_file.py"],
    main = "create_single_file.py",
    deps = [
        requirement("google-cloud-storage"),
    ],
)

docker_build(
    name = "create_single_file",
    base = ":create_single_file_py",
)

container_push(
    name = "push_create_single_file",
    format = "Docker",
    image = ":create_single_file",
    registry = "gcr.io",
    repository = "extended-atrium-198523/create_single_file",
)
