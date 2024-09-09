"""A Python Pulumi program"""

import pulumi
import pulumi_docker as docker

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
    opts = pulumi.ResourceOptions(import_="b68bc69b9ed5034779bbf6f955e5c5c09615024282926146ccf3f322b51592aa")) # frontend container ID
