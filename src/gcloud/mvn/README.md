mvn exec:exec -DLocalSplitAndPlaintextConversion -Dexec.args="-Dinput_file=[...].bz2"

To run CoreNLP on articles:

```
mvn package exec:exec -DCoreNLPOnArticles
```

To run wikitext-to-plaintext translation

```
mvn package exec:exec -DWikitextToPlaintext
```
