import subprocess
# Start the Docker container.
# Load into local Docker client.
print subprocess.check_output('src/gcloud/corenlp_image')
image_path = './src/gcloud/corenlp_image'
docker_process = subprocess.Popen([
    '/usr/bin/docker', 'run', image_path, '--publish', '127.0.0.1:9000:9000/tcp'
])
# Try connecting to it on port 9000.
