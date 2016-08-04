all: sentence_pb2.py

sentence_pb2.py: sentence.proto
	protoc -I=. --python_out=. sentence.proto
