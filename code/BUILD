sh_binary(
    name = "metacentrum_distant_supervision_train",
    srcs = [
        "metacentrum_distant_supervision_train.sh",
    ],
    deps = [
        ":common",
    ],
    data = [
        ":distant_supervision_train_main",
    ],
)

py_binary(
    name = "distant_supervision_train_main",
    srcs = [
        "distant_supervision_train_main.py",
        "training_samples_pb2.py",
    ],
    deps = [
        ":file_util_lib",
    ]
)

py_binary(
    name = "launch_get_training_samples_main",
    srcs = [
        "launch_get_training_samples_main.py",
    ],
    deps = [
        ":pbs_util_lib",
        ":paths_lib",
        ":get_training_samples_main",
    ],
)

py_library(
    name = "split_wiki_lib",
    srcs = [
        "split_wiki.py",
    ],
    deps = [
        ":file_util_lib",
    ],
)

py_binary(
    name = "split_wiki_main",
    srcs = [
        "split_wiki_main.py",
    ],
    deps = [
        ":split_wiki_lib",
    ],
)

py_test(
    name = "split_wiki_test",
    srcs = [
        "split_wiki_test.py",
    ],
    deps = [
        ":split_wiki_lib",
    ],
)

py_binary(
    name = "launch_split_wiki_main",
    srcs = [
        "launch_split_wiki_main.py",
    ],
    deps = [
        ":split_wiki_main",
        ":file_util_lib",
        ":pbs_util_lib",
        ":paths_lib",
    ],
)

py_library(
    name = "pbs_util_lib",
    srcs = [
        "pbs_util.py",
    ],
)

sh_binary(
    name = "metacentrum_add_negative_samples",
    srcs = [
        "metacentrum_add_negative_samples.sh",
    ],
    deps = [
        ":common",
    ],
    data = [
        ":add_negative_samples_main",
    ],
)

sh_library(
    name = "common",
    srcs = [
        "common.sh",
    ],
)

py_binary(
    name = "add_negative_samples_main",
    srcs = [
        "add_negative_samples_main.py",
        "get_training_samples.py",
        "sentence_pb2.py",
        "training_samples_pb2.py",
    ],
    deps = [
        ":wikidata_lib",
        ":file_util_lib",
    ],
)

py_library(
    name = "file_util_lib",
    srcs = [
        "file_util.py",
    ],
)

py_library(
    name = "paths_lib",
    srcs = [
        "paths.py",
    ],
)

py_library(
    name = "spotlight_lib",
    srcs = [
        "spotlight.py",
    ],
)

py_test(
    name = "spotlight_test",
    srcs = [
        "spotlight_test.py",
    ],
    deps = [
        ":spotlight_lib",
    ],
)

py_binary(
    name = "metacentrum_spotlight_main",
    srcs = [
        "metacentrum_spotlight_main.py",
    ],
    deps = [
        ":spotlight_lib",
        ":paths_lib",
    ]
)

py_binary(
    name = "show_training_samples",
    srcs = [
        "show_training_samples.py",
        "training_samples_pb2.py",
    ],
    deps = [
        ":wikidata_lib",
    ],
)

sh_binary(
    name = "annotate_coreferences",
    srcs = [
        "annotate_coreferences.sh",
    ],
    data = [
        ":annotate_coreferences_main",
    ],
    deps = [
        ":common",
    ],
)

py_library(
    name = "annotate_coreferences_lib",
    srcs = [
        "annotate_coreferences.py",
        "sentence_pb2.py",
    ],
    deps = [
        ":dbpedia_lib",
    ],
)

py_binary(
    name = "annotate_coreferences_main",
    srcs = [
        "annotate_coreferences_main.py",
    ],
    deps = [
        ":annotate_coreferences_lib",
        ":paths_lib",
        ":file_util_lib",
    ],
)

py_library(
    name = "dbpedia_lib",
    srcs = [
        "dbpedia.py",
    ],
    deps = [
        ":json_cache_lib",
        ":sparql_client_lib",
        ":wikidata_util_lib",
    ],
)

py_test(
    name = "dbpedia_test",
    srcs = [
        "dbpedia_test.py",
    ],
    deps = [
        ":dbpedia_lib",
    ],
)

