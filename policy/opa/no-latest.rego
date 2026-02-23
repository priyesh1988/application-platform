package platform.policy

deny[msg] {
  input.environment == "prod"
  endswith(input.config.image, ":latest")
  msg := "prod deployments must not use :latest"
}
