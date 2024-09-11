Deploying

Ensure you have the Azure CLI installed

```
brew install azure-cli
```

This project and files were generated with:
```
pulumi new azure-python
```

Login to Azure via the CLI:
```
az login
```

Deploy:
```
pulumi up
```

To clean up deployed resources:
```
pulumi destroy
```
