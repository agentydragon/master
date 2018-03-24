java_library(
    name = "google_cloud_core",
    exports = [
        "//3rdparty/jvm/com/google/api/grpc:proto_google_common_protos",
        "//3rdparty/jvm/com/google/api/grpc:proto_google_iam_v1",
        "//3rdparty/jvm/com/google/api:api_common",
        "//3rdparty/jvm/com/google/api:gax",
        "//3rdparty/jvm/com/google/code/findbugs:jsr305",
        "//3rdparty/jvm/com/google/guava:guava",
        "//3rdparty/jvm/com/google/http_client:google_http_client",
        "//3rdparty/jvm/com/google/protobuf:protobuf_java_util",
        "//3rdparty/jvm/joda_time:joda_time",
        "//3rdparty/jvm/org/json:json",
        "//external:jar/com/google/cloud/google_cloud_core"
    ],
    visibility = [
        "//visibility:public"
    ]
)



java_library(
    name = "google_cloud_core_http",
    exports = [
        "//3rdparty/jvm/com/google/api_client:google_api_client",
        "//3rdparty/jvm/com/google/auth:google_auth_library_credentials",
        "//3rdparty/jvm/com/google/auth:google_auth_library_oauth2_http",
        "//3rdparty/jvm/com/google/http_client:google_http_client_appengine",
        "//3rdparty/jvm/com/google/http_client:google_http_client_jackson",
        "//3rdparty/jvm/com/google/http_client:google_http_client_jackson2",
        "//3rdparty/jvm/com/google/oauth_client:google_oauth_client",
        "//external:jar/com/google/cloud/google_cloud_core_http"
    ],
    visibility = [
        "//visibility:public"
    ]
)



java_library(
    name = "google_cloud_storage",
    exports = [
        "//3rdparty/jvm/com/google/apis:google_api_services_storage",
        "//external:jar/com/google/cloud/google_cloud_storage",
        ":google_cloud_core",
        ":google_cloud_core_http"
    ],
    visibility = [
        "//visibility:public"
    ]
)


