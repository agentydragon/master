java_library(
    name = "api_common",
    exports = [
        "//external:jar/com/google/api/api_common"
    ],
    visibility = [
        "//visibility:public"
    ]
)



java_library(
    name = "gax",
    exports = [
        "//3rdparty/jvm/com/google/auto/value:auto_value",
        "//3rdparty/jvm/org/threeten:threetenbp",
        "//external:jar/com/google/api/gax"
    ],
    visibility = [
        "//visibility:public"
    ]
)



java_library(
    name = "gax_grpc",
    exports = [
        "//3rdparty/jvm/com/google/auto/value:auto_value",
        "//3rdparty/jvm/io/grpc:grpc_protobuf",
        "//3rdparty/jvm/org/threeten:threetenbp",
        "//external:jar/com/google/api/gax_grpc",
        ":api_common",
        ":gax"
    ],
    visibility = [
        "//visibility:public"
    ]
)


