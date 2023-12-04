# Subtitles extractor

This Django-based project utilizes the CCextractor binary file to extract closed captions from video files.
The application incorporates Amazon's S3 storage for uploading user files and leverages Amazon's DynamoDB to store the extracted subtitles in a tabular format along with their corresponding timestamps.

The ultimate goal is to enable users to search for specific keywords, prompting the system to display the timestamp of occurrence for the identified subtitles.
