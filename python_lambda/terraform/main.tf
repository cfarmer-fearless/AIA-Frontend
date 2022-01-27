resource "null_resource" "create_image" {
  triggers = {
    always_run = "${timestamp()}"
  }
  provisioner "local-exec" {
    working_dir = "../"
    command = "docker build -t ${local.docker_build_tag} ."
  }
}


module "dev" {
  source = "./modules"

  environment        = "dev"
  project            = var.project
  docker_build_tag   = local.docker_build_tag

  depends_on = [null_resource.create_image]
}

module "prod" {
  source = "./modules"
  count = var.create_prod_infrastructure ? 1 : 0

  environment        = "prod"
  project            = var.project
  docker_build_tag   = local.docker_build_tag

  depends_on = [null_resource.create_image]
}
