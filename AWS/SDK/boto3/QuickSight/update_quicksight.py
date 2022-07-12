import boto3
import random, string

client = boto3.client('quicksight')
Id = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(20))

response = client.create_ingestion(
    DataSetId='<dataset id>',
    IngestionId=Id,
    AwsAccountId='<aws account id>',
    IngestionType='INCREMENTAL_REFRESH'|'FULL_REFRESH'
)