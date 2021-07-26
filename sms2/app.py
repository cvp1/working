# Basic MetaData Store SMS v0.9
# https://hub.docker.com/repository/docker/cvande/sms
# https://github.com/cvp1/pyscripts/tree/master/app2

import boto3
import logging
import aws_controller
from flask import Flask
from flask import request
from flask import jsonify

app = Flask(__name__)

# Logs to console for container
logging.basicConfig(level=logging.INFO, format = '%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')


# Set the landing page
@app.route('/')
def lp():
  return 'SMS2 V.9'

# Tired of doing this manually so configure an endpoint to flush the Redis DB. This needs to be removed later
@app.route('/flushall')                            
def flushall():
    
    table = aws_controller.Table('devices')
    table.delete()
    return 'Table Deleted'

# Endpoint for formatted JSON files to load. Need to add token auth
@app.route('/load', methods=['GET', 'POST'])
def add_message():
    data = request.json
    table = aws_controller.Table('devices')
    table.put_item(
        Item={
            'SerialNumber': '1234567890',
            'DeviceName': 'P01002965',
            'MacAddress': '84:4e:6f:75:43:01',
            'Store': 25,
            'Location': 'Shoe Dept',
            }
        )
    return jsonify(data)

# Search by SerialNumber (key)
@app.route('/search/<string:serial>', methods=['GET', 'POST'])
def getr(serial, device):
    table = aws_controller.Table('devices')
    response = table.get_item(
    Key={
        'SerialNumber': serial,
        'DeviceName': device,
        }
    )
    item = response['Item']
    print(item)

# Search by attribute (value). This can get expensive as the data grows
#@app.route('/vsearch/<string:name>', methods=['GET', 'POST'])
#def get_values(name):
#    r = rcon()
#    cursor = '0'
#    vals = []
#    while cursor != 0:
#        cursor, values = r.scan(cursor=cursor)
##        values = r.mget(*values)
#       for val in values:
#           if name in val:
#                vals.append(val)
#        return jsonify(vals)

# Get a dump of all keys and values       
@app.route('/getall')
def getall():
    return jsonify(aws_controller.get_items())
#    return jsonify(data)    

# Application start
if __name__ == "__main__":
  app.run(host ='0.0.0.0', port=5001, debug=True)