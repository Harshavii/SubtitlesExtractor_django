from django.shortcuts import render
from .utils import upload_to_s3, parse_srt, store_dynamodb, search
from django.shortcuts import render, redirect
import subprocess
import secrets
import os
from django.conf import settings

# BUCKET NAME
bucket_name = 'subtitle4bucket'
aa = secrets.token_hex(4)

# MAIN FUNC.
def extract_subtitles(request):
    if request.method == 'POST':
        video_file = request.FILES.get('video_file')
        search_phrase = request.POST.get('search_phrase', '')

        if video_file:
            aa = secrets.token_hex(4)
            unique_filename = aa + '.mp4'
            temp_file_path = os.path.join('temp_videos', unique_filename)

            os.makedirs(os.path.dirname(temp_file_path), exist_ok=True)

            with open(temp_file_path, 'wb') as temp_file:
                for chunk in video_file.chunks():
                    temp_file.write(chunk)



            # # Call Celery task instead of performing tasks directly
            # result = process_video.delay(temp_file_path, search_phrase)

            # # Redirect to a processing page with the task ID
            # return redirect('processing_status', task_id=result.id)


            # UPLOADING VIDEO TO S3
            object_key = f'videos/{unique_filename}'
            upload_to_s3(temp_file_path, bucket_name, object_key)

            base_path = os.path.dirname(os.path.abspath(__file__))
            # print(base_path)
            ccextractor_path = os.path.join(base_path, "CCExtractor_bin", "ccextractorwinfull.exe")
            # print(ccextractor_path)



            # ccextractor_path = r"djangoCC\ccextractorwinfull.exe"
            command = [ccextractor_path, temp_file_path, "-o", f"{aa}.srt"]
            try:
                result = subprocess.run(command, capture_output=True, text=True, check=True)
                subtitles = result.stdout

                # print(temp_file_path)             this is path of video and not srt file
                subtitles_data = parse_srt(F"{aa}.srt")   #this var should have list of subtitles

                video_filename = unique_filename.split('.')[0]  # Use the video filename without extension

                # STORING SUBTITLES IN DYNAMODB
                store_dynamodb(subtitles_data, video_filename)
                print("subtitles uploaded to dynamo db table")  

                # Pass the video file path to the HTML page
                # path = settings.BASE_DIR
                # print(path)
                video_file_path = r'C:\Users\harsh\OneDrive\Desktop\Django_CC\djangoCC\temp_videos' + unique_filename

                search_phrase = request.POST.get('search_phrase', '')
                # print(search_phrase)
                matching_segments = search(subtitles_data, search_phrase)
                

                # os.remove(temp_file_path)
                return render(request, 'index.html', {'subtitles': subtitles,'video_file': video_file_path, 'matching_segments': matching_segments, 'search_phrase': search_phrase})
            

            except subprocess.CalledProcessError as e:
                error_message = f"Error running ccextractor: {e.stderr}"
                return render(request, 'index.html', {'error': error_message})


    return render(request, 'index.html')

