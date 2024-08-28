Example Pulumi code that pulls Docker images and runs them locally. This is from the [Pulumi Fundamentals](https://www.pulumi.com/tutorials/pulumi-fundamentals/) tutorial with some slight modifications.

## Running

Set up a new Pulumi project:

```
pulumi new python -y
```

Activate the Python virtual environment:

```
source venv/bin/activate
```

Install dependencies:

```
pip3 install pulumi_docker
```

Run Pulumi:

```
pulumi up
```

This will download the images and output an IP address you can copy and paste into your browser to access the demo site.

## Cleaning Up

```
pulumi destroy
```
