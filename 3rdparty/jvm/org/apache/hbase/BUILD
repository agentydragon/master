java_library(
    name = "hbase_annotations",
    exports = [
        "//3rdparty/jvm/junit:junit",
        "//3rdparty/jvm/log4j:log4j",
        "//external:jar/org/apache/hbase/hbase_annotations"
    ],
    visibility = [
        "//visibility:public"
    ]
)



java_library(
    name = "hbase_client",
    exports = [
        "//3rdparty/jvm/com/google/guava:guava",
        "//3rdparty/jvm/com/google/protobuf:protobuf_java",
        "//3rdparty/jvm/com/yammer/metrics:metrics_core",
        "//3rdparty/jvm/commons_codec:commons_codec",
        "//3rdparty/jvm/commons_io:commons_io",
        "//3rdparty/jvm/commons_lang:commons_lang",
        "//3rdparty/jvm/commons_logging:commons_logging",
        "//3rdparty/jvm/io/netty:netty_all",
        "//3rdparty/jvm/org/apache/hadoop:hadoop_auth",
        "//3rdparty/jvm/org/apache/hadoop:hadoop_common",
        "//3rdparty/jvm/org/apache/hadoop:hadoop_mapreduce_client_core",
        "//3rdparty/jvm/org/apache/htrace:htrace_core",
        "//3rdparty/jvm/org/apache/zookeeper:zookeeper",
        "//3rdparty/jvm/org/codehaus/jackson:jackson_mapper_asl",
        "//3rdparty/jvm/org/jruby/jcodings:jcodings",
        "//3rdparty/jvm/org/jruby/joni:joni",
        "//external:jar/org/apache/hbase/hbase_client",
        ":hbase_annotations",
        ":hbase_common",
        ":hbase_hadoop2_compat",
        ":hbase_hadoop_compat",
        ":hbase_protocol"
    ],
    visibility = [
        "//visibility:public"
    ]
)



java_library(
    name = "hbase_common",
    exports = [
        "//3rdparty/jvm/commons_collections:commons_collections",
        "//3rdparty/jvm/org/apache/avro:avro",
        "//3rdparty/jvm/org/mortbay/jetty:jetty_util",
        "//external:jar/org/apache/hbase/hbase_common"
    ],
    visibility = [
        "//visibility:public"
    ]
)



java_library(
    name = "hbase_hadoop2_compat",
    exports = [
        "//external:jar/org/apache/hbase/hbase_hadoop2_compat",
        ":hbase_metrics"
    ],
    visibility = [
        "//visibility:public"
    ]
)



java_library(
    name = "hbase_hadoop_compat",
    exports = [
        "//3rdparty/jvm/org/apache/commons:commons_math",
        "//external:jar/org/apache/hbase/hbase_hadoop_compat",
        ":hbase_metrics_api"
    ],
    visibility = [
        "//visibility:public"
    ]
)



java_library(
    name = "hbase_metrics",
    exports = [
        "//3rdparty/jvm/io/dropwizard/metrics:metrics_core",
        "//external:jar/org/apache/hbase/hbase_metrics"
    ],
    visibility = [
        "//visibility:public"
    ]
)



java_library(
    name = "hbase_metrics_api",
    exports = [
        "//external:jar/org/apache/hbase/hbase_metrics_api"
    ],
    visibility = [
        "//visibility:public"
    ]
)



java_library(
    name = "hbase_protocol",
    exports = [
        "//external:jar/org/apache/hbase/hbase_protocol"
    ],
    visibility = [
        "//visibility:public"
    ]
)



java_library(
    name = "hbase_shaded_client",
    exports = [
        "//3rdparty/jvm/com/github/stephenc/findbugs:findbugs_annotations",
        "//3rdparty/jvm/commons_logging:commons_logging",
        "//3rdparty/jvm/junit:junit",
        "//3rdparty/jvm/log4j:log4j",
        "//3rdparty/jvm/org/apache/htrace:htrace_core",
        "//3rdparty/jvm/org/apache/yetus:audience_annotations",
        "//3rdparty/jvm/org/slf4j:slf4j_api",
        "//external:jar/org/apache/hbase/hbase_shaded_client"
    ],
    visibility = [
        "//visibility:public"
    ]
)


