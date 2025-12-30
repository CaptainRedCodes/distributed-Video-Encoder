import glob
import math
import tempfile
import os
import subprocess, json



file_path = r"C:\Users\svmra\Videos\X2Twitter.com_1779866393212817408(720p).mp4"

#Video Chunking
def split_media(file_path,chunk_duration=20):
    file_size = os.path.getsize(file_path)

    prep_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    prep_file_path = prep_file.name
    prep_file.close()
    
    #prepping video with key frames
    cmd_prepare = [
                "ffmpeg",
                "-i", file_path,
                "-map", "0",
                "-c:v", "libx264",
                "-force_key_frames", "expr:gte(t,n_forced*{})".format(chunk_duration),
                "-preset", "fast",
                "-crf", "23",
                "-c:a", "copy",
                "-y",
                prep_file_path
            ]
    run_command_with_output(cmd_prepare, "Preparing video with keyframes")

    #chunking the prepped video
    output_pattern = os.path.join(tempfile.gettempdir(), "chunk_%03d.mp4")
    cmd_split = [
                "ffmpeg",
                "-i", prep_file_path,
                "-map", "0",
                "-f", "segment",
                "-segment_time", str(chunk_duration),
                "-reset_timestamps", "1",
                "-c", "copy",
                "-y",
               output_pattern
            ]

    run_command_with_output(
            cmd_split, 
            f"splittting chunks"
    )

    chunks = sorted(glob.glob((os.path.join(tempfile.gettempdir(), "chunk_*.mp4"))))
    os.remove(prep_file_path)
    return chunks
        

#video duration
def with_ffprobe(filepath):
    """
    Return the total length of the media
    
    :param filepath: path of the file
    """
    result = subprocess.run(
        [
            "ffprobe",
            "-v", "quiet",
            "-show_format",
            "-of", "json",
            filepath
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=True
    )
    
    data = json.loads(result.stdout)
    return float(data["format"]["duration"])

def run_command_with_output(cmd, desc=None):
    """Run a command and stream its output in real-time"""
    if desc:
        print(f"\n{desc}")
    
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True
    )
    
    if process.stdout:
        for line in iter(process.stdout.readline, ''):
            print(line, end='')
        process.stdout.close()
    
    return_code = process.wait()
    
    if return_code != 0:
        raise subprocess.CalledProcessError(return_code, cmd)
    
if __name__ == "__main__":
    split_media(file_path,chunk_duration=6)

#parallel processing
#video merging