py_library(
    name = "get_training_samples_lib",
    srcs = [
        "get_training_samples.py",
        "sentence_pb2.py",
        "training_samples_pb2.py",
        "relations.py",
    ],
    deps = [
        ":file_util_lib",
    ]
)

py_binary(
    name = "get_training_samples_main",
    srcs = [
        "get_training_samples_main.py",
        "sentence_pb2.py",
    ],
    deps = [
        ":get_training_samples_lib",
        ":wikidata_lib",
        ":file_util_lib",
    ],
)

py_library(
    name = "json_cache_lib",
    srcs = [
        "json_cache.py",
    ],
    deps = [
        ":paths_lib",
        ":file_util_lib",
    ],
)

py_library(
    name = "sparql_client_lib",
    srcs = [
        "sparql_client.py",
    ],
)

py_library(
    name = "wikidata_util_lib",
    srcs = [
        "wikidata_util.py",
    ],
)

py_library(
    name = "wikidata_lib",
    srcs = [
        "wikidata.py",
    ],
    deps = [
        ":json_cache_lib",
        ":sparql_client_lib",
        ":wikidata_util_lib",
    ],
)

py_test(
    name = "wikidata_test",
    srcs = [
        "wikidata_test.py",
    ],
    deps = [
        ":wikidata_lib",
    ]
)

genrule(
    name = "sentence_proto",
    srcs = [
        "sentence.proto",
    ],
    outs = [
        "sentence_pb2.py",
    ],
    cmd = "protoc -I=. --python_out=$(GENDIR)/ $(location :sentence.proto)"
)

genrule(
    name = "training_samples_proto",
    srcs = [
        "training_samples.proto",
    ],
    outs = [
        "training_samples_pb2.py",
    ],
    cmd = "protoc -I=. --python_out=$(GENDIR)/ $(location :training_samples.proto)"
)

py_binary(
    name = "nlpize_articles_main",
    srcs = [
        "nlpize_articles_main.py",
    ],
    deps = [
        ":file_util_lib",
        ":paths_lib",
    ],
)

py_binary(
    name = "launch_nlpize_articles_main",
    srcs = [
        "launch_nlpize_articles_main.py",
    ],
    deps = [
        ":file_util_lib",
        ":paths_lib",
        ":pbs_util_lib",
        ":nlpize_articles_main",
    ],
)

py_test(
    name = "annotate_coreferences_test",
    srcs = [
        "annotate_coreferences_test.py",
    ],
    deps = [
        ":get_training_samples_lib",
        ":annotate_coreferences_lib",
        ":parse_xmls_to_protos_lib",
    ],
)

py_library(
    name = "parse_xmls_to_protos_lib",
    srcs = [
        "parse_xmls_to_protos.py",
        "sentence_pb2.py",
    ],
)

py_binary(
    name = "parse_xmls_to_protos_main",
    srcs = [
        "parse_xmls_to_protos_main.py",
    ],
    deps = [
        ":parse_xmls_to_protos_lib",
    ],
)


# The following dependencies were calculated from:
# org.apache.hadoop:hadoop-common:2.6.0
# org.apache.hadoop:hadoop-mapreduce-client-core:2.6.0
# edu.stanford.nlp:stanford-corenlp:3.6.0
# edu.stanford.nlp:stanford-corenlp:models:3.6.0


java_library(
    name = "com_google_code_findbugs_jsr305",
    visibility = ["//visibility:public"],
    exports = [
        "@com_google_code_findbugs_jsr305//jar",
    ],
)

java_library(
    name = "javax_xml_stream_stax_api",
    visibility = ["//visibility:public"],
    exports = [
        "@javax_xml_stream_stax_api//jar",
    ],
)

java_library(
    name = "aopalliance_aopalliance",
    visibility = ["//visibility:public"],
    exports = [
        "@aopalliance_aopalliance//jar",
    ],
)

java_library(
    name = "io_netty_netty",
    visibility = ["//visibility:public"],
    exports = [
        "@io_netty_netty//jar",
    ],
)

java_library(
    name = "commons_io_commons_io",
    visibility = ["//visibility:public"],
    exports = [
        "@commons_io_commons_io//jar",
    ],
)

java_library(
    name = "javax_json_javax_json_api",
    visibility = ["//visibility:public"],
    exports = [
        "@javax_json_javax_json_api//jar",
    ],
)

