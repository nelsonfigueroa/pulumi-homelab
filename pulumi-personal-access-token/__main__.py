import pulumi
import pulumi_pulumiservice as pulumiservice

token_1 = pulumiservice.AccessToken(
    resource_name="token_1",
    description="personal access token created via IaC",
)

token_2 = pulumiservice.AccessToken(
    resource_name="token_2",
    description="personal access token created via IaC",
)

# The value isn't printed out to stdout
# The value is hidden in Pulumi cloud
pulumi.export("access_token_1", token_1.value)
pulumi.export("access_token_2", token_2.value)

# You can still view them in the CLI using
# pulumi stack output --show-secrets

# docs: https://www.pulumi.com/registry/packages/pulumiservice/api-docs/accesstoken/
# reference for pulumi stack output --show-secrets: https://www.pulumi.com/docs/iac/cli/commands/pulumi_stack_output/

# there doesn't seem to be a way to specify an expiration for the token through code.