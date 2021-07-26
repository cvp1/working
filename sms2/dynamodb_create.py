import boto3

# Get the service resource.
dynamodb = boto3.resource('dynamodb')

# Create the DynamoDB table.
table = dynamodb.create_table(
    TableName='devices',
    KeySchema=[
        {
            'AttributeName': 'SerialNumber',
            'KeyType': 'HASH'
        },
        {
            'AttributeName': 'DeviceName',
            'KeyType': 'RANGE'
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'SerialNumber',
            'AttributeType': 'S'
        },
        {
            'AttributeName': 'DeviceName',
            'AttributeType': 'S'
        },
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    }
)

# Wait until the table exists.
table.meta.client.get_waiter('table_exists').wait(TableName='devices')

# Print out some data about the table.
print(table.item_count)