java_library(
    name = "commons_configuration_commons_configuration",
    visibility = ["//visibility:public"],
    exports = [
        "@commons_configuration_commons_configuration//jar",
    ],
)

java_library(
    name = "commons_codec_commons_codec",
    visibility = ["//visibility:public"],
    exports = [
        "@commons_codec_commons_codec//jar",
    ],
)

java_library(
    name = "org_apache_hadoop_hadoop_auth",
    visibility = ["//visibility:public"],
    exports = [
        "@org_apache_hadoop_hadoop_auth//jar",
        "@com_google_guava_guava//jar",
        "@commons_codec_commons_codec//jar",
        "@io_netty_netty//jar",
        "@jline_jline//jar",
        "@log4j_log4j//jar",
        "@org_apache_curator_curator_client//jar",
        "@org_apache_curator_curator_framework//jar",
        "@org_apache_directory_api_api_asn1_api//jar",
        "@org_apache_directory_api_api_util//jar",
        "@org_apache_directory_server_apacheds_i18n//jar",
        "@org_apache_directory_server_apacheds_kerberos_codec//jar",
        "@org_apache_httpcomponents_httpclient//jar",
        "@org_apache_zookeeper_zookeeper//jar",
        "@org_slf4j_slf4j_api//jar",
        "@org_slf4j_slf4j_log4j12//jar",
    ],
)

java_library(
    name = "com_sun_jersey_jersey_core",
    visibility = ["//visibility:public"],
    exports = [
        "@com_sun_jersey_jersey_core//jar",
    ],
)

java_library(
    name = "xml_apis_xml_apis",
    visibility = ["//visibility:public"],
    exports = [
        "@xml_apis_xml_apis//jar",
    ],
)

java_library(
    name = "asm_asm",
    visibility = ["//visibility:public"],
    exports = [
        "@asm_asm//jar",
    ],
)

java_library(
    name = "com_thoughtworks_paranamer_paranamer",
    visibility = ["//visibility:public"],
    exports = [
        "@com_thoughtworks_paranamer_paranamer//jar",
    ],
)

java_library(
    name = "com_google_inject_guice",
    visibility = ["//visibility:public"],
    exports = [
        "@com_google_inject_guice//jar",
        "@aopalliance_aopalliance//jar",
        "@asm_asm//jar",
        "@javax_inject_javax_inject//jar",
        "@org_sonatype_sisu_inject_cglib//jar",
    ],
)

java_library(
    name = "org_codehaus_jettison_jettison",
    visibility = ["//visibility:public"],
    exports = [
        "@org_codehaus_jettison_jettison//jar",
    ],
)

java_library(
    name = "org_xerial_snappy_snappy_java",
    visibility = ["//visibility:public"],
    exports = [
        "@org_xerial_snappy_snappy_java//jar",
    ],
)

java_library(
    name = "edu_stanford_nlp_stanford_corenlp",
    visibility = ["//visibility:public"],
    exports = [
        "@edu_stanford_nlp_stanford_corenlp//jar",
        "@com_googlecode_efficient_java_matrix_library_ejml//jar",
        "@com_io7m_xom_xom//jar",
        "@de_jollyday_jollyday//jar",
        "@javax_json_javax_json_api//jar",
        "@joda_time_joda_time//jar",
        "@org_slf4j_slf4j_api//jar",
    ],
)

java_library(
    name = "org_apache_avro_avro",
    visibility = ["//visibility:public"],
    exports = [
        "@org_apache_avro_avro//jar",
        "@com_thoughtworks_paranamer_paranamer//jar",
        "@org_apache_commons_commons_compress//jar",
        "@org_codehaus_jackson_jackson_core_asl//jar",
        "@org_codehaus_jackson_jackson_mapper_asl//jar",
        "@org_slf4j_slf4j_api//jar",
        "@org_tukaani_xz//jar",
        "@org_xerial_snappy_snappy_java//jar",
    ],
)

java_library(
    name = "net_java_dev_jets3t_jets3t",
    visibility = ["//visibility:public"],
    exports = [
        "@net_java_dev_jets3t_jets3t//jar",
        "@com_jamesmurty_utils_java_xmlbuilder//jar",
        "@commons_codec_commons_codec//jar",
        "@commons_logging_commons_logging//jar",
        "@org_apache_httpcomponents_httpclient//jar",
        "@org_apache_httpcomponents_httpcore//jar",
    ],
)

