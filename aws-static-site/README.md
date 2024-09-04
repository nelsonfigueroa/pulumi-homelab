# aws-static-site

A simple static site that can be deployed on AWS using S3 and CloudFront.

## Deployment

Deployment assumes you have the AWS CLI configured and the Pulumi CLI installed.

Clone this repo

Browse to the `aws-static-site` directory

Install Python dependencies:

```
pip3 install -r requirements.txt
```

Use Pulumi locally (no cloud backend):

```
pulumi login --local
```

Create a new Pulumi stack called `dev`

```
pulumi stack init dev
```

Configure the AWS region if needed

```
pulumi config set aws:region us-west-2
```

Then deploy

```
pulumi up
```

The CLI will output a CloudFront URL where you can see the deployed site.

## Cleaning Up

```
pulumi destroy
```

Then remove the Pulumi stack locally

```
pulumi stack rm dev
```
