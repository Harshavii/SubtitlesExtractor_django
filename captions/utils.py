import boto3
from botocore.exceptions import NoCredentialsError
import os
from datetime import datetime
from dateutil.parser import parse as dateutil_parse
from botocore.exceptions import WaiterError
import time

s3 = boto3.client(
    's3',
    aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),  # Replace with your AWS access key
    aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),  # Replace with your AWS secret key
    region_name=os.environ.get('AWS_DEFAULT_REGION')  # Replace with your AWS region
)

# SETTING UP AWS S3 TO STORE VIDEO
def upload_to_s3(file_path, bucket_name, object_key):


    try:
        s3.upload_file(file_path, bucket_name, object_key)
        print(f"File uploaded to S3: {object_key}")
    except NoCredentialsError:
        print("Credentials not available or incorrect. Please check your AWS credentials.")
    except Exception as e:
        print(f"Error uploading file to S3: {e}")


# PARSING SRT FILE
from datetime import datetime

def parse_srt(file_path):
    subtitles = []
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        lines = file.readlines()
        i = 0
        while i < len(lines):
            # Skip empty lines
            if not lines[i].strip():
                i += 1
                continue

            # Check if there are enough lines left
            if i + 1 < len(lines):
                timestamp_line = lines[i + 1].strip()
                if " --> " in timestamp_line:
                    # Parse timestamp
                    start_time, end_time = timestamp_line.split(" --> ")

                    # Parse and format timestamp without date
                    start_time = start_time.replace(',', '.')
                    end_time = end_time.replace(',', '.')

                    # Parse text (handle multiline)
                    text_lines = []
                    i += 2

                    # Check if there are enough lines left
                    while i < len(lines) and lines[i].strip() != "":
                        text_lines.append(lines[i].strip())
                        i += 1

                    text = ' '.join(text_lines)

                    subtitle_data = {
                        'start_time': start_time,
                        'end_time': end_time,
                        'text': text
                    }
                    subtitles.append(subtitle_data)

                    # Move to the next subtitle
                    i += 2
                else:
                    # Move to the next line if no timestamp information found
                    i += 1
            else:
                # Move to the next line if no more lines available
                i += 1
    # print(subtitles)
    return subtitles



# STORING SUBTITLES IN DYNAMODB
def store_dynamodb(subtitles, video_filename):
    # Generate a unique table name using the video filename
    table_name = video_filename.split('.')[0]  # Use the video filename without extension

    # Initialize the DynamoDB client
    dynamodb = boto3.resource('dynamodb')

    # Check if the table already exists
    existing_tables = dynamodb.meta.client.list_tables()['TableNames']
    if table_name not in existing_tables:
        # Create a new DynamoDB table with the unique name
        table = dynamodb.create_table(
            TableName=table_name,
            KeySchema=[
                {'AttributeName': 'id', 'KeyType': 'HASH'},
            ],
            AttributeDefinitions=[
                {'AttributeName': 'id', 'AttributeType': 'S'},
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5,
            }
        )
        time.sleep(5)  # Adjust the sleep time as needed

        # Wait until the table exists before proceeding
        table.meta.client.get_waiter('table_exists').wait(TableName=table_name)

    # Get the DynamoDB table
    table = dynamodb.Table(table_name)

    # Create a unique identifier for the DynamoDB item (you can customize this based on your requirements)
    item_id = video_filename

    # print("Subtitles data:", subtitles)
    # for i, subtitle in enumerate(subtitles):
    #     print(f"Subtitle {i + 1}: {subtitle}")

    dynamodb_items = [
        {
            'id': f'{i}',
            'start_time': subtitle['start_time'],
            'end_time': subtitle['end_time'],
            'text': subtitle['text']
        }
        for i, subtitle in enumerate(subtitles)
    ]

    # print("DynamoDB items:", dynamodb_items)

    with table.batch_writer() as batch:
        for item in dynamodb_items:
            try:
                batch.put_item(Item=item)
                # print(f"Item added to DynamoDB table '{table_name}': {item}")
            except WaiterError as e:
                print(f"Error adding item to DynamoDB table '{table_name}': {e}")
    # print("After batch writer")

# FUNCTION TO SEARCH KEYWORDS
def search(subtitles, search_phrase):
    matching_segments = []

    for subtitle in subtitles:
        if search_phrase.lower() in subtitle['text'].lower():
            matching_segments.append({
                'start_time': subtitle['start_time'],
                'end_time': subtitle['end_time'],
                'text': subtitle['text']
            })

      
    # print(matching_segments)
    return matching_segments