java_library(
    name = "org_apache_hadoop_hadoop_yarn_api",
    visibility = ["//visibility:public"],
    exports = [
        "@org_apache_hadoop_hadoop_yarn_api//jar",
        "@com_google_guava_guava//jar",
        "@com_google_protobuf_protobuf_java//jar",
        "@commons_lang_commons_lang//jar",
        "@commons_logging_commons_logging//jar",
        "@org_apache_hadoop_hadoop_annotations//jar",
    ],
)

java_library(
    name = "org_apache_commons_commons_math3",
    visibility = ["//visibility:public"],
    exports = [
        "@org_apache_commons_commons_math3//jar",
    ],
)

java_library(
    name = "org_apache_hadoop_hadoop_annotations",
    visibility = ["//visibility:public"],
    exports = [
        "@org_apache_hadoop_hadoop_annotations//jar",
    ],
)

java_library(
    name = "com_googlecode_efficient_java_matrix_library_ejml",
    visibility = ["//visibility:public"],
    exports = [
        "@com_googlecode_efficient_java_matrix_library_ejml//jar",
    ],
)

java_library(
    name = "org_apache_directory_server_apacheds_i18n",
    visibility = ["//visibility:public"],
    exports = [
        "@org_apache_directory_server_apacheds_i18n//jar",
        "@org_slf4j_slf4j_api//jar",
    ],
)

java_library(
    name = "javax_activation_activation",
    visibility = ["//visibility:public"],
    exports = [
        "@javax_activation_activation//jar",
    ],
)

java_library(
    name = "javax_inject_javax_inject",
    visibility = ["//visibility:public"],
    exports = [
        "@javax_inject_javax_inject//jar",
    ],
)

java_library(
    name = "xalan_xalan",
    visibility = ["//visibility:public"],
    exports = [
        "@xalan_xalan//jar",
        "@xml_apis_xml_apis//jar",
    ],
)

java_library(
    name = "org_codehaus_jackson_jackson_core_asl",
    visibility = ["//visibility:public"],
    exports = [
        "@org_codehaus_jackson_jackson_core_asl//jar",
    ],
)

java_library(
    name = "com_sun_jersey_contribs_jersey_guice",
    visibility = ["//visibility:public"],
    exports = [
        "@com_sun_jersey_contribs_jersey_guice//jar",
        "@com_google_inject_extensions_guice_servlet//jar",
        "@com_google_inject_guice//jar",
        "@com_sun_jersey_jersey_server//jar",
        "@javax_inject_javax_inject//jar",
    ],
)

java_library(
    name = "com_jamesmurty_utils_java_xmlbuilder",
    visibility = ["//visibility:public"],
    exports = [
        "@com_jamesmurty_utils_java_xmlbuilder//jar",
    ],
)

java_library(
    name = "javax_xml_bind_jaxb_api",
    visibility = ["//visibility:public"],
    exports = [
        "@javax_xml_bind_jaxb_api//jar",
        "@javax_activation_activation//jar",
        "@javax_xml_stream_stax_api//jar",
    ],
)

java_library(
    name = "org_codehaus_jackson_jackson_xc",
    visibility = ["//visibility:public"],
    exports = [
        "@org_codehaus_jackson_jackson_xc//jar",
        "@org_codehaus_jackson_jackson_core_asl//jar",
        "@org_codehaus_jackson_jackson_mapper_asl//jar",
    ],
)

java_library(
    name = "org_apache_curator_curator_client",
    visibility = ["//visibility:public"],
    exports = [
        "@org_apache_curator_curator_client//jar",
        "@com_google_guava_guava//jar",
        "@org_apache_zookeeper_zookeeper//jar",
        "@org_slf4j_slf4j_api//jar",
    ],
)

java_library(
    name = "org_apache_curator_curator_recipes",
    visibility = ["//visibility:public"],
    exports = [
        "@org_apache_curator_curator_recipes//jar",
        "@com_google_guava_guava//jar",
        "@org_apache_curator_curator_framework//jar",
        "@org_apache_zookeeper_zookeeper//jar",
    ],
)

java_library(
    name = "joda_time_joda_time",
    visibility = ["//visibility:public"],
    exports = [
        "@joda_time_joda_time//jar",
    ],
)

