Component to fetch a Wikipedia image and upload it to a Cloud Storage bucket.

What used to work locally
====

virtualenv env
. env/bin/activate
pip install -r requirements.txt

python main.py

--> it will upload the file :)

Trying to get this to work remotely/containerizedly
====

To deploy the image to the image registry, run:

```
bazel run :push_upload_to_storage
```

To then start the upload job, run:

```
kubectl create -f upload_to_storage.yaml
```

To inspect the job's status, run:

```
kubectl describe jobs/upload-to-storage
```

If you want to re-run the job, delete it first:

```
kubectl delete jobs/upload-to-storage
```
