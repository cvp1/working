import requests
import boto3
import json
import base64
import logging

#Logs for script based execution
logging.basicConfig(filename = 'aws_session.log', level=logging.INFO, format = '%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')



# Get personal gitlab API key from local file. Add this file to .gitignore.
def creds():
    with open('api_key.txt') as f:
        api_key = f.readline()
        return api_key

# Use personal key to fetch NIU vars from gitlab. This will ensure we catch 50 day rotations. We'll change this to use vault creds later.
def get_keys():
    # assigning the output of creds to the authk variable (personal gitlab token)
    authk = creds().strip()
    # get the NIU App ID from the gitlab API
    url1 = 'https://gitlab.nordstrom.com/api/v4/groups/10006/variables/NIU_App_ID'
    # get the NIU App Secret from the gitlab API
    url2 = 'https://gitlab.nordstrom.com/api/v4/groups/10006/variables/NIU_App_Secret'
    # Define the headers to post including the gitlab auth token (authk)
    headers = {"PRIVATE-TOKEN": authk, "Content-Type": "application/json"}
    # Execute the first request and assign it to r
    r = requests.get(url1, headers=headers)
    # Execute the second request and assign it to r2
    r2 = requests.get(url2, headers=headers)
    # Convert the request r to json and decode it - assign it to n1
    n1 = json.loads(r.content.decode())
    # Convert the request r2 to json and decode it - assign it to n2
    n2 = json.loads(r2.content.decode())
    # get the NIU Username and Secret values from both JSON files - concatenate them into token
    # format appid:appsecret
    m = n1['value'] + ":" + n2['value']
    # Encode the formatted token and return the encoded token as auth_key
    m_bytes = m.encode('ascii')
    base64_bytes = base64.b64encode(m_bytes)
    auth_key = base64_bytes.decode('ascii')
    return auth_key

# Use NAuth key to fetch AWS token for the below IAM role from Nauth/awstoken endpoint.
def get_token():
        # Call get_keys as get out encoded NIU token and assign it to auth
        auth = get_keys()
        # Assign the AWS awstoken endpoint to url
        url = 'https://8sor1yide2.execute-api.us-west-2.amazonaws.com/prod/nauth/niu/awstoken'
        # Define our payload that specifies what account and IAM role to fetch the token for and passing it to payload
        payload = """
        {
            "iamRole": "arn:aws:iam::725244813466:role/POSDS3"
        }
        """
        # Define our headers to pass including the NIU token (auth) to autenticate with
        headers = {"Authorization": auth, "Cache-Control": "no-cache", "Content-Type": "application/json"}
        # Fetch our AWS token with S3 read privileges for the above account from the AWS endpoint and assign it to r
        r = requests.post(url, data=payload, headers=headers)
        # Load the response as json and decode from bytes
        nauth = json.loads(r.content.decode())
        # Return our AWS token as nauth
        return nauth

# Set up the AWS session
# Parse AWS session token and define session. Change service_name to desired type (EC2, S3 ,etc).
# Service_name must match policies attached to IAM role.
# Use from aws_session import session to call this function (like s3_ops)

def session():
    # call get token to get us a fresh AWS token for the above account with S3 read perms
    # and return it as auth2
    auth2 = get_token()
    # Create the AWS session object and pass the relevent Access / Secret / Session keys retrieved in auth2
    s3 = boto3.client(
        service_name='s3',
        region_name='us-east-2',
        aws_access_key_id=auth2['AccessKeyId'],
        aws_secret_access_key=auth2['SecretAccessKey'],
        aws_session_token=auth2['SessionToken']
    )
    # Return the AWS session object to be used below to read S3 buckets as s3
    return s3