java_library(
    name = "org_apache_httpcomponents_httpcore",
    visibility = ["//visibility:public"],
    exports = [
        "@org_apache_httpcomponents_httpcore//jar",
    ],
)

java_library(
    name = "log4j_log4j",
    visibility = ["//visibility:public"],
    exports = [
        "@log4j_log4j//jar",
    ],
)

java_library(
    name = "com_google_protobuf_protobuf_java",
    visibility = ["//visibility:public"],
    exports = [
        "@com_google_protobuf_protobuf_java//jar",
    ],
)

java_library(
    name = "javax_servlet_servlet_api",
    visibility = ["//visibility:public"],
    exports = [
        "@javax_servlet_servlet_api//jar",
    ],
)

java_library(
    name = "jline_jline",
    visibility = ["//visibility:public"],
    exports = [
        "@jline_jline//jar",
    ],
)

java_library(
    name = "org_sonatype_sisu_inject_cglib",
    visibility = ["//visibility:public"],
    exports = [
        "@org_sonatype_sisu_inject_cglib//jar",
        "@asm_asm//jar",
    ],
)

java_library(
    name = "de_jollyday_jollyday",
    visibility = ["//visibility:public"],
    exports = [
        "@de_jollyday_jollyday//jar",
        "@javax_xml_bind_jaxb_api//jar",
        "@joda_time_joda_time//jar",
    ],
)

java_library(
    name = "org_apache_zookeeper_zookeeper",
    visibility = ["//visibility:public"],
    exports = [
        "@org_apache_zookeeper_zookeeper//jar",
        "@io_netty_netty//jar",
        "@jline_jline//jar",
        "@log4j_log4j//jar",
        "@org_slf4j_slf4j_api//jar",
        "@org_slf4j_slf4j_log4j12//jar",
    ],
)

java_library(
    name = "org_slf4j_slf4j_log4j12",
    visibility = ["//visibility:public"],
    exports = [
        "@org_slf4j_slf4j_log4j12//jar",
        "@log4j_log4j//jar",
        "@org_slf4j_slf4j_api//jar",
    ],
)

java_library(
    name = "com_sun_jersey_jersey_client",
    visibility = ["//visibility:public"],
    exports = [
        "@com_sun_jersey_jersey_client//jar",
        "@com_sun_jersey_jersey_core//jar",
    ],
)

java_library(
    name = "commons_cli_commons_cli",
    visibility = ["//visibility:public"],
    exports = [
        "@commons_cli_commons_cli//jar",
    ],
)

java_library(
    name = "com_google_inject_extensions_guice_servlet",
    visibility = ["//visibility:public"],
    exports = [
        "@com_google_inject_extensions_guice_servlet//jar",
        "@aopalliance_aopalliance//jar",
        "@asm_asm//jar",
        "@com_google_inject_guice//jar",
        "@javax_inject_javax_inject//jar",
        "@org_sonatype_sisu_inject_cglib//jar",
    ],
)

java_library(
    name = "xerces_xercesImpl",
    visibility = ["//visibility:public"],
    exports = [
        "@xerces_xercesImpl//jar",
        "@xml_apis_xml_apis//jar",
    ],
)

java_library(
    name = "commons_net_commons_net",
    visibility = ["//visibility:public"],
    exports = [
        "@commons_net_commons_net//jar",
    ],
)

java_library(
    name = "com_sun_jersey_jersey_server",
    visibility = ["//visibility:public"],
    exports = [
        "@com_sun_jersey_jersey_server//jar",
        "@asm_asm//jar",
        "@com_sun_jersey_jersey_core//jar",
    ],
)

java_library(
    name = "org_apache_directory_server_apacheds_kerberos_codec",
    visibility = ["//visibility:public"],
    exports = [
        "@org_apache_directory_server_apacheds_kerberos_codec//jar",
        "@org_apache_directory_api_api_asn1_api//jar",
        "@org_apache_directory_api_api_util//jar",
        "@org_apache_directory_server_apacheds_i18n//jar",
        "@org_slf4j_slf4j_api//jar",
    ],
)

java_library(
    name = "org_mortbay_jetty_jetty_util",
    visibility = ["//visibility:public"],
    exports = [
        "@org_mortbay_jetty_jetty_util//jar",
    ],
)

java_library(
    name = "xmlenc_xmlenc",
    visibility = ["//visibility:public"],
    exports = [
        "@xmlenc_xmlenc//jar",
    ],
)

