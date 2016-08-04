all: sentence_pb2.py training_samples_pb2.py

sentence_pb2.py: sentence.proto
	protoc -I=. --python_out=. sentence.proto

training_samples_pb2.py: training_samples.proto
	protoc -I=. --python_out=. training_samples.proto
