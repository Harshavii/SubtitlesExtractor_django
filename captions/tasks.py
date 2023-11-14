# # tasks.py
# from celery import shared_task
# from .utils import upload_to_s3, parse_srt, store_dynamodb, search
# # from .views import aa, bucket_name
# import subprocess
# import logging
# import secrets
# import os

# @shared_task
# def process_video(temp_file_path, search_phrase):

#     bucket_name = 'subtitle4bucket'
#     aa = secrets.token_hex(4)

#     # Upload video to S3
#     object_key = f'videos/{aa}.mp4'
#     upload_to_s3(temp_file_path, bucket_name, object_key)

#     ccextractor_path = "C:\\Users\\harsh\\OneDrive\\Desktop\\Django_CC\\djangoCC\\CCExtractor_bin\\ccextractorwinfull.exe"
#     command = [ccextractor_path, temp_file_path, "-o", f"{aa}.srt"]
#     try:
#         result = subprocess.run(command, capture_output=True, text=True, check=True)
#         subtitles = result.stdout

#         # print(temp_file_path)             this is path of video and not srt file
#         # PARSING SRT FILE
#         subtitles_data = parse_srt(f"{aa}.srt")   #this var should have list of subtitles

#         video_filename = aa 

#         # STORING SUBTITLES IN DYNAMODB
#         store_dynamodb(subtitles_data, video_filename)
#         print("subtitles uploaded to dynamo db table")  

#         # Pass the video file path to the HTML page
#         video_file_path = r'C:\Users\harsh\OneDrive\Desktop\Django_CC\djangoCC\temp_videos' + f'{aa}.mp4'

#         # SEARCHING ENTERED KEYWORD
#         matching_segments = search(subtitles_data, search_phrase)
        
#         return subtitles, video_file_path, matching_segments, search_phrase
    
#     except subprocess.CalledProcessError as e:
#         error_message = f"Error running ccextractor: {e.stderr}"
#         return error_message       