java_library(
    name = "org_apache_hadoop_hadoop_common",
    visibility = ["//visibility:public"],
    exports = [
        "@org_apache_hadoop_hadoop_common//jar",
        "@asm_asm//jar",
        "@com_google_code_findbugs_jsr305//jar",
        "@com_google_code_gson_gson//jar",
        "@com_google_guava_guava//jar",
        "@com_google_protobuf_protobuf_java//jar",
        "@com_jamesmurty_utils_java_xmlbuilder//jar",
        "@com_jcraft_jsch//jar",
        "@com_sun_jersey_jersey_core//jar",
        "@com_sun_jersey_jersey_json//jar",
        "@com_sun_jersey_jersey_server//jar",
        "@com_sun_xml_bind_jaxb_impl//jar",
        "@com_thoughtworks_paranamer_paranamer//jar",
        "@commons_cli_commons_cli//jar",
        "@commons_codec_commons_codec//jar",
        "@commons_collections_commons_collections//jar",
        "@commons_configuration_commons_configuration//jar",
        "@commons_httpclient_commons_httpclient//jar",
        "@commons_io_commons_io//jar",
        "@commons_lang_commons_lang//jar",
        "@commons_logging_commons_logging//jar",
        "@commons_net_commons_net//jar",
        "@io_netty_netty//jar",
        "@javax_activation_activation//jar",
        "@javax_servlet_servlet_api//jar",
        "@javax_xml_bind_jaxb_api//jar",
        "@javax_xml_stream_stax_api//jar",
        "@jline_jline//jar",
        "@log4j_log4j//jar",
        "@net_java_dev_jets3t_jets3t//jar",
        "@org_apache_avro_avro//jar",
        "@org_apache_commons_commons_compress//jar",
        "@org_apache_commons_commons_math3//jar",
        "@org_apache_curator_curator_client//jar",
        "@org_apache_curator_curator_framework//jar",
        "@org_apache_curator_curator_recipes//jar",
        "@org_apache_directory_api_api_asn1_api//jar",
        "@org_apache_directory_api_api_util//jar",
        "@org_apache_directory_server_apacheds_i18n//jar",
        "@org_apache_directory_server_apacheds_kerberos_codec//jar",
        "@org_apache_hadoop_hadoop_annotations//jar",
        "@org_apache_hadoop_hadoop_auth//jar",
        "@org_apache_httpcomponents_httpclient//jar",
        "@org_apache_httpcomponents_httpcore//jar",
        "@org_apache_zookeeper_zookeeper//jar",
        "@org_codehaus_jackson_jackson_core_asl//jar",
        "@org_codehaus_jackson_jackson_jaxrs//jar",
        "@org_codehaus_jackson_jackson_mapper_asl//jar",
        "@org_codehaus_jackson_jackson_xc//jar",
        "@org_codehaus_jettison_jettison//jar",
        "@org_htrace_htrace_core//jar",
        "@org_mortbay_jetty_jetty//jar",
        "@org_mortbay_jetty_jetty_util//jar",
        "@org_slf4j_slf4j_api//jar",
        "@org_slf4j_slf4j_log4j12//jar",
        "@org_tukaani_xz//jar",
        "@org_xerial_snappy_snappy_java//jar",
        "@xmlenc_xmlenc//jar",
    ],
)

java_library(
    name = "commons_collections_commons_collections",
    visibility = ["//visibility:public"],
    exports = [
        "@commons_collections_commons_collections//jar",
    ],
)

java_library(
    name = "org_tukaani_xz",
    visibility = ["//visibility:public"],
    exports = [
        "@org_tukaani_xz//jar",
    ],
)

java_library(
    name = "com_jcraft_jsch",
    visibility = ["//visibility:public"],
    exports = [
        "@com_jcraft_jsch//jar",
    ],
)

java_library(
    name = "commons_logging_commons_logging",
    visibility = ["//visibility:public"],
    exports = [
        "@commons_logging_commons_logging//jar",
    ],
)

java_library(
    name = "org_slf4j_slf4j_api",
    visibility = ["//visibility:public"],
    exports = [
        "@org_slf4j_slf4j_api//jar",
    ],
)

java_library(
    name = "org_apache_commons_commons_compress",
    visibility = ["//visibility:public"],
    exports = [
        "@org_apache_commons_commons_compress//jar",
        "@org_tukaani_xz//jar",
    ],
)

