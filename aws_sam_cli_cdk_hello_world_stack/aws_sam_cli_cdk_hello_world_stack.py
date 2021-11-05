from aws_cdk import core as cdk

# For consistency with other languages, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from aws_cdk import (
    aws_lambda as _lambda,
    aws_apigateway as _apigateway,
    aws_lambda_event_sources as _lambda_event_sources,
    core
)


class AwsSamCliCdkHelloWorldStack(core.Stack):
    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.lambda_event = _lambda_event_sources.ApiEventSource(
            method="get",
            path="/hello"
        )

        cdk_lambda = _lambda.DockerImageFunction(
            self,
            "helloworld",
            description="poc rest api",
            timeout=cdk.Duration.minutes(2),                
            code=_lambda.DockerImageCode.from_image_asset('./hello_world'),
            #role=hello_world_service_role,
            #security_groups=[helloworld_security_group],
            #vpc=vpc,
            #vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE), 
            events=[self.lambda_event]

        )        

        cdk_lambda2 = _lambda.Function(
            scope=self,
            id="cdk-hello-world-lambda",
            runtime=_lambda.Runtime.PYTHON_3_8,
            function_name="cdk-hello-world-lambda-function",
            description="Lambda function deployed using AWS CDK Python",
            code=_lambda.Code.from_asset("./hello_world"),
            handler="app.lambda_handler",
            events=[self.lambda_event]
        )

        api = _apigateway.LambdaRestApi(
            scope=self,
            id="cdk-hello-world-rest-api",
            handler=cdk_lambda,
            proxy=False
        )

        hello_world = api.root.add_resource("hello")
        hello_world.add_method('GET')

