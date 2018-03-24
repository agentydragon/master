# Everything that builds has to continue building.
bazel build \
  //src/gcloud/upload_to_storage:upload_to_storage_py \
  //src/gcloud/upload_to_storage:upload_to_storage \
  //src/gcloud/upload_to_storage:push_upload_to_storage \
  //src/gcloud/upload_to_storage:create_single_file_bin \
  //src/gcloud/upload_to_storage:create_single_file_py \
  //src/gcloud/upload_to_storage:create_single_file \
  //src/gcloud/upload_to_storage:push_create_single_file \
  //src/gcloud/split_to_articles:demo \
  //src/gcloud/split_to_articles:split_to_articles \
  //src/gcloud/split_to_articles:push_split_to_articles \
  //src/gcloud/wikitext_to_plaintext:wikitext_to_plaintext