java_library(
    name = "org_mortbay_jetty_jetty",
    visibility = ["//visibility:public"],
    exports = [
        "@org_mortbay_jetty_jetty//jar",
        "@org_mortbay_jetty_jetty_util//jar",
    ],
)

java_library(
    name = "com_google_code_gson_gson",
    visibility = ["//visibility:public"],
    exports = [
        "@com_google_code_gson_gson//jar",
    ],
)

java_library(
    name = "org_apache_directory_api_api_util",
    visibility = ["//visibility:public"],
    exports = [
        "@org_apache_directory_api_api_util//jar",
        "@org_slf4j_slf4j_api//jar",
    ],
)

java_library(
    name = "org_apache_hadoop_hadoop_mapreduce_client_core",
    visibility = ["//visibility:public"],
    exports = [
        "@org_apache_hadoop_hadoop_mapreduce_client_core//jar",
        "@aopalliance_aopalliance//jar",
        "@asm_asm//jar",
        "@com_google_guava_guava//jar",
        "@com_google_inject_extensions_guice_servlet//jar",
        "@com_google_inject_guice//jar",
        "@com_google_protobuf_protobuf_java//jar",
        "@com_sun_jersey_contribs_jersey_guice//jar",
        "@com_sun_jersey_jersey_client//jar",
        "@com_sun_jersey_jersey_core//jar",
        "@com_sun_jersey_jersey_json//jar",
        "@com_sun_jersey_jersey_server//jar",
        "@commons_cli_commons_cli//jar",
        "@commons_codec_commons_codec//jar",
        "@commons_io_commons_io//jar",
        "@commons_lang_commons_lang//jar",
        "@commons_logging_commons_logging//jar",
        "@io_netty_netty//jar",
        "@javax_inject_javax_inject//jar",
        "@javax_servlet_servlet_api//jar",
        "@javax_xml_bind_jaxb_api//jar",
        "@log4j_log4j//jar",
        "@org_apache_avro_avro//jar",
        "@org_apache_commons_commons_compress//jar",
        "@org_apache_hadoop_hadoop_annotations//jar",
        "@org_apache_hadoop_hadoop_yarn_api//jar",
        "@org_apache_hadoop_hadoop_yarn_common//jar",
        "@org_codehaus_jackson_jackson_core_asl//jar",
        "@org_codehaus_jackson_jackson_jaxrs//jar",
        "@org_codehaus_jackson_jackson_mapper_asl//jar",
        "@org_codehaus_jackson_jackson_xc//jar",
        "@org_mortbay_jetty_jetty_util//jar",
        "@org_slf4j_slf4j_api//jar",
        "@org_slf4j_slf4j_log4j12//jar",
        "@org_sonatype_sisu_inject_cglib//jar",
    ],
)

java_library(
    name = "org_apache_httpcomponents_httpclient",
    visibility = ["//visibility:public"],
    exports = [
        "@org_apache_httpcomponents_httpclient//jar",
        "@org_apache_httpcomponents_httpcore//jar",
    ],
)

java_library(
    name = "com_sun_xml_bind_jaxb_impl",
    visibility = ["//visibility:public"],
    exports = [
        "@com_sun_xml_bind_jaxb_impl//jar",
        "@javax_activation_activation//jar",
        "@javax_xml_bind_jaxb_api//jar",
        "@javax_xml_stream_stax_api//jar",
    ],
)

java_library(
    name = "commons_httpclient_commons_httpclient",
    visibility = ["//visibility:public"],
    exports = [
        "@commons_httpclient_commons_httpclient//jar",
    ],
)

java_library(
    name = "org_apache_directory_api_api_asn1_api",
    visibility = ["//visibility:public"],
    exports = [
        "@org_apache_directory_api_api_asn1_api//jar",
        "@org_slf4j_slf4j_api//jar",
    ],
)

java_library(
    name = "org_htrace_htrace_core",
    visibility = ["//visibility:public"],
    exports = [
        "@org_htrace_htrace_core//jar",
        "@com_google_guava_guava//jar",
        "@commons_logging_commons_logging//jar",
        "@org_mortbay_jetty_jetty_util//jar",
    ],
)

