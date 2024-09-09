terraform {
  required_providers {
    docker = {
      source = "kreuzwerker/docker"
      version = "~> 2.13.0"
    }
  }
}

provider "docker" {}

resource "docker_image" "backend" {
  name         = "pulumi/tutorial-pulumi-fundamentals-backend:latest"
  keep_locally = false
}

resource "docker_image" "frontend" {
  name         = "pulumi/tutorial-pulumi-fundamentals-frontend:latest"
  keep_locally = false
}

resource "docker_image" "mongo" {
  name         = "pulumi/tutorial-pulumi-fundamentals-database:latest"
  keep_locally = false
}

resource "docker_network" "network" {
  name = "services-dev"
}

resource "docker_container" "mongo-container" {
  image = docker_image.mongo.latest
  name  = "mongo-dev"
  ports {
    internal = 27017
    external = 27017
  }
  networks_advanced {
    name = "services-dev"
    aliases = ["mongo"]
  }
}

resource "docker_container" "backend-container" {
  image = docker_image.backend.latest
  name  = "backend-dev"
  env   = [
    "DATABASE_HOST=mongodb://mongo:27017",
    "DATABASE_NAME=cart"
  ]
  ports {
    internal = 3000
    external = 3000
  }
  networks_advanced {
    name = "services-dev"
    aliases = ["backend-dev"]
  }
}

resource "docker_container" "frontend-container" {
  image = docker_image.frontend.latest
  name  = "frontend-dev"
  env   = [
    "LISTEN_PORT=3001",
    "HTTP_PROXY=backend-dev:3000",
    "PROXY_PROTOCOL=http://"
  ]
  ports {
    internal = 3001
    external = 3001
  }
  networks_advanced {
    name = "services-dev"
    aliases = ["frontend-dev"]
  }
}
