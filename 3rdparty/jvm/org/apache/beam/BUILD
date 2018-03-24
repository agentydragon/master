java_library(
    name = "beam_runners_google_cloud_dataflow_java",
    exports = [
        "//3rdparty/jvm/com/fasterxml/jackson/core:jackson_annotations",
        "//3rdparty/jvm/com/fasterxml/jackson/core:jackson_core",
        "//3rdparty/jvm/com/fasterxml/jackson/core:jackson_databind",
        "//3rdparty/jvm/com/google/api_client:google_api_client",
        "//3rdparty/jvm/com/google/apis:google_api_services_clouddebugger",
        "//3rdparty/jvm/com/google/apis:google_api_services_dataflow",
        "//3rdparty/jvm/com/google/apis:google_api_services_storage",
        "//3rdparty/jvm/com/google/auth:google_auth_library_credentials",
        "//3rdparty/jvm/com/google/auth:google_auth_library_oauth2_http",
        "//3rdparty/jvm/com/google/cloud/bigdataoss:util",
        "//3rdparty/jvm/com/google/code/findbugs:jsr305",
        "//3rdparty/jvm/com/google/http_client:google_http_client",
        "//3rdparty/jvm/com/google/http_client:google_http_client_jackson2",
        "//3rdparty/jvm/joda_time:joda_time",
        "//3rdparty/jvm/org/apache/avro:avro",
        "//3rdparty/jvm/org/slf4j:slf4j_api",
        "//external:jar/org/apache/beam/beam_runners_google_cloud_dataflow_java",
        ":beam_sdks_common_runner_api",
        ":beam_sdks_java_core",
        ":beam_sdks_java_extensions_google_cloud_platform_core",
        ":beam_sdks_java_io_google_cloud_platform"
    ],
    visibility = [
        "//visibility:public"
    ]
)



java_library(
    name = "beam_sdks_common_runner_api",
    exports = [
        "//3rdparty/jvm/com/google/protobuf:protobuf_java",
        "//external:jar/org/apache/beam/beam_sdks_common_runner_api"
    ],
    visibility = [
        "//visibility:public"
    ]
)



java_library(
    name = "beam_sdks_java_core",
    exports = [
        "//3rdparty/jvm/com/fasterxml/jackson/core:jackson_annotations",
        "//3rdparty/jvm/com/fasterxml/jackson/core:jackson_core",
        "//3rdparty/jvm/com/fasterxml/jackson/core:jackson_databind",
        "//3rdparty/jvm/com/google/code/findbugs:jsr305",
        "//3rdparty/jvm/joda_time:joda_time",
        "//3rdparty/jvm/org/apache/avro:avro",
        "//3rdparty/jvm/org/slf4j:slf4j_api",
        "//3rdparty/jvm/org/xerial/snappy:snappy_java",
        "//external:jar/org/apache/beam/beam_sdks_java_core"
    ],
    visibility = [
        "//visibility:public"
    ]
)



java_library(
    name = "beam_sdks_java_extensions_google_cloud_platform_core",
    exports = [
        "//3rdparty/jvm/com/google/apis:google_api_services_cloudresourcemanager",
        "//3rdparty/jvm/com/google/cloud/bigdataoss:gcsio",
        "//external:jar/org/apache/beam/beam_sdks_java_extensions_google_cloud_platform_core"
    ],
    visibility = [
        "//visibility:public"
    ]
)



java_library(
    name = "beam_sdks_java_extensions_protobuf",
    exports = [
        "//external:jar/org/apache/beam/beam_sdks_java_extensions_protobuf"
    ],
    visibility = [
        "//visibility:public"
    ]
)



java_library(
    name = "beam_sdks_java_io_google_cloud_platform",
    exports = [
        "//3rdparty/jvm/com/google/api/grpc:grpc_google_pubsub_v1",
        "//3rdparty/jvm/com/google/api/grpc:proto_google_cloud_spanner_admin_database_v1",
        "//3rdparty/jvm/com/google/api/grpc:proto_google_common_protos",
        "//3rdparty/jvm/com/google/api:gax_grpc",
        "//3rdparty/jvm/com/google/apis:google_api_services_bigquery",
        "//3rdparty/jvm/com/google/apis:google_api_services_pubsub",
        "//3rdparty/jvm/com/google/cloud/bigtable:bigtable_client_core",
        "//3rdparty/jvm/com/google/cloud/bigtable:bigtable_protos",
        "//3rdparty/jvm/com/google/cloud/datastore:datastore_v1_proto_client",
        "//3rdparty/jvm/com/google/cloud/datastore:datastore_v1_protos",
        "//3rdparty/jvm/com/google/cloud:google_cloud_core",
        "//3rdparty/jvm/com/google/cloud:google_cloud_core_grpc",
        "//3rdparty/jvm/com/google/cloud:google_cloud_spanner",
        "//3rdparty/jvm/com/google/guava:guava",
        "//3rdparty/jvm/io/grpc:grpc_all",
        "//3rdparty/jvm/io/grpc:grpc_auth",
        "//3rdparty/jvm/io/grpc:grpc_core",
        "//3rdparty/jvm/io/grpc:grpc_netty",
        "//3rdparty/jvm/io/grpc:grpc_stub",
        "//3rdparty/jvm/io/netty:netty_handler",
        "//3rdparty/jvm/io/netty:netty_tcnative_boringssl_static",
        "//external:jar/org/apache/beam/beam_sdks_java_io_google_cloud_platform",
        ":beam_sdks_java_extensions_protobuf"
    ],
    visibility = [
        "//visibility:public"
    ]
)



java_library(
    name = "beam_sdks_java_io_hadoop_common",
    exports = [
        "//external:jar/org/apache/beam/beam_sdks_java_io_hadoop_common"
    ],
    visibility = [
        "//visibility:public"
    ]
)



java_library(
    name = "beam_sdks_java_io_hbase",
    exports = [
        "//3rdparty/jvm/org/apache/hbase:hbase_shaded_client",
        "//external:jar/org/apache/beam/beam_sdks_java_io_hbase",
        ":beam_sdks_java_io_hadoop_common"
    ],
    visibility = [
        "//visibility:public"
    ]
)


