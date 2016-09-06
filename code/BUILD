sh_library(
    name = "common",
    srcs = [
        "common.sh",
    ],
)

genrule(
    name = "sentence_proto",
    srcs = [
        "sentence.proto",
    ],
    outs = [
        "sentence_pb2.py",
        "Sentence.java",
    ],
    visibility = ["//visibility:public"],
    cmd = "protoc -I=. " +
        "--python_out=$(GENDIR)/ " +
        "--java_out=$(GENDIR)/ " +
        "$(location :sentence.proto)"
)

genrule(
    name = "training_samples_proto",
    srcs = [
        "training_samples.proto",
    ],
    outs = [
        "training_samples_pb2.py",
        "TrainingSamples.java",
    ],
    visibility = ["//visibility:public"],
    cmd = "protoc -I=. " +
        "--python_out=$(GENDIR)/ " +
        "--java_out=$(GENDIR)/ " +
        "$(location :training_samples.proto)"
)

# The following dependencies were calculated from:
# org.apache.hadoop:hadoop-common:2.6.0
# org.apache.hadoop:hadoop-mapreduce-client-core:2.6.0
# edu.stanford.nlp:stanford-corenlp:3.6.0
# org.json:json:20160810
# org.apache.jena:apache-jena-libs:3.1.0
# org.apache.httpcomponents:httpclient:4.2.6
# org.apache.httpcomponents:httpcore:4.2.5
# com.google.protobuf:protobuf-java:3.0.0
# javax.xml.parsers:jaxp-api:1.4
# org.apache.hbase:hbase-client:1.2.2
# org.apache.hbase:hbase-server:1.2.2


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
    name = "org_apache_jena_apache_jena_libs",
    visibility = ["//visibility:public"],
    exports = [
        "@org_apache_jena_apache_jena_libs//jar",
        "@com_fasterxml_jackson_core_jackson_annotations//jar",
        "@com_fasterxml_jackson_core_jackson_core//jar",
        "@com_fasterxml_jackson_core_jackson_databind//jar",
        "@com_github_andrewoma_dexx_collection//jar",
        "@com_github_jsonld_java_jsonld_java//jar",
        "@commons_cli_commons_cli//jar",
        "@commons_io_commons_io//jar",
        "@org_apache_commons_commons_csv//jar",
        "@org_apache_commons_commons_lang3//jar",
        "@org_apache_httpcomponents_httpclient//jar",
        "@org_apache_httpcomponents_httpclient_cache//jar",
        "@org_apache_jena_jena_arq//jar",
        "@org_apache_jena_jena_base//jar",
        "@org_apache_jena_jena_core//jar",
        "@org_apache_jena_jena_iri//jar",
        "@org_apache_jena_jena_shaded_guava//jar",
        "@org_apache_jena_jena_tdb//jar",
        "@org_apache_thrift_libthrift//jar",
        "@org_slf4j_jcl_over_slf4j//jar",
        "@org_slf4j_slf4j_api//jar",
        "@xerces_xercesImpl//jar",
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
    name = "org_apache_hadoop_hadoop_annotations",
    visibility = ["//visibility:public"],
    exports = [
        "@org_apache_hadoop_hadoop_annotations//jar",
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
    name = "xalan_xalan",
    visibility = ["//visibility:public"],
    exports = [
        "@xalan_xalan//jar",
        "@xml_apis_xml_apis//jar",
    ],
)

java_library(
    name = "com_github_jsonld_java_jsonld_java",
    visibility = ["//visibility:public"],
    exports = [
        "@com_github_jsonld_java_jsonld_java//jar",
        "@com_fasterxml_jackson_core_jackson_annotations//jar",
        "@com_fasterxml_jackson_core_jackson_core//jar",
        "@com_fasterxml_jackson_core_jackson_databind//jar",
        "@commons_io_commons_io//jar",
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
    name = "org_apache_hbase_hbase_common",
    visibility = ["//visibility:public"],
    exports = [
        "@org_apache_hbase_hbase_common//jar",
        "@com_github_stephenc_findbugs_findbugs_annotations//jar",
        "@com_google_guava_guava//jar",
        "@com_google_protobuf_protobuf_java//jar",
        "@commons_codec_commons_codec//jar",
        "@commons_collections_commons_collections//jar",
        "@commons_io_commons_io//jar",
        "@commons_lang_commons_lang//jar",
        "@commons_logging_commons_logging//jar",
        "@junit_junit//jar",
        "@log4j_log4j//jar",
        "@org_apache_hbase_hbase_annotations//jar",
        "@org_apache_hbase_hbase_protocol//jar",
        "@org_apache_htrace_htrace_core//jar",
        "@org_mortbay_jetty_jetty_util//jar",
    ],
)

java_library(
    name = "com_fasterxml_jackson_core_jackson_databind",
    visibility = ["//visibility:public"],
    exports = [
        "@com_fasterxml_jackson_core_jackson_databind//jar",
        "@com_fasterxml_jackson_core_jackson_annotations//jar",
        "@com_fasterxml_jackson_core_jackson_core//jar",
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
    name = "com_fasterxml_jackson_core_jackson_core",
    visibility = ["//visibility:public"],
    exports = [
        "@com_fasterxml_jackson_core_jackson_core//jar",
    ],
)

java_library(
    name = "com_yammer_metrics_metrics_core",
    visibility = ["//visibility:public"],
    exports = [
        "@com_yammer_metrics_metrics_core//jar",
        "@org_slf4j_slf4j_api//jar",
    ],
)

java_library(
    name = "org_apache_hbase_hbase_protocol",
    visibility = ["//visibility:public"],
    exports = [
        "@org_apache_hbase_hbase_protocol//jar",
        "@com_github_stephenc_findbugs_findbugs_annotations//jar",
        "@com_google_protobuf_protobuf_java//jar",
        "@commons_logging_commons_logging//jar",
        "@junit_junit//jar",
        "@log4j_log4j//jar",
        "@org_apache_hbase_hbase_annotations//jar",
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
    name = "org_jruby_jcodings_jcodings",
    visibility = ["//visibility:public"],
    exports = [
        "@org_jruby_jcodings_jcodings//jar",
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
    name = "org_apache_hbase_hbase_client",
    visibility = ["//visibility:public"],
    exports = [
        "@org_apache_hbase_hbase_client//jar",
        "@com_github_stephenc_findbugs_findbugs_annotations//jar",
        "@com_google_guava_guava//jar",
        "@com_google_protobuf_protobuf_java//jar",
        "@com_yammer_metrics_metrics_core//jar",
        "@commons_codec_commons_codec//jar",
        "@commons_collections_commons_collections//jar",
        "@commons_io_commons_io//jar",
        "@commons_lang_commons_lang//jar",
        "@commons_logging_commons_logging//jar",
        "@io_netty_netty_all//jar",
        "@junit_junit//jar",
        "@log4j_log4j//jar",
        "@org_apache_hbase_hbase_annotations//jar",
        "@org_apache_hbase_hbase_common//jar",
        "@org_apache_hbase_hbase_protocol//jar",
        "@org_apache_htrace_htrace_core//jar",
        "@org_apache_zookeeper_zookeeper//jar",
        "@org_codehaus_jackson_jackson_mapper_asl//jar",
        "@org_hamcrest_hamcrest_core//jar",
        "@org_jruby_jcodings_jcodings//jar",
        "@org_jruby_joni_joni//jar",
        "@org_mortbay_jetty_jetty_util//jar",
        "@org_slf4j_slf4j_api//jar",
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
    name = "org_slf4j_slf4j_api",
    visibility = ["//visibility:public"],
    exports = [
        "@org_slf4j_slf4j_api//jar",
    ],
)

java_library(
    name = "org_apache_jena_jena_arq",
    visibility = ["//visibility:public"],
    exports = [
        "@org_apache_jena_jena_arq//jar",
        "@com_fasterxml_jackson_core_jackson_annotations//jar",
        "@com_fasterxml_jackson_core_jackson_core//jar",
        "@com_fasterxml_jackson_core_jackson_databind//jar",
        "@com_github_andrewoma_dexx_collection//jar",
        "@com_github_jsonld_java_jsonld_java//jar",
        "@commons_cli_commons_cli//jar",
        "@commons_io_commons_io//jar",
        "@org_apache_commons_commons_csv//jar",
        "@org_apache_commons_commons_lang3//jar",
        "@org_apache_httpcomponents_httpclient//jar",
        "@org_apache_httpcomponents_httpclient_cache//jar",
        "@org_apache_jena_jena_base//jar",
        "@org_apache_jena_jena_core//jar",
        "@org_apache_jena_jena_iri//jar",
        "@org_apache_jena_jena_shaded_guava//jar",
        "@org_apache_thrift_libthrift//jar",
        "@org_slf4j_jcl_over_slf4j//jar",
        "@org_slf4j_slf4j_api//jar",
        "@xerces_xercesImpl//jar",
    ],
)

java_library(
    name = "org_apache_jena_jena_iri",
    visibility = ["//visibility:public"],
    exports = [
        "@org_apache_jena_jena_iri//jar",
        "@org_slf4j_slf4j_api//jar",
    ],
)

java_library(
    name = "org_apache_htrace_htrace_core",
    visibility = ["//visibility:public"],
    exports = [
        "@org_apache_htrace_htrace_core//jar",
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
    name = "org_slf4j_jcl_over_slf4j",
    visibility = ["//visibility:public"],
    exports = [
        "@org_slf4j_jcl_over_slf4j//jar",
        "@org_slf4j_slf4j_api//jar",
    ],
)

java_library(
    name = "com_fasterxml_jackson_core_jackson_annotations",
    visibility = ["//visibility:public"],
    exports = [
        "@com_fasterxml_jackson_core_jackson_annotations//jar",
    ],
)

java_library(
    name = "org_apache_httpcomponents_httpclient",
    visibility = ["//visibility:public"],
    exports = [
        "@org_apache_httpcomponents_httpclient//jar",
        "@commons_codec_commons_codec//jar",
        "@commons_logging_commons_logging//jar",
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
    name = "org_apache_httpcomponents_httpclient_cache",
    visibility = ["//visibility:public"],
    exports = [
        "@org_apache_httpcomponents_httpclient_cache//jar",
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
    name = "io_netty_netty_all",
    visibility = ["//visibility:public"],
    exports = [
        "@io_netty_netty_all//jar",
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

java_library(
    name = "com_google_code_findbugs_jsr305",
    visibility = ["//visibility:public"],
    exports = [
        "@com_google_code_findbugs_jsr305//jar",
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
    name = "org_apache_jena_jena_core",
    visibility = ["//visibility:public"],
    exports = [
        "@org_apache_jena_jena_core//jar",
        "@com_github_andrewoma_dexx_collection//jar",
        "@commons_cli_commons_cli//jar",
        "@org_apache_commons_commons_csv//jar",
        "@org_apache_commons_commons_lang3//jar",
        "@org_apache_jena_jena_base//jar",
        "@org_apache_jena_jena_iri//jar",
        "@org_apache_jena_jena_shaded_guava//jar",
        "@org_slf4j_slf4j_api//jar",
        "@xerces_xercesImpl//jar",
    ],
)

java_library(
    name = "com_github_stephenc_findbugs_findbugs_annotations",
    visibility = ["//visibility:public"],
    exports = [
        "@com_github_stephenc_findbugs_findbugs_annotations//jar",
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
    name = "javax_xml_parsers_jaxp_api",
    visibility = ["//visibility:public"],
    exports = [
        "@javax_xml_parsers_jaxp_api//jar",
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
        "@javax_xml_bind_jaxb_api//jar",
        "@joda_time_joda_time//jar",
        "@org_slf4j_slf4j_api//jar",
        "@xalan_xalan//jar",
        "@xerces_xercesImpl//jar",
        "@xml_apis_xml_apis//jar",
    ],
)

java_library(
    name = "org_apache_commons_commons_csv",
    visibility = ["//visibility:public"],
    exports = [
        "@org_apache_commons_commons_csv//jar",
    ],
)

java_library(
    name = "org_apache_hbase_hbase_annotations",
    visibility = ["//visibility:public"],
    exports = [
        "@org_apache_hbase_hbase_annotations//jar",
        "@com_github_stephenc_findbugs_findbugs_annotations//jar",
        "@junit_junit//jar",
        "@log4j_log4j//jar",
        "@org_hamcrest_hamcrest_core//jar",
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
    name = "org_hamcrest_hamcrest_core",
    visibility = ["//visibility:public"],
    exports = [
        "@org_hamcrest_hamcrest_core//jar",
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
    name = "javax_inject_javax_inject",
    visibility = ["//visibility:public"],
    exports = [
        "@javax_inject_javax_inject//jar",
    ],
)

java_library(
    name = "com_github_andrewoma_dexx_collection",
    visibility = ["//visibility:public"],
    exports = [
        "@com_github_andrewoma_dexx_collection//jar",
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
    name = "org_apache_hbase_hbase_server",
    visibility = ["//visibility:public"],
    exports = [
        "@org_apache_hbase_hbase_server//jar",
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
    name = "javax_servlet_servlet_api",
    visibility = ["//visibility:public"],
    exports = [
        "@javax_servlet_servlet_api//jar",
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
    name = "org_apache_thrift_libthrift",
    visibility = ["//visibility:public"],
    exports = [
        "@org_apache_thrift_libthrift//jar",
        "@org_apache_httpcomponents_httpclient//jar",
        "@org_slf4j_slf4j_api//jar",
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
    name = "org_apache_jena_jena_base",
    visibility = ["//visibility:public"],
    exports = [
        "@org_apache_jena_jena_base//jar",
        "@com_github_andrewoma_dexx_collection//jar",
        "@org_apache_commons_commons_csv//jar",
        "@org_apache_commons_commons_lang3//jar",
        "@org_apache_jena_jena_shaded_guava//jar",
        "@org_slf4j_slf4j_api//jar",
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
    name = "junit_junit",
    visibility = ["//visibility:public"],
    exports = [
        "@junit_junit//jar",
        "@org_hamcrest_hamcrest_core//jar",
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
    name = "org_jruby_joni_joni",
    visibility = ["//visibility:public"],
    exports = [
        "@org_jruby_joni_joni//jar",
        "@org_jruby_jcodings_jcodings//jar",
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
    name = "org_json_json",
    visibility = ["//visibility:public"],
    exports = [
        "@org_json_json//jar",
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
    name = "org_apache_commons_commons_lang3",
    visibility = ["//visibility:public"],
    exports = [
        "@org_apache_commons_commons_lang3//jar",
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
    name = "org_apache_jena_jena_tdb",
    visibility = ["//visibility:public"],
    exports = [
        "@org_apache_jena_jena_tdb//jar",
        "@com_fasterxml_jackson_core_jackson_annotations//jar",
        "@com_fasterxml_jackson_core_jackson_core//jar",
        "@com_fasterxml_jackson_core_jackson_databind//jar",
        "@com_github_andrewoma_dexx_collection//jar",
        "@com_github_jsonld_java_jsonld_java//jar",
        "@commons_cli_commons_cli//jar",
        "@commons_io_commons_io//jar",
        "@org_apache_commons_commons_csv//jar",
        "@org_apache_commons_commons_lang3//jar",
        "@org_apache_httpcomponents_httpclient//jar",
        "@org_apache_httpcomponents_httpclient_cache//jar",
        "@org_apache_jena_jena_arq//jar",
        "@org_apache_jena_jena_base//jar",
        "@org_apache_jena_jena_core//jar",
        "@org_apache_jena_jena_iri//jar",
        "@org_apache_jena_jena_shaded_guava//jar",
        "@org_apache_thrift_libthrift//jar",
        "@org_slf4j_jcl_over_slf4j//jar",
        "@org_slf4j_slf4j_api//jar",
        "@xerces_xercesImpl//jar",
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
    name = "org_apache_jena_jena_shaded_guava",
    visibility = ["//visibility:public"],
    exports = [
        "@org_apache_jena_jena_shaded_guava//jar",
        "@org_slf4j_slf4j_api//jar",
    ],
)

