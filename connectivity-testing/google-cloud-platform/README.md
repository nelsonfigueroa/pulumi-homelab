Deploying

Ensure you have the Google Cloud CLI installed

```
brew install --cask google-cloud-sdk
```

This project and files were generated with:
```
pulumi new gcp-python
```

Login to GCP via the CLI:
```
gcloud auth application-default login
```

Set a GCP project (This can be whatever you want)
```
pulumi config set gcp:project <my-project>
```

Deploy:
```
pulumi up
```

To clean up deployed resources:
```
pulumi destroy
```
