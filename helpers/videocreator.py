import multiprocessing
from moviepy.editor import *
from moviepy.video.fx.resize import resize
from moviepy.video.fx.crop import crop
import random
import math

class VideoCreator:
    @staticmethod
    def create_video(number_of_clips, path_name):
        screenshots = [f"{path_name}/paragraph_{i}.png" for i in range(1, number_of_clips)]
        #screenshots.insert(0, f"{path_name}/title.png")
        audio_files = [f"{path_name}/{i}.mp3" for i in range(1, number_of_clips)]
        #audio_files.insert(0, f"{path_name}/title.mp3")
        #title_clip = ImageClip(f"{path_name}/final_title.jpg").set_duration(AudioFileClip(audio_files[0]).duration).resize(width=800).set_position("center")
        clips = [ImageClip(m).set_duration(AudioFileClip(a).duration) for m, a in zip(screenshots, audio_files)]
        [print(m, a) for m, a in zip(screenshots, audio_files)]
        #clips = [ImageClip(f"{path_name}/title.png").set_duration(AudioFileClip(a).duration) for m, a in zip(screenshots, audio_files)]
        for i, clip in enumerate(clips):
            print(i)
            clips[i] = clip.resize(width=600).set_position("center")

        final_video = concatenate_videoclips(clips, method="compose").set_position((660, 400))
        final_audio = concatenate_audioclips([AudioFileClip(audio) for audio in audio_files])
        audio_duration = final_audio.duration
        start_timing = random.randint(0, 4813 - math.floor(audio_duration))

        video = VideoFileClip("vid.mp4")

        title_audio = AudioFileClip(f"{path_name}/0.mp3")
        temp = ImageClip(f"{path_name}/paragraph_{0}.png").set_duration(title_audio.duration)
        temp = temp.resize(width=600).set_position("center")
        temp2 = concatenate_videoclips([temp], method="compose").set_position((660, 400))
        temp2.audio = AudioFileClip(f"{path_name}/0.mp3")
        title_background = video.subclip(start_timing, start_timing + title_audio.duration)
        #title_background = crop(title_background, x1=656.25, y1=0, x2=1263.75, y2=1080)
        #.resize(width=1080)
        title_video = CompositeVideoClip([title_background, temp2])
        #title_video.write_videofile(f'{path_name}/title.mp4', fps=30, codec='libx264', audio_codec="aac", audio_bitrate="192k")  

        print(start_timing)

        trimmed_video = video.subclip(start_timing + title_audio.duration, start_timing + title_audio.duration + audio_duration)
        #trimmed_video = crop(trimmed_video, x1=656.25, y1=0, x2=1263.75, y2=1080).resize(width=1080)
        final_video = CompositeVideoClip([trimmed_video, final_video])
        final_video.audio = final_audio

        # write the final clip to a video file
        #final_video.write_videofile(f'{path_name}/asdf.mp4', fps=30, codec='libx264', audio_codec="aac", audio_bitrate="192k")            

        # Load the two videos
        # video1 = VideoFileClip(f'{path_name}/title.mp4')
        # video2 = VideoFileClip(f'{path_name}/asdf.mp4')

        # Concatenate the videos
        final_clip = concatenate_videoclips([title_video, final_video], method="compose")
        final_clip = crop(final_clip, x1=656, y1=0, x2=1263, y2=1080)
        #.resize(width=1080) 

        # Write the final video to a file
        final_clip.write_videofile(f'{path_name}/output.mp4', fps=30, codec='libx264', audio_codec="aac", audio_bitrate="192k", verbose=False, threads=multiprocessing.cpu_count(),)