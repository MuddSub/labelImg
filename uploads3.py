# MUST INSTALL boto3 IN YOUR VIRTUAL ENVIRONMENT
import boto3
import os
from botocore import UNSIGNED
from botocore.client import Config

BUCKET_NAME = 'halu-test-bucket'

# client = boto3.client('s3',
#                       aws_access_key_id=ACCESS_KEY,
#                       aws_secret_access_key=SECRET_ACCESS_KEY)

client = boto3.client('s3', config=Config(signature_version=UNSIGNED))

#upload this file to s3 bucket
upath = 'uploads3.py'
ukey = 'randomfolder/' + upath
client.upload_file(upath, BUCKET_NAME, ukey)
print('done uploading')

#download random fish image to computer
dkey = 'image-data/Abactochromis_labrosus_0003.jpg'
dpath = 'Abactochromis_labrosus_0003.jpg'
client.download_file(BUCKET_NAME, dkey, dpath)
print('done downloading')

#get a presigned url so that we can view the image without having to download it
response = client.generate_presigned_url('get_object',
                                         Params={
                                             'Bucket': BUCKET_NAME,
                                             'Key': dkey
                                         },
                                         ExpiresIn=3600)

print(response)  # should be url string

# ftr the 'response' string is the same as
fileurl = 'https://' + BUCKET_NAME + '.s3.amazonaws.com/' + dkey
assert (response == fileurl)
