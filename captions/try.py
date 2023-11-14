# import boto3
# from botocore.exceptions import NoCredentialsError
# import os

# s3 = boto3.client(
#     's3',
#     aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),  # Replace with your AWS access key
#     aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),  # Replace with your AWS secret key
#     region_name=os.environ.get('AWS_DEFAULT_REGION')  # Replace with your AWS region
# )

# # Upload the processed video to S3
# file_path = r'C:\Users\harsh\OneDrive\Desktop\Django_CC\djangoCC\sample.mp4'
# bucket_name = 'subtitle4bucket'
# object_key = 'videos/temp_video.mp4'

# try:
#     s3.upload_file(file_path, bucket_name, object_key)
#     print(f"File uploaded to S3: {object_key}")
# except NoCredentialsError:
#     print("Credentials not available or incorrect. Please check your AWS credentials.")
# except Exception as e:
#     print(f"Error uploading file to S3: {e}")

# # upload_to_s3(video_file_path, bucket_name, object_key)

from utils import parse_srt, store_dynamodb

subtitles = parse_srt(r'C:\Users\harsh\OneDrive\Desktop\Django_CC\djangoCC\temp_videos\86f1fda4.srt')

store_dynamodb(subtitles,'random')

