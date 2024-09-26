A simple Pulumi program in Python that demonstrates multi-cloud deployments of storage buckets.

To try this out yourself do the following (assuming you already have AWS and GCP access configured):

Create a python virtual environment:

```
python3 -m venv venv
```

Use the virtual environment:

```
source venv/bin/activate
```

Install dependencies:

```
pip3 install -r requirements.txt
```

Deploy:

```
pulumi up
```

From this point forward you can continue defining infrastructure in `__main__.py`