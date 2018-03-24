java_library(
    name = "bigtable_client_core",
    exports = [
        "//3rdparty/jvm/com/google/api/grpc:grpc_google_cloud_bigtable_admin_v2",
        "//3rdparty/jvm/com/google/api/grpc:grpc_google_cloud_bigtable_v2",
        "//3rdparty/jvm/com/google/api/grpc:grpc_google_common_protos",
        "//3rdparty/jvm/com/google/api/grpc:proto_google_cloud_bigtable_admin_v2",
        "//3rdparty/jvm/com/google/api/grpc:proto_google_cloud_bigtable_v2",
        "//3rdparty/jvm/com/google/api_client:google_api_client",
        "//3rdparty/jvm/com/google/auth:google_auth_library_appengine",
        "//3rdparty/jvm/com/google/auth:google_auth_library_credentials",
        "//3rdparty/jvm/com/google/auth:google_auth_library_oauth2_http",
        "//3rdparty/jvm/com/google/code/findbugs:jsr305",
        "//3rdparty/jvm/io/dropwizard/metrics:metrics_core",
        "//3rdparty/jvm/io/grpc:grpc_auth",
        "//3rdparty/jvm/io/grpc:grpc_netty",
        "//3rdparty/jvm/io/grpc:grpc_protobuf",
        "//3rdparty/jvm/io/grpc:grpc_stub",
        "//3rdparty/jvm/io/netty:netty_tcnative_boringssl_static",
        "//3rdparty/jvm/io/opencensus:opencensus_api",
        "//3rdparty/jvm/io/opencensus:opencensus_contrib_grpc_util",
        "//external:jar/com/google/cloud/bigtable/bigtable_client_core"
    ],
    visibility = [
        "//visibility:public"
    ]
)



java_library(
    name = "bigtable_hbase",
    exports = [
        "//3rdparty/jvm/com/google/guava:guava",
        "//3rdparty/jvm/com/google/http_client:google_http_client",
        "//3rdparty/jvm/com/google/protobuf:protobuf_java",
        "//3rdparty/jvm/io/grpc:grpc_core",
        "//external:jar/com/google/cloud/bigtable/bigtable_hbase",
        ":bigtable_client_core"
    ],
    visibility = [
        "//visibility:public"
    ]
)



java_library(
    name = "bigtable_hbase_1_x_shaded",
    exports = [
        "//3rdparty/jvm/commons_logging:commons_logging",
        "//3rdparty/jvm/io/dropwizard/metrics:metrics_core",
        "//external:jar/com/google/cloud/bigtable/bigtable_hbase_1_x_shaded"
    ],
    visibility = [
        "//visibility:public"
    ]
)



java_library(
    name = "bigtable_hbase_2_x",
    exports = [
        "//3rdparty/jvm/org/apache/hbase:hbase_shaded_client",
        "//external:jar/com/google/cloud/bigtable/bigtable_hbase_2_x",
        ":bigtable_hbase"
    ],
    visibility = [
        "//visibility:public"
    ]
)



java_library(
    name = "bigtable_hbase_beam",
    exports = [
        "//3rdparty/jvm/org/apache/beam:beam_sdks_java_core",
        "//3rdparty/jvm/org/apache/beam:beam_sdks_java_io_hbase",
        "//external:jar/com/google/cloud/bigtable/bigtable_hbase_beam",
        ":bigtable_hbase_1_x_shaded"
    ],
    visibility = [
        "//visibility:public"
    ]
)



java_library(
    name = "bigtable_protos",
    exports = [
        "//external:jar/com/google/cloud/bigtable/bigtable_protos"
    ],
    visibility = [
        "//visibility:public"
    ]
)


