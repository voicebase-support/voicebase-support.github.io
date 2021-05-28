# list.csv is a list of urls
# any extra metadata fields under 'extended' need to be indexed on the VB platform before upload

# command line example
#  python BatchUpload_URL.py --list test_sample_urls.csv --results ./res.csv --token  


import argparse
import csv
import json
import os


from VoiceBaseClient import VoiceBaseClient

# ********* def main ***********
def main():
  parser = argparse.ArgumentParser(
    description = "Batch URL uploader to VoiceBase V3"
  )
  parser.add_argument(
    '--list', 
    help = "path to csv list of URLs(one per line)", 
    required = True
  )
  parser.add_argument(
    '--results',
    help = "path to output csv file of files, media ids, and status",
    required = True
  )
  parser.add_argument(
    '--token',
    help = "Bearer token for V3 API authentication",
    required = True
  )


  args = parser.parse_args()

  upload(args.list, args.results, args.token)

# ********* def upload  ***********
def upload(list_path, results_path, token):

  client = VoiceBaseClient(token = token)
  media = client.media()

  counter = 0

  with open(list_path, 'r') as list_file:
    with open(results_path, 'w') as results_file:
      results_writer = csv.writer(
        results_file, delimiter = ',', quotechar = '"'
      )

      results_writer.writerow([ 'file', 'mediaId', 'status' ]) # write headers

      for recordingUrl in list_file:
        print recordingUrl
        filename = recordingUrl[89:]
 
        md = {
          "externalId": filename,
          # "extended": {
          #  "uploadversion": "1"
          # }
          } 
        meta_data = json.dumps(md)
        response = media.postUrl(
        recordingUrl, None,None,configuration = generate_configuration(), metadata = meta_data
          )
        print response
        media_id = response['mediaId']
        status = response['status']

        results_writer.writerow([ filename, media_id, status ])
        counter += 1
        print counter

# ********* def generate config json ***********
def generate_configuration():
  return json.dumps({
  
 "transcript": {
    "formatting" : {
      "enableNumberFormatting" : False
    }
  } 

})


if __name__ == "__main__":
  main()