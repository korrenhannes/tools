import requests
import shutil

def download_video(video_url, output_path):
    """
    Downloads a video from a given URL to a specified output path.

    Parameters:
    video_url (str): URL of the video to be downloaded.
    output_path (str): Local path where the video will be saved.
    """
    try:
        # Send a GET request to the video URL
        response = requests.get(video_url, stream=True)

        # Check if the request was successful
        if response.status_code == 200:
            # Open the output file in binary mode and write the content
            with open(output_path, 'wb') as file:
                shutil.copyfileobj(response.raw, file)
            print(f"Video downloaded successfully and saved to {output_path}")
        else:
            print(f"Failed to download video. Status code: {response.status_code}")
    
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
video_url = "https://www.youtube.com/watch?v=LBbq3CgCux8"
output_path = "/Users/korrenhannes/Desktop/videos"
download_video(video_url, output_path)
