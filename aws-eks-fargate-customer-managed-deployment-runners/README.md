A repo to test out customer-managed agents on EKS with Fargate. Not officially supported by Pulumi at this time (2024-11-01) but it should work in theory. Still a work in progress with some issues...

More info: https://www.pulumi.com/blog/customer-managed-agents-kubernetes/

## Deploying

Clone this repo and navigate to this directory.

Run:

```
python3 -m venv venv
```

Then run:

```
source venv/bin/activate
```

Install dependencies:

```
pip install -r requirements.txt
```

Then deploy with Pulumi:
```
pulumi up
```