import os
import googleapiclient.discovery

api_service_name = "youtube"
api_version = "v3"
DEVELOPER_KEY = "AIzaSyARp0HFHHsahQsoDJSmVagAZ3EygVVHRoA"
youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey = DEVELOPER_KEY)

def retrive_youtube_videos(videoArry):
    
    request = youtube.videos().list(
        part="snippet, contentDetails",
        id = videoArry
    )

    response = request.execute()
    return response