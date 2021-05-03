# upload from s3 to VB using pre-signed URLs
# creates presigned URL using s3 key
# requires a csv list of files to be uploaded with filename and s3 key
# -*- coding: utf-8 -*-

import csv
import json
import os
import boto3
import boto3.session
from botocore.client import Config
from VoiceBaseClient import VoiceBaseClient

AWS_SERVER_PUBLIC_KEY = ''
AWS_SERVER_SECRET_KEY = ''

vb_bearer_token = '**VoiceBase_Token_Here**'

s3 = boto3.client('s3', aws_access_key_id=AWS_SERVER_PUBLIC_KEY,
					 aws_secret_access_key=AWS_SERVER_SECRET_KEY,
					 region_name='', config=Config(signature_version='s3v4'))

client = VoiceBaseClient(token = vb_bearer_token)
media = client.media()

# include all desired features, example below:
def generate_configuration():

  return json.dumps({
  
   "speechModel": {
   "model":"Titan"
  }
} )

 
counter = 0

with open('list.csv', 'r') as list_file:
	list_reader = csv.DictReader(list_file, delimiter = ',')
	
	with open('res.csv', 'a') as results_file:
	
		results_writer = csv.writer(
			results_file, delimiter = ',', quotechar = '"'
		)
		results_writer.writerow(['key', 'filename','mediaId','status'])
		for row in list_reader:
			key = row['s3key']
			filename = row['filename']
			
			fileURL = s3.generate_presigned_url(
			ClientMethod='get_object',
			Params={
	
			'Bucket': 'bucketname',
			'Key': key
			},
			ExpiresIn=604800
			)
		
			counter = counter + 1
			md = {
 			"externalId": filename,
 			"extended": {
  			 "uploadversion": "1"
  			  
 			}
			} 
			m_data = json.dumps(md)
			response = media.postUrl(
				fileURL,None, None,configuration = generate_configuration(), metadata = m_data
				)
			
			if response['status'] !='accepted':

				media_id = 0
				status = 'error'
			else: 
				media_id = response['mediaId']
				status = response['status']
			results_writer.writerow([key, filename,media_id, status])


      