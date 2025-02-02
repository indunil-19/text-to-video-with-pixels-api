from openai import OpenAI
import os
import edge_tts
import json
import asyncio
import whisper_timestamped as whisper
from utility.script.script_generator import generate_script
from utility.audio.audio_generator import generate_audio
from utility.captions.timed_captions_generator import generate_timed_captions
from utility.video.background_video_generator import generate_video_url
from utility.render.render_engine import get_output_media
from utility.video.video_search_query_generator import getVideoSearchQueriesTimed, merge_empty_intervals
import argparse
import time

VIDEO_SERVER = "pexel"
OUTPUT_FOLDER = "generate_videos"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def generate_videos(topics):
    for topic in topics:
        print(f"Generating video for topic: {topic}")
        
        SAMPLE_FILE_NAME = f"{topic.replace(' ', '_')}_audio_tts.wav"
        
        # Generate script
        response = generate_script(topic)
        print(f"Script for {topic}: {response}")
        
        # Generate audio
        asyncio.run(generate_audio(response, SAMPLE_FILE_NAME))
        
        # Generate captions
        timed_captions = generate_timed_captions(SAMPLE_FILE_NAME)
        print(f"Captions for {topic}: {timed_captions}")
        
        # Generate search terms for background videos
        search_terms = getVideoSearchQueriesTimed(response, timed_captions)
        print(f"Search terms for {topic}: {search_terms}")
        
        background_video_urls = None
        if search_terms:
            background_video_urls = generate_video_url(search_terms, VIDEO_SERVER)
            print(f"Background videos for {topic}: {background_video_urls}")
        else:
            print("No background video found")
        
        background_video_urls = merge_empty_intervals(background_video_urls)
        
        # Generate final video
        if background_video_urls:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            output_file_name = os.path.join(OUTPUT_FOLDER, f"rendered_video_{timestamp}.mp4")
            video = get_output_media(SAMPLE_FILE_NAME, timed_captions, background_video_urls, VIDEO_SERVER, output_file_name)
            print(f"Video generated for {topic}: {video}")
        else:
            print(f"No video created for {topic}")


