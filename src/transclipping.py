import subprocess
import json
import string
import os

def get_word_timecodes(transcribe_file):
    with open(transcribe_file, 'r') as f:
        transcript = json.load(f)
    return transcript["results"]["items"]

def find_timecodes(transcript, search_text):
    t_phrase = ""
    matched = False
    timecodes = []
    words = search_text.split()
    for index, t_word in enumerate(transcript):
        if matched:
            break
        #print("t_word ", t_word['alternatives'][0]['content'])
        for s_word in words:
            #print( "s_word ", s_word)
            if s_word == t_word['alternatives'][0]['content']:
                #print("Matched!")
                start_time, end_time = match_text_for_timecode(transcript, index, search_text)
                if start_time != -1 and end_time != -1:
                    timecodes.append({'start_time':start_time,'end_time':end_time, 'search_text':search_text})
                    matched = True
                    break
    return timecodes

def match_text_for_timecode(transcript, start_index, search_text):
    updated_text, punctuation_count = get_punctuation_count(search_text)
    words = search_text.split()
    sub_transcript = []
    construct_text = ''
    timecode_info = []
    for i in range(start_index, start_index + len(words)+ punctuation_count):
        sub_transcript.append(transcript[i])
        construct_text += transcript[i]['alternatives'][0]['content'] + " "       
    print( construct_text , updated_text)
    start_time = -1
    end_time = -1
    if construct_text.strip() == updated_text.strip():
        for script in sub_transcript:
            if script['type'] == 'punctuation':
                continue;
            elif start_time == -1:
                start_time = script['start_time']
            else:
                end_time = script['end_time']
    return start_time, end_time

def get_punctuation_count(search_text):
    punctuation_chars = set(string.punctuation)
    punctuation_count = 0
    updated_text = ''
    for char in search_text:
        if char in punctuation_chars:
            punctuation_count += 1
            updated_text += " "+ char
        else: 
            updated_text += char
    print("Updated Text ",updated_text)
    return updated_text, punctuation_count

def clip_video(video_file, output_file, start_time, end_time):
    command = [
        'ffmpeg',
        '-i', video_file,
        '-ss', str(start_time),
        '-to', str(end_time),
        '-c', 'copy',
        output_file
    ]
    subprocess.run(command, check=True)

def print_usage():
    print("python transclipping.py <video file path> <Transcribe output file> <Search text> <Output clip file name>")
    exit(0)

if __name__ == "__main__":
    import sys
    if not len(sys.argv) == 5:
        print_usage()
    video_file = sys.argv[1]
    output_file = sys.argv[4]
    transcribe_file = sys.argv[2]
    search_text = sys.argv[3]
    transcript = get_word_timecodes(transcribe_file)
    timecodes = find_timecodes(transcript, search_text)
    print(timecodes)
    if not os.path.exists(video_file):
        print("Valid Video file not provided, please check!!")
        print_usage()
    elif not os.path.exists(transcribe_file):
        print("Valid Transcribe file not provided, Please check!!")
        print_usage()
    elif not search_text:
        print("Search text not provided, please check!!")
        print_usage()
    elif not output_file:
        print("Output file name not provided, please check!!")
        print_usage()
    if timecodes:
        clip_video(video_file, output_file, timecodes[0]['start_time'], timecodes[0]['end_time'])
        print(f'Created clip: {output_file} for text: "{search_text}"')
