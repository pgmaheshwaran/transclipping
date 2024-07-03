# Transclipping

Transclipping is a Python utility designed to facilitate the process of creating video clips based on specific sections of transcribed text obtained from Amazon Transcribe. This utility aims to automate the extraction of relevant video segments corresponding to identified text snippets within the transcription.

## Prerequisite 
* Install latest python
* Install FFMPEG utility 

## Step to run the utility

* Clone the repository

`git clone https://github.com/pgmaheshwaran/transclipping.git`

* Traverse to the project directory using below command

`cd transclipping`

* Usage details

`python src/transclipping.py <Video File path> <Transcribe output for the video> <Section of transcribed text> <Output file name> `

* Execute the below command, the sample source and transcribe output is available for testing

`python src/transclipping.py sample/test_video.mp4 sample/transcribe_output.json "Indian troops along the line of actual control in Ladakh has begun." clip.mp4`

* You will find the clip.mp4 file generated based on supplied section of the transcibed text.

