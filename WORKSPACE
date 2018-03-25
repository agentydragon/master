# Load rules for building Python and Java Docker images.
# =============================================================================

git_repository(
    name = "io_bazel_rules_docker",
    remote = "https://github.com/bazelbuild/rules_docker.git",
    tag = "v0.4.0",
)

load(
    "@io_bazel_rules_docker//python:image.bzl",
    _py_image_repos = "repositories",
)

_py_image_repos()

load(
    "@io_bazel_rules_docker//java:image.bzl",
    _java_image_repos = "repositories",
)

_java_image_repos()

# Import pip dependencies.
# =============================================================================

git_repository(
    name = "io_bazel_rules_python",
    commit = "115e3a0dab4291184fdcb0d4e564a0328364571a",
    remote = "https://github.com/bazelbuild/rules_python.git",
)

load("@io_bazel_rules_python//python:pip.bzl", "pip_import")

pip_import(
    name = "pip_dependencies",
    requirements = "//src:requirements.txt",
)

load("@pip_dependencies//:requirements.bzl", "pip_install")

pip_install()

# Maven dependencies.
# =============================================================================
#
# 3rdparty/workspace.bzl generated using https://github.com/johnynek/bazel-deps:
# bazel run //:parse -- generate \
#     -r ~/repos/master -s 3rdparty/workspace.bzl -d dependencies.yaml
# TODO: bazelbuild/migration-tooling also has transitive_maven_jars rule which
# might alleviate the need for generating WORKSPACE.
load("//3rdparty:workspace.bzl", "maven_dependencies")

maven_dependencies()

# TODO: want commons_cli_commons_cli

# # Stanford CoreNLP
# http_jar(
#     name = "corenlp_models",
#     url = "http://nlp.stanford.edu/software/stanford-english-corenlp-2016-01-10-models.jar",
#     sha256 = "8ad16bb419044a8c3efc2d14b9072c56b300e6f462183c62ff1f6470c11389c0"
# )
#
# http_jar(
#     name = "corenlp_srparser_model",
#     url = "http://nlp.stanford.edu/software/stanford-srparser-2014-10-23-models.jar",
#     sha256 = "0335b1a443a41952d18a472ac65e49b4482424ffec12ddf41703c696e72c793d"
# )

# # DBpedia Spotlight
# http_jar(
#     name = "dbpedia_spotlight",
#     url = "http://spotlight.sztaki.hu/downloads/archive/version-0.1/dbpedia-spotlight.jar",
#     sha256 = "760ce9440be6858f956ad98bcbb4754636c31cdf77d23c6f98019cb02412d32b"
# )
#
# http_file(
#     name = "dbpedia_spotlight_model_en",
#     url = "http://spotlight.sztaki.hu/downloads/archive/version-0.1/en.tar.gz",
#     sha256 = "773beb985b3a28d8618e620ac7ac699a59228e81f0afa56618f13e3984a40e2f",
# )

# # Apache Jena Fuseki
# new_http_archive(
#     name = "jena",
#     url = "http://mirror.dkm.cz/apache/jena/binaries/apache-jena-3.1.0.tar.gz",
#     sha256 = "532ad87eab7792ff1ffae34375d4c27956aada7c659743c39027e8b48f29cbd9",
#     build_file_content = """
# filegroup(
#     name = "everything",
#     srcs = glob(
#         include = ["**/*"]
#     ),
#     visibility = ["//visibility:public"],
# )
# """,
# )
#
# new_http_archive(
#     name = "jena_fuseki",
#     url = "http://mirror.dkm.cz/apache/jena/binaries/apache-jena-fuseki-2.4.0.tar.gz",
#     sha256 = "8b4299c35374bba47c6f9644166c069c243b08eb600a71f66c3c9cc2ec7e594a",
#     build_file_content = """
# filegroup(
#     name = "everything",
#     srcs = glob(
#         include = ["**/*"]
#     ),
#     visibility = ["//visibility:public"],
# )
# """,
# )

# http_archive(
#     name = "migration_tooling",
#     url = "https://github.com/bazelbuild/migration-tooling/archive/master.zip",
#     type = "zip",
#     strip_prefix = "migration-tooling-master",
# )
#
# load("@migration_tooling//transitive_maven_jar:transitive_maven_jar.bzl", "transitive_maven_jar")
#
# transitive_maven_jar(
#   name = "dependencies",
#   artifacts = [
#     "org.apache.beam:beam-runners-google-cloud-dataflow-java:2.1.0",
#     "org.apache.hbase:hbase-client:1.4.2",
#     "com.google.cloud:google-cloud-storage:1.14.0",
#     # "com.google.api-client:google-api-client:1.22.0",
#     "com.google.cloud.bigtable:bigtable-hbase-2.x:1.3.0",
#     "com.google.cloud.bigtable:bigtable-hbase-beam:1.1.2",
#     "info.bliki.wiki:bliki-core:3.1.0",
#   ],
#   repositories = [
#     # "https://repo.maven.apache.org/maven2/"
#     #"https://repo1.maven.org/maven2/",
#     "http://uk.maven.org/maven2/",
#   ]
# )

# TODO: Leftover artifacts from earlier version:
#    --artifact=org.apache.hadoop:hadoop-common:2.6.0 \
#    --artifact=org.apache.hadoop:hadoop-mapreduce-client-core:2.6.0 \
#    --artifact=edu.stanford.nlp:stanford-corenlp:3.6.0 \
#    --artifact=org.json:json:20160810 \
#    --artifact=org.apache.jena:apache-jena-libs:3.1.0 \
#    --artifact=org.apache.httpcomponents:httpclient:4.2.6 \
#    --artifact=org.apache.httpcomponents:httpcore:4.2.5 \
#    --artifact=com.google.protobuf:protobuf-java:3.0.0 \
#    --artifact=org.apache.hbase:hbase-client:1.2.2 \
#    --artifact=org.apache.hbase:hbase-server:1.2.2
