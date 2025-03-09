import os

from aws_cdk import (
    Stack,
    aws_s3 as s3,
    aws_iam as iam,
    aws_cloudfront as cloudfront,
    aws_cloudfront_origins as origins,
    aws_s3_deployment as s3_deployment,
    aws_certificatemanager as acm,
    aws_route53 as route53,
    aws_route53_targets as targets, RemovalPolicy,
)
from constructs import Construct

class PortfolioIacStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        domain_name = os.environ.get("DOMAIN_NAME")
        hosted_zone = route53.HostedZone.from_lookup(self, "HostedZone", domain_name=domain_name)

        # SSL Certificate
        certificate = acm.DnsValidatedCertificate(
            self, "PortfolioCertificate",
            domain_name=domain_name,
            hosted_zone=hosted_zone,
            region="us-east-1"
        )

        # S3 Bucket
        bucket = s3.Bucket(
            self, "PortfolioBucket",
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            removal_policy=RemovalPolicy.DESTROY
        )

        # CloudFront Distribution
        distribution = cloudfront.Distribution(
            self, "PortfolioDistribution",
            default_root_object="index.html",
            domain_names=[domain_name],
            certificate=certificate,
            default_behavior=cloudfront.BehaviorOptions(
                origin=origins.S3Origin(bucket),
                viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS
            )
        )

        oai = cloudfront.OriginAccessIdentity(self, "PortfolioOAI")

        # Update bucket policy to allow CloudFront access
        bucket.add_to_resource_policy(
            iam.PolicyStatement(
                actions=["s3:GetObject"],
                resources=[bucket.arn_for_objects("portfolio_sergi/*")],
                principals=[iam.CanonicalUserPrincipal(oai.cloud_front_origin_access_identity_s3_canonical_user_id)]
            )
        )

        # Deploy files to S3
        s3_deployment.BucketDeployment(
            self, "DeployPortfolio",
            sources=[s3_deployment.Source.asset("portfolio_sergi")],
            destination_bucket=bucket,
            destination_key_prefix=""
        )

        # Route 53 Alias Record
        route53.ARecord(
            self, "CloudFrontAlias",
            zone=hosted_zone,
            target=route53.RecordTarget.from_alias(targets.CloudFrontTarget(distribution))
        )
