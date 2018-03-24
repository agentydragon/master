Component to split a Wiki XML tarball into individual articles.
The articles are stored in the wiki-articles Cloud Bigtable.

Demo:

```
bazel run --jvmopt='-Dbigtable.projectID=extended-atrium-198523 -Dbigtable.instanceID=wiki-articles' :demo
```
