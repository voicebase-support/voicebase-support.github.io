#  batch json or txt file download
# for txt files, change line 77 to "api_results = media.get_item_txt(media_id)"
# and line 80 to "write_txtresult_to_output(output_path, filename, api_results)"

## example command line
# python Batchdownloadv3.py --outstanding ./outstanding.csv --results ./res.csv --output ./transcripts --token  ****token goes here****  



import argparse
import csv
import json
import os
import io


from VoiceBaseClient import VoiceBaseClient

def main():
	parser = argparse.ArgumentParser(
		description = 'Batch downloader to VoiceBase V3'
	)
	parser.add_argument(
		'--results', 
		help = 'path to download list, or upload result csv file of files, media ids, and status',
		required = True
	)
	parser.add_argument(
		'--outstanding',
		help = 'path to csv file of outstanding (not finished) files',
		# saving the portion of the list that is not yet ready
		required = True
	)
	parser.add_argument(
		'--output',
		help = 'path to directory to write outputs',
		required = True
	)
	parser.add_argument(
		'--token',
		help = 'Bearer token for V3 API authentication',
		required = True
	)


	args = parser.parse_args()

	download(
		args.results, 
		args.outstanding,
		args.output,
		args.token
	)

def download(results_path, outstanding_path, output_path, token):


	client = VoiceBaseClient(token = token)
	media = client.media()

	with open(results_path, 'r') as results_file:
		results_reader = csv.DictReader(results_file)

		
		with open(outstanding_path, 'w') as outstanding_file:
			outstanding_writer = csv.writer(
				outstanding_file, delimiter = ',', quotechar = '"'
			)
			outstanding_writer.writerow([ 'file', 'mediaId', 'status' ])
			
			for results_row in results_reader:
				filename = results_row['file']
				media_id = results_row['mediaId']
				original_status = results_row['status']

				api_results = media.get_item(media_id) 
				
				write_result_to_output(output_path, filename, api_results)
	

def write_result_to_output(output_path, filename, results):
	if not os.path.exists(output_path):
		os.mkdir(output_path)
	with io.open(os.path.join(output_path,  (os.path.splitext(os.path.basename(filename))[0] + '.json')), 'w', encoding = 'utf8') as output_file:
		output_file.write(json.dumps(results, ensure_ascii=False))

def write_txtresult_to_output(output_path, filename, results):
	if not os.path.exists(output_path):
		os.mkdir(output_path)
	with io.open(os.path.join(output_path,  (os.path.splitext(os.path.basename(filename))[0] + '.txt')), 'w', encoding='utf8') as output_file:

		output_file.write(results)  


if __name__ == "__main__":
	main()