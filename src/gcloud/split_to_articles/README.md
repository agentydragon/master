Component to split a Wiki XML tarball into individual articles.
The articles are stored in the wiki-articles Cloud Bigtable.

Demo:

```
bazel run --jvmopt='-Dbigtable.projectID=extended-atrium-198523 -Dbigtable.instanceID=wiki-articles' :demo
```

To push:

```
bazel run :push_split_to_articles
```

To run:

```
kubectl create -f split_to_articles.yaml
```

TODO: Could I speed this up by maybe using sharded XML dumps? Or maybe by
bundling the mutations?