java_library(
    name = "com_io7m_xom_xom",
    visibility = ["//visibility:public"],
    exports = [
        "@com_io7m_xom_xom//jar",
        "@xalan_xalan//jar",
        "@xerces_xercesImpl//jar",
        "@xml_apis_xml_apis//jar",
    ],
)

java_library(
    name = "com_google_guava_guava",
    visibility = ["//visibility:public"],
    exports = [
        "@com_google_guava_guava//jar",
        "@com_google_code_findbugs_jsr305//jar",
    ],
)

java_library(
    name = "org_codehaus_jackson_jackson_mapper_asl",
    visibility = ["//visibility:public"],
    exports = [
        "@org_codehaus_jackson_jackson_mapper_asl//jar",
        "@org_codehaus_jackson_jackson_core_asl//jar",
    ],
)

java_library(
    name = "com_sun_jersey_jersey_json",
    visibility = ["//visibility:public"],
    exports = [
        "@com_sun_jersey_jersey_json//jar",
        "@com_sun_jersey_jersey_core//jar",
        "@com_sun_xml_bind_jaxb_impl//jar",
        "@javax_activation_activation//jar",
        "@javax_xml_bind_jaxb_api//jar",
        "@javax_xml_stream_stax_api//jar",
        "@org_codehaus_jackson_jackson_core_asl//jar",
        "@org_codehaus_jackson_jackson_jaxrs//jar",
        "@org_codehaus_jackson_jackson_mapper_asl//jar",
        "@org_codehaus_jackson_jackson_xc//jar",
        "@org_codehaus_jettison_jettison//jar",
    ],
)

java_library(
    name = "org_codehaus_jackson_jackson_jaxrs",
    visibility = ["//visibility:public"],
    exports = [
        "@org_codehaus_jackson_jackson_jaxrs//jar",
        "@org_codehaus_jackson_jackson_core_asl//jar",
        "@org_codehaus_jackson_jackson_mapper_asl//jar",
    ],
)

java_library(
    name = "commons_lang_commons_lang",
    visibility = ["//visibility:public"],
    exports = [
        "@commons_lang_commons_lang//jar",
    ],
)

java_library(
    name = "org_apache_curator_curator_framework",
    visibility = ["//visibility:public"],
    exports = [
        "@org_apache_curator_curator_framework//jar",
        "@com_google_guava_guava//jar",
        "@org_apache_curator_curator_client//jar",
        "@org_apache_zookeeper_zookeeper//jar",
        "@org_slf4j_slf4j_api//jar",
    ],
)

java_library(
    name = "org_apache_hadoop_hadoop_yarn_common",
    visibility = ["//visibility:public"],
    exports = [
        "@org_apache_hadoop_hadoop_yarn_common//jar",
        "@aopalliance_aopalliance//jar",
        "@asm_asm//jar",
        "@com_google_guava_guava//jar",
        "@com_google_inject_extensions_guice_servlet//jar",
        "@com_google_inject_guice//jar",
        "@com_google_protobuf_protobuf_java//jar",
        "@com_sun_jersey_contribs_jersey_guice//jar",
        "@com_sun_jersey_jersey_client//jar",
        "@com_sun_jersey_jersey_core//jar",
        "@com_sun_jersey_jersey_json//jar",
        "@com_sun_jersey_jersey_server//jar",
        "@commons_cli_commons_cli//jar",
        "@commons_codec_commons_codec//jar",
        "@commons_io_commons_io//jar",
        "@commons_lang_commons_lang//jar",
        "@commons_logging_commons_logging//jar",
        "@javax_inject_javax_inject//jar",
        "@javax_servlet_servlet_api//jar",
        "@javax_xml_bind_jaxb_api//jar",
        "@log4j_log4j//jar",
        "@org_apache_commons_commons_compress//jar",
        "@org_apache_hadoop_hadoop_annotations//jar",
        "@org_apache_hadoop_hadoop_yarn_api//jar",
        "@org_codehaus_jackson_jackson_core_asl//jar",
        "@org_codehaus_jackson_jackson_jaxrs//jar",
        "@org_codehaus_jackson_jackson_mapper_asl//jar",
        "@org_codehaus_jackson_jackson_xc//jar",
        "@org_mortbay_jetty_jetty_util//jar",
        "@org_slf4j_slf4j_api//jar",
        "@org_sonatype_sisu_inject_cglib//jar",
    ],
)

