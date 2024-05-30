import yt_dlp
import subprocess
import os

def download_youtube_video(video_url, output_path, username, password):
    """
    Downloads a YouTube video from a given URL to a specified output path using yt-dlp, including auto-generated captions.
    The captions are embedded into the video.
    
    Parameters:
    video_url (str): URL of the YouTube video to be downloaded.
    output_path (str): Local path where the video will be saved, including the filename.
    username (str): YouTube account username.
    password (str): YouTube account password.
    """
    try:
        # Temporary paths for video and subtitles
        temp_video_path = output_path.replace(".mp4", "_temp.mp4")
        temp_subs_path_vtt = output_path.replace(".mp4", ".en.vtt")
        temp_subs_path_ass = output_path.replace(".mp4", ".en.ass")

        ydl_opts = {
            'format': 'best',
            'outtmpl': temp_video_path,
            'username': username,
            'password': password,
            'subtitleslangs': ['en'],  # You can specify other languages if needed
            'writesubtitles': True,
            'writeautomaticsub': True,  # Include auto-generated captions
            'subtitlesformat': 'vtt'  # Subtitle format
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        print(f"Video and subtitles downloaded successfully")

        # Check the existence of the actual subtitle file
        subtitle_files = [f for f in os.listdir(os.path.dirname(temp_subs_path_vtt)) if f.endswith('.vtt')]
        if not subtitle_files:
            raise FileNotFoundError("No subtitle files found.")
        
        # Ensure correct subtitle file path
        actual_subs_path_vtt = os.path.join(os.path.dirname(temp_subs_path_vtt), subtitle_files[0])

        # Convert VTT subtitles to ASS format
        convert_vtt_to_ass(actual_subs_path_vtt, temp_subs_path_ass)

        # Embed subtitles into the video
        embed_subtitles(temp_video_path, temp_subs_path_ass, output_path)
        print(f"Video with subtitles saved to {output_path}")
    
    except Exception as e:
        print(f"An error occurred: {e}")

def convert_vtt_to_ass(vtt_path, ass_path):
    """
    Converts VTT subtitles to ASS format using ffmpeg.
    
    Parameters:
    vtt_path (str): Path to the VTT subtitles file.
    ass_path (str): Path where the converted ASS subtitles will be saved.
    """
    try:
        command = [
            'ffmpeg',
            '-i', vtt_path,
            '-c:s', 'ass',
            ass_path
        ]
        subprocess.run(command, check=True)
        print(f"Subtitles converted to ASS format successfully: {ass_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error converting subtitles: {e}")

def embed_subtitles(video_path, subs_path, output_path):
    """
    Embeds subtitles into a video file using ffmpeg.
    
    Parameters:
    video_path (str): Path to the video file.
    subs_path (str): Path to the subtitles file.
    output_path (str): Path where the output video with subtitles will be saved.
    """
    try:
        command = [
            'ffmpeg',
            '-i', video_path,
            '-vf', f"subtitles={subs_path}",
            '-c:a', 'copy',
            output_path
        ]
        subprocess.run(command, check=True)
        print(f"Subtitles embedded successfully into {output_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error embedding subtitles: {e}")

# Example usage
video_url = "https://www.youtube.com/watch?v=NbT8YZBWwBA"
output_path = "/Users/korrenhannes/Desktop/videos/subs.mp4"  # Ensure the filename is included
username = "korrenh@gmail.com"
password = "Kokoh100"
download_youtube_video(video_url, output_path, username, password)
