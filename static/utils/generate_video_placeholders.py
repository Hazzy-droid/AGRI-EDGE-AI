"""
Script to generate video placeholders and thumbnail for the Climate-Smart Agriculture Platform

This script creates placeholder MP4 videos and thumbnail for demonstration purposes.
It uses FFmpeg to generate color-gradient videos with text overlays.
"""

import os
import subprocess
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Define paths
STATIC_DIR = Path("static")
VIDEOS_DIR = STATIC_DIR / "videos"
IMG_DIR = STATIC_DIR / "img"

# Make sure directories exist
VIDEOS_DIR.mkdir(exist_ok=True, parents=True)
IMG_DIR.mkdir(exist_ok=True, parents=True)

# Video configurations
VIDEO_CONFIGS = [
    {
        "name": "welcome",
        "title": "Welcome to Climate-Smart Agriculture Platform",
        "subtitle": "An introduction to our platform's features and capabilities",
        "duration": 3,  # seconds, for placeholder
        "color": "0x1E40AF-0x3B82F6"  # gradient from dark blue to blue
    },
    {
        "name": "dashboard",
        "title": "Dashboard Tutorial",
        "subtitle": "Learn how to use the main dashboard",
        "duration": 3,
        "color": "0x065F46-0x10B981"  # gradient from dark green to green
    },
    {
        "name": "satellite",
        "title": "Satellite Imagery Tutorial",
        "subtitle": "Understanding NDVI and crop health monitoring",
        "duration": 3,
        "color": "0x7E22CE-0xA855F7"  # gradient from dark purple to purple
    },
    {
        "name": "weather",
        "title": "Weather Forecasting Tutorial",
        "subtitle": "Using weather data for agricultural planning",
        "duration": 3,
        "color": "0x0369A1-0x0EA5E9"  # gradient from dark sky blue to sky blue
    },
    {
        "name": "soil",
        "title": "Soil Monitoring Tutorial",
        "subtitle": "Interpreting soil moisture and fertility data",
        "duration": 3,
        "color": "0x7C2D12-0xEA580C"  # gradient from dark brown to orange
    },
    {
        "name": "recommendations",
        "title": "Recommendations Tutorial",
        "subtitle": "Understanding AI-powered agricultural recommendations",
        "duration": 3,
        "color": "0x155E75-0x06B6D4"  # gradient from dark cyan to cyan
    },
    {
        "name": "community",
        "title": "Community Platform Tutorial",
        "subtitle": "Connecting with other farmers and experts",
        "duration": 3,
        "color": "0x991B1B-0xEF4444"  # gradient from dark red to red
    },
    {
        "name": "marketplace",
        "title": "Marketplace Tutorial",
        "subtitle": "Buying and selling agricultural products",
        "duration": 3,
        "color": "0x854D0E-0xF59E0B"  # gradient from dark amber to amber
    },
    {
        "name": "messages",
        "title": "Messaging System Tutorial",
        "subtitle": "Communicating with other platform users",
        "duration": 3,
        "color": "0x0F766E-0x14B8A6"  # gradient from dark teal to teal
    },
    {
        "name": "settings",
        "title": "Settings Page Tutorial",
        "subtitle": "Customizing your account preferences",
        "duration": 3,
        "color": "0x0F172A-0x475569"  # gradient from dark slate to slate
    },
    {
        "name": "learning",
        "title": "Learning Module Tutorial",
        "subtitle": "Accessing educational content on agriculture",
        "duration": 3,
        "color": "0x831843-0xEC4899"  # gradient from dark pink to pink
    }
]

def generate_thumbnail():
    """Generates a welcome video thumbnail"""
    output_path = IMG_DIR / "welcome-video-thumbnail.jpg"
    
    # Check if the thumbnail already exists
    if output_path.exists():
        logger.info(f"Thumbnail already exists: {output_path}")
        return
    
    cmd = [
        "ffmpeg", "-f", "lavfi", "-i", 
        f"color=c=0x1E40AF:s=1280x720,format=yuv420p", 
        "-vf", "drawtext=text='Welcome to Climate-Smart Agriculture Platform':fontcolor=white:fontsize=48:x=(w-text_w)/2:y=(h-text_h)/2-40,"
        "drawtext=text='Click to Watch Introduction Video':fontcolor=white:fontsize=32:x=(w-text_w)/2:y=(h-text_h)/2+40",
        "-frames:v", "1", str(output_path)
    ]
    
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        logger.info(f"Generated thumbnail: {output_path}")
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to generate thumbnail: {e}")
        logger.error(f"Error output: {e.stderr.decode() if e.stderr else 'None'}")
    except Exception as e:
        logger.error(f"Unexpected error generating thumbnail: {e}")

def generate_video_placeholder(config):
    """Generates a video placeholder based on the configuration"""
    output_path = VIDEOS_DIR / f"{config['name']}.mp4"
    
    # Check if the video already exists
    if output_path.exists():
        logger.info(f"Video already exists: {output_path}")
        return
    
    # Create ffmpeg command
    cmd = [
        "ffmpeg", "-f", "lavfi", "-i", 
        f"gradients=s=1280x720:c0={config['color']}:d={config['duration']}:speed=0.5",
        "-vf", f"drawtext=text='{config['title']}':fontcolor=white:fontsize=48:x=(w-text_w)/2:y=(h-text_h)/2-40,"
        f"drawtext=text='{config['subtitle']}':fontcolor=white:fontsize=32:x=(w-text_w)/2:y=(h-text_h)/2+40,"
        "drawtext=text='This is a placeholder for the actual tutorial video':fontcolor=white:fontsize=24:x=(w-text_w)/2:y=(h-text_h)/2+120",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-shortest", str(output_path)
    ]
    
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        logger.info(f"Generated video placeholder: {output_path}")
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to generate video for {config['name']}: {e}")
        logger.error(f"Error output: {e.stderr.decode() if e.stderr else 'None'}")
    except Exception as e:
        logger.error(f"Unexpected error generating video for {config['name']}: {e}")

def check_ffmpeg():
    """Check if FFmpeg is installed"""
    try:
        result = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True)
        logger.info("FFmpeg is installed")
        return True
    except Exception:
        logger.error("FFmpeg is not installed or not in PATH. Please install FFmpeg to generate videos.")
        return False

def create_text_placeholders():
    """Create simple text files as placeholders if FFmpeg is not available"""
    for config in VIDEO_CONFIGS:
        output_path = VIDEOS_DIR / f"{config['name']}.txt"
        
        with open(output_path, 'w') as f:
            f.write(f"Video: {config['title']}\n")
            f.write(f"{config['subtitle']}\n")
            f.write("This is a placeholder for the actual tutorial video.")
        
        logger.info(f"Created text placeholder: {output_path}")
    
    # Create thumbnail placeholder
    with open(IMG_DIR / "welcome-video-thumbnail.txt", 'w') as f:
        f.write("Welcome to Climate-Smart Agriculture Platform\n")
        f.write("Click to Watch Introduction Video")
    
    logger.info("Created thumbnail text placeholder")

def main():
    """Main function to generate all video placeholders"""
    logger.info("Starting to generate video placeholders")
    
    # Check if FFmpeg is installed
    if check_ffmpeg():
        # Generate the welcome video thumbnail
        generate_thumbnail()
        
        # Generate all video placeholders
        for config in VIDEO_CONFIGS:
            generate_video_placeholder(config)
    else:
        # Create simple text placeholders if FFmpeg is not available
        create_text_placeholders()
    
    logger.info("Finished generating video placeholders")

if __name__ == "__main__":
    main()