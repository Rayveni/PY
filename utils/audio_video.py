#!pip install moviepy
#!pip install ffmpeg --upgrade
import moviepy.editor as mp

def compress_replace_audio(output_file:str,video_file:str,audio_file:str=None):
    #Input video file
    video = mp.VideoFileClip(video_file)
    #adding external audio to video
    if audio_file is not None:
        #Input audio file  
        audio = mp.AudioFileClip(audio_file)
        final_video = video.set_audio(audio)
    else:
        final_video=video
    #Extracting final output video
    final_video.write_videofile(output_file, fps=30)
    
def extract_audio(output_file:str,input_file :str):
    #video = mp.VideoFileClip(input_file)
    sound = mp.AudioFileClip(input_file)
    sound.write_audiofile(output_file)

in_file=r'C:\Users\ivolochkov\Videos\interview\{}.mkv'   
out_file=r'C:\Users\ivolochkov\Videos\interview\final\{}.mp3'
f_name='neoflex'
extract_audio(out_file.format(f_name),in_file.format(f_name))
