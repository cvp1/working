import boto3

# Get the service resource.
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('devices')
table.put_item(
   Item={
        'SerialNumber': '1234567890',
        'DeviceName': 'P01002965',
        'MacAddress': '84:4e:6f:75:43:01',
        'Store': 25,
        'Location': 'Shoe Dept',
    }
)