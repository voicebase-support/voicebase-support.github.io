# S3 Callbacks

VoiceBase is able to return the results of your requests into your Amazon S3 bucket
without you having to provide AWS credentials to VoiceBase. This is achieved
by providing a pre-signed URL in the callback configuration when you submit the
media for processing to us.



## How to generate a pre-signed URL with Python using Boto3

The following code shows how to generate a pre-signed URL using boto3 as the AWS client library.
Note that the "method" must be set to "PUT".

You you must provide a Content-Type header with a value that matches the content type of the results
to be received. Refer to [callback] documentation. (callbacks.html)

You must provide ample time between the time you create the
pre-signed URL and the expected time your processing request to VoiceBase will complete.  The
sample code expires the URL after 24 hours (86400 seconds).

_presigned.py_
```python
import boto3
import requests

# Get the service client.
session = boto3.Session(aws_access_key_id="XXX", aws_secret_access_key="XXX")
s3 = session.client('s3')

bucket = 'your-bucket-name'
objectName = 'desired/object/name/analytics.json'
mimeType = 'application/json'

# Generate the URL for a PUT of the 'desired-object-name' into 'your-bucket-name'
url = s3.generate_presigned_url(
    ClientMethod='put_object',
    Params={
        'Bucket': bucket,
        'Key': objectName,
        'ContentType' : mimeType
    },
    ExpiresIn=86400,
    HttpMethod='PUT'
   )
print url
```

Generate the presigned URL
```bash
python presigned.py
```

Use the pre-signed URL in the configuration when submitting media to the /v3 API. For example:

```json
{
  "publish": {
    "callbacks": [
      {
        "url" : "https://your-bucket-name.s3.amazonaws.com/desired/object/name/analytics.json?AWSAccessKeyId=AKIAJV3H7XSCGJXMUGGA&content-type=application%2Fjson&Expires=1499476130&Signature=UwcWOfLWLpvtj1LibHd0Na5Fw%2FM%3D",
        "type" : "analytics",
        "method" : "PUT",
        "include" : [ "transcript", "knowledge", "metadata", "prediction", "streams" ]
      }
    ]
  }
}
```
