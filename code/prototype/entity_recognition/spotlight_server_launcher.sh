#!/bin/bash
module add jdk-8
export JAVABIN=/packages/run/jdk-8/current/bin/java
prototype/entity_recognition/spotlight_server $*
