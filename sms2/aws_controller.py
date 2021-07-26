import boto3

dc = boto3.client('dynamodb', region_name='us-west-2')

def get_items():
    return dc.scan(
        TableName='devices'
    )