import os
import sys

def run_command(command):
    os.system(command)

# Get the song title from the command line argument
song_title = sys.argv[1]

# Split the song title into individual words
words = song_title.split()

# Construct the command using each word separately
command = ""
for word in words:
    command += f"open '{word} {'dreams'}.m3u'"

run_command(command)
