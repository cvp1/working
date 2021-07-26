import boto3

# Get the service resource.
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('devices')

response = table.get_item(
    Key={
        'SerialNumber': '1234567890',
        'DeviceName': 'P01002965'
    }
)
item = response['Item']
print(item)