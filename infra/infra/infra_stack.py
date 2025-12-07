from pathlib import Path

from aws_cdk import (
    Duration,
    RemovalPolicy,
    Stack,
    aws_dynamodb as dynamodb,
    aws_events as events,
    aws_events_targets as targets,
    aws_lambda as _lambda,
    aws_s3 as s3,
    aws_stepfunctions as sfn,
    aws_stepfunctions_tasks as tasks,
)
from constructs import Construct


class InfraStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        project_root = Path(__file__).resolve().parent.parent
        lambda_src = project_root / "lambda_src" / "processor"

        ingest_bucket = s3.Bucket(
            self,
            "ExpenseIngestBucket",
            encryption=s3.BucketEncryption.S3_MANAGED,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
        )

        expense_table = dynamodb.Table(
            self,
            "ExpenseRecords",
            partition_key=dynamodb.Attribute(
                name="pk",
                type=dynamodb.AttributeType.STRING,
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.DESTROY,
        )

        processor_fn = _lambda.Function(
            self,
            "ExpenseProcessorFn",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="index.handler",
            code=_lambda.Code.from_asset(str(lambda_src)),
            timeout=Duration.seconds(30),
            environment={
                "TABLE_NAME": expense_table.table_name,
                "INGEST_BUCKET": ingest_bucket.bucket_name,
            },
        )
        ingest_bucket.grant_read(processor_fn)
        expense_table.grant_write_data(processor_fn)

        textract_step = sfn.Pass(
            self,
            "RunTextractStub",
            result=sfn.Result.from_object({"message": "Textract placeholder"}),
            comment="Replace with actual Textract task",
        )

        comprehend_step = sfn.Pass(
            self,
            "ScanPIIStub",
            result=sfn.Result.from_object({"message": "Comprehend placeholder"}),
            comment="Replace with actual Comprehend task",
        )

        fraud_step = tasks.LambdaInvoke(
            self,
            "FraudAndPersist",
            lambda_function=processor_fn,
            payload=sfn.TaskInput.from_object(
                {
                    "bucket": sfn.JsonPath.string_at("$.bucket.name"),
                    "key": sfn.JsonPath.string_at("$.object.key"),
                }
            ),
            comment="Stub fraud logic and DynamoDB write",
        )

        definition = textract_step.next(comprehend_step).next(fraud_step)

        state_machine = sfn.StateMachine(
            self,
            "ExpensePipelineStateMachine",
            definition=definition,
            timeout=Duration.minutes(5),
        )

        s3_event_rule = events.Rule(
            self,
            "IngestObjectCreatedRule",
            event_pattern=events.EventPattern(
                source=["aws.s3"],
                detail_type=["Object Created"],
                detail={"bucket": {"name": [ingest_bucket.bucket_name]}},
            ),
            description="Kick off the workflow when a receipt lands in S3",
        )
        s3_event_rule.add_target(
            targets.SfnStateMachine(
                state_machine,
                input=targets.RuleTargetInput.from_event_path("$.detail"),
            )
        )
