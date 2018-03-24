java_library(
    name = "hadoop_annotations",
    exports = [
        "//external:jar/org/apache/hadoop/hadoop_annotations"
    ],
    visibility = [
        "//visibility:public"
    ]
)



java_library(
    name = "hadoop_auth",
    exports = [
        "//3rdparty/jvm/org/apache/curator:curator_framework",
        "//3rdparty/jvm/org/apache/directory/server:apacheds_kerberos_codec",
        "//3rdparty/jvm/org/apache/httpcomponents:httpclient",
        "//external:jar/org/apache/hadoop/hadoop_auth"
    ],
    visibility = [
        "//visibility:public"
    ]
)



java_library(
    name = "hadoop_common",
    exports = [
        "//3rdparty/jvm/com/google/code/gson:gson",
        "//3rdparty/jvm/com/jcraft:jsch",
        "//3rdparty/jvm/commons_cli:commons_cli",
        "//3rdparty/jvm/commons_configuration:commons_configuration",
        "//3rdparty/jvm/commons_httpclient:commons_httpclient",
        "//3rdparty/jvm/commons_net:commons_net",
        "//3rdparty/jvm/org/apache/commons:commons_compress",
        "//3rdparty/jvm/org/apache/commons:commons_math3",
        "//3rdparty/jvm/org/apache/curator:curator_client",
        "//3rdparty/jvm/org/apache/curator:curator_recipes",
        "//3rdparty/jvm/org/mortbay/jetty:jetty_sslengine",
        "//3rdparty/jvm/xmlenc:xmlenc",
        "//external:jar/org/apache/hadoop/hadoop_common",
        ":hadoop_annotations"
    ],
    visibility = [
        "//visibility:public"
    ]
)



java_library(
    name = "hadoop_mapreduce_client_core",
    exports = [
        "//external:jar/org/apache/hadoop/hadoop_mapreduce_client_core",
        ":hadoop_yarn_common"
    ],
    visibility = [
        "//visibility:public"
    ]
)



java_library(
    name = "hadoop_yarn_api",
    exports = [
        "//external:jar/org/apache/hadoop/hadoop_yarn_api"
    ],
    visibility = [
        "//visibility:public"
    ]
)



java_library(
    name = "hadoop_yarn_common",
    exports = [
        "//3rdparty/jvm/javax/xml/bind:jaxb_api",
        "//external:jar/org/apache/hadoop/hadoop_yarn_common",
        ":hadoop_yarn_api"
    ],
    visibility = [
        "//visibility:public"
    ]
)


