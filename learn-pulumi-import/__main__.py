"""A Python Pulumi program"""

import pulumi
import pulumi_docker as docker

# this was imported via CLI
frontend_dev = docker.Container("frontend-dev",
    command=[
        "npm",
        "start",
    ],
    entrypoints=["docker-entrypoint.sh"],
    hostname="b68bc69b9ed5",
    image="sha256:2402f5905b7d36f22350df7c61b1f7ea948a9dac543c40bb75fbfd577efdd3ad",
    ipc_mode="private",
    log_driver="json-file",
    name="frontend-dev",
    network_mode="bridge",
    ports=[{
        "external": 3001,
        "internal": 3001,
    }],
    runtime="runc",
    shm_size=64,
    working_dir="/usr/src/app",
    opts = pulumi.ResourceOptions(protect=True))

# bulk imported via resources.json
backend_dev = docker.Container("backend-dev",
    command=[
        "npm",
        "start",
    ],
    entrypoints=["docker-entrypoint.sh"],
    hostname="a964bd431b69",
    image="sha256:3cc3e17d6899ef1ac27c1f376861f0783cf5f032c4359f5146206f0db52aef0b",
    ipc_mode="private",
    log_driver="json-file",
    name="backend-dev",
    network_mode="bridge",
    ports=[{
        "external": 3000,
        "internal": 3000,
    }],
    runtime="runc",
    shm_size=64,
    working_dir="/usr/src/app",
    opts = pulumi.ResourceOptions(protect=True))
mongo_dev = docker.Container("mongo-dev",
    command=["mongod"],
    entrypoints=["docker-entrypoint.sh"],
    healthcheck={
        "tests": [
            "CMD",
            "/usr/local/bin/docker-healthcheck.sh",
        ],
    },
    hostname="d9ca0729fc93",
    image="sha256:5f95d80bde8c46a51d731076ba833a621421c061981ec800a6735c604abe9a78",
    ipc_mode="private",
    log_driver="json-file",
    name="mongo-dev",
    network_mode="bridge",
    ports=[{
        "external": 27017,
        "internal": 27017,
    }],
    runtime="runc",
    shm_size=64,
    opts = pulumi.ResourceOptions(protect=True))
