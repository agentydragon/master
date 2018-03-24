from googleapiclient.discovery

client = googleapiclient.discovery.build('storagetransfer', 'v1')
transfer_job = {
    'description': 'download wiki dump',
    'status': 'ENABLED',
    'projectId': 'extended-atrium-198523',
    'transferSpec': {
        'httpDataSource': {
        },
        'gcsDataSink': {
            'bucketName': 'agentydragon-master'
        }
    }
}
client.transferJobs().create(body=transfer_job)
