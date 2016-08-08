def parse_proto_file(proto, path):
    message = proto()
    with open(path, 'rb') as f:
        message.ParseFromString(f.read())
    return message
