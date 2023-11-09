import os
import subprocess
import dbus
import time
import readline
import re
import random
import shutil
import readline
from urllib.parse import unquote

#cat /dev/null > ~/.bash_history
#history -c
#truncate -s 0 history.m3u
#truncate -s 0 history3333.m3u

def extract_info_from_playlists(playlist_path):
    playlist_info = {"Artist": "", "Album": "", "Song": ""}
    
    with open(playlist_path, "r") as playlist_file:
        for line in playlist_file:
            if line.startswith("# Artist:"):
                playlist_info["Artist"] = line.split(":")[1].strip()
            elif line.startswith("# Album:"):
                playlist_info["Album"] = line.split(":")[1].strip()
            elif line.startswith("# Song:"):
                playlist_info["Song"] = line.split(":")[1].strip()
    
    return playlist_info

def guessing_game(playlist_info):
    print("Guess the details of the playlist:")
    guess_artist = input("Guess the Artist: ")
    guess_album = input("Guess the Album: ")
    guess_song = input("Guess the Song: ")

    return (guess_artist.lower() == playlist_info["Artist"].lower() and
            guess_album.lower() == playlist_info["Album"].lower() and
            guess_song.lower() == playlist_info["Song"].lower())

def listening_game():
    playlists_folder = "/home/riley"  # Change to the appropriate folder
    playlist_titles = []

    with open("history3333.m3u", "r") as file:
        for line in file:
            line = line.strip()
            if not line.endswith(".m3u"):
                line += ".m3u"
            playlist_titles.append(line)

    while True:
        if not playlist_titles:
            print("No playlists available.")
            break
        
        playlist_title = random.choice(playlist_titles)
        playlist_titles.remove(playlist_title)
        
        playlist_path = os.path.join(playlists_folder, playlist_title)
        
        if os.path.exists(playlist_path):
            playlist_info = extract_info_from_playlists(playlist_path)
            os.system(f"vlc -I null --play-and-exit '{playlist_path}'")
            result = guessing_game(playlist_info)
            if result:
                print("Correct!")
            else:
                print(f"Sorry, the correct information is:")
                print(f"Artist: {playlist_info['Artist']}")
                print(f"Album: {playlist_info['Album']}")
                print(f"Song: {playlist_info['Song']}")
        else:
            print(f"Playlist '{playlist_title}' not found.")
        
        user_input = input("Enter 0 to exit or press Enter to continue: ")
        if user_input == "0":
            break

def clear_bash_history():
    os.system("sudo history >> history888.m3u")


def save_bash_history_to_m3u():
    # Path to the history file
    bash_history_path = os.path.join(os.path.expanduser("~"), ".bash_history")

    # Read the Bash history
    with open(bash_history_path, "r") as bash_history_file:
        history_lines = bash_history_file.readlines()

    # Path to the history.m3u file
    history_m3u_path = os.path.join(os.path.expanduser("~"), "history.m3u")
    # Write the Bash history to history.m3u
    with open(history_m3u_path, "w") as history_m3u_file:
        history_m3u_file.writelines(history_lines)

def create_custom_playlist():
    playlist_name = input("Enter the custom playlist name: ")
    playlist_path = os.path.join(os.path.expanduser("~"), f"{playlist_name}.m3u")

    with open(playlist_path, "w") as playlist_file:
        while True:
            song_title = input("Enter a song title to add to the playlist (type '0' to stop): ")
            if song_title == "0":
                break
            playlist_file.write(f"{song_title}.m3u\n")

def vlc_play():
    subprocess.run(["dbus-send", "--type=method_call", "--dest=org.mpris.MediaPlayer2.vlc", "/org/mpris/MediaPlayer2", "org.mpris.MediaPlayer2.Player.Play"])

def vlc_pause():
    subprocess.run(["dbus-send", "--type=method_call", "--dest=org.mpris.MediaPlayer2.vlc", "/org/mpris/MediaPlayer2", "org.mpris.MediaPlayer2.Player.Pause"])

def vlc_next():
    subprocess.run(["dbus-send", "--type=method_call", "--dest=org.mpris.MediaPlayer2.vlc", "/org/mpris/MediaPlayer2", "org.mpris.MediaPlayer2.Player.Next"])

def vlc_previous():
    subprocess.run(["dbus-send", "--type=method_call", "--dest=org.mpris.MediaPlayer2.vlc", "/org/mpris/MediaPlayer2", "org.mpris.MediaPlayer2.Player.Previous"])

def vlc_enqueue_playlist(playlist_path):
    if not playlist_path.endswith('.m3u'):
        playlist_path += '.m3u'
    formatted_path = f"{playlist_path}"
    subprocess.run(["vlc", "--playlist-enqueue", formatted_path])

def vlc_enqueue_song(song_title):
    formatted_title = f"{song_title}.m3u"
    subprocess.run(["vlc", "--playlist-enqueue", formatted_title])

def change_volume(volume):
    if volume < 1 or volume > 10:
        print("Invalid input. Please enter a number between 1 and 10.")
        return

    volume_percent = volume * 10
    command = f"amixer -D pulse sset Master {volume_percent}%"
    subprocess.run(command, shell=True)

def change_volume(volume):
    if volume < 1 or volume > 10:
        print("Invalid input. Please enter a number between 1 and 10.")
        return

    volume_percent = volume * 10
    command = f"amixer -D pulse sset Master {volume_percent}%"
    subprocess.run(command, shell=True)
# Create an empty list to track the executed commands
executed_commands = []


def get_current_volume():
    # Get the current volume level using amixer command
    command = "amixer -D pulse sget Master | grep 'Front Left:' | awk -F'[][]' '{ print $2 }'"
    output = subprocess.check_output(command, shell=True, text=True)
    volume_str = output.strip().replace('%', '')  # Remove the percentage sign
    return int(volume_str)

def change_volume2():
    current_volume = get_current_volume()
    new_volume = current_volume + 10

    if new_volume > 100:
        new_volume = 100

    command = f"amixer -D pulse sset Master {new_volume}%"
    subprocess.run(command, shell=True)


def change_volume3():
    current_volume = get_current_volume()
    new_volume = current_volume - 10

    if new_volume > 100:
        new_volume = 100

    command = f"amixer -D pulse sset Master {new_volume}%"
    subprocess.run(command, shell=True)



def skip_tracks(choice):
    bus = dbus.SessionBus()
    player_obj = bus.get_object('org.mpris.MediaPlayer2.vlc', '/org/mpris/MediaPlayer2')
    player_interface = dbus.Interface(player_obj, 'org.mpris.MediaPlayer2.Player')

    if choice > 0:
        for _ in range(choice):
            vlc_previous()
            time.sleep(0.1)
    else:
        for _ in range(-choice):
            vlc_next()
            time.sleep(0.1)

# Create an empty list to track the executed commands
executed_commands = []

def execute_command(command):
    formatted_command = f"open '{command}.m3u'"
    os.system(formatted_command)
    executed_commands.append(formatted_command)

def execute_command2(command):
    formatted_command = f"{command}"
    os.system(formatted_command)
    executed_commands.append(formatted_command)


# (existing code)

def save_command_history_to_playlist(playlist_name):
    # Get the user's home directory
    home_dir = os.path.expanduser("~")
    history_file_path = os.path.join(home_dir, "history.m3u")

    # Read the entire history from the history file
    with open(history_file_path, "r") as history_file:
        history_lines = history_file.readlines()

    # Ask the user for the number of lines to include in the playlist
    num_lines = int(input("Enter the number of lines from the history to include in the playlist: "))
    if num_lines <= 0:
        print("Invalid number of lines. Playlist not created.")
        return

    # Create the M3U playlist with the given playlist_name
    playlist_path = os.path.join(home_dir, f"{playlist_name}.m3u")
    with open(playlist_path, "w") as playlist_file:
        line_number = 1
        for line in history_lines[-num_lines:]:
            if "open" in line and ".m3u" in line:
                # Remove all the information before the single quotes and delete the single quotes
                command = line.split("'")[1]
                playlist_file.write(f"# Command: {line_number}\n")
                playlist_file.write(f"{command}\n")
                line_number += 1

    print(f"{line_number - 1} command(s) from history have been saved to {playlist_path}.")

def select_open_commands(input_file, output_file):
    with open(input_file, "r") as f_in:
        lines = f_in.readlines()

    with open(output_file + ".m3u", "w") as f_out:
        for line in reversed(lines):
            # Keep only the lines that contain the text "open" and end with ".m3u'"
            if "open '" in line and line.strip().endswith(".m3u'"):
                # Use regex to remove numbers at the beginning of the line and "open " and one space
                line_without_numbers = re.sub(r"^\d+\s*open\s+", "", line.strip())
                # Remove single quote marks from the line
                line_without_quotes = line_without_numbers.replace("'", "")
                # Write the modified line to the output file
                f_out.write(line_without_quotes + "\n")

def run_history_command():
    command = "history >> history3333.m3u"
    subprocess.run(command, shell=True)

# Call the function to execute the command
run_history_command()


def select_random_song_from_history(playlist_path):
    # Get the user's home directory
    home_dir = os.path.expanduser("~")
    history_file_path = os.path.join(home_dir, "history.m3u")

    # Read the entire history from the history file
    with open(history_file_path, "r") as history_file:
        playlist_lines = history_file.readlines()

    # Remove any lines that start with '#'
    playlist_lines = [line for line in playlist_lines if not line.startswith("#")]

    # Select a random song from the playlist
    if playlist_lines:
        random_song = random.choice(playlist_lines).strip()
        return random_song
    else:
        print("The playlist is empty.")
        return None
    
def load_history_to_m3u(history_file_path):
    # Run the bash command "history >> history.m3u"
    command = f"history >> {history_file_path}"
    subprocess.run(command, shell=True)

def select_random_song_from_history2(playlist_path):
    with open(playlist_path, "r") as playlist_file:
        playlist_lines = playlist_file.readlines()

    # Remove any lines that start with '#'
    playlist_lines = [line for line in playlist_lines if not line.startswith("#")]

    # Select a random song from the playlist
    if playlist_lines:
        random_song = random.choice(playlist_lines).strip()
        return random_song
    else:
        print("The playlist is empty.")
        return None

def extract_info_from_m3u(file_path):
    with open(file_path, "r") as m3u_file:
        content = m3u_file.read()

    # Use regular expressions to find the artist and album information
    artist_match = re.search(r"# Artist: (.+)", content)
    album_match = re.search(r"# Album: (.+)", content)

    artist = artist_match.group(1) if artist_match else None
    album = album_match.group(1) if album_match else None

    return artist, album

def game_question():
    folder_path = "/home/riley"  # Replace with the correct folder path

    # Get a list of all .m3u files in the folder
    m3u_files = [file for file in os.listdir(folder_path) if file.endswith('.m3u') and len(file) <= 28]

    total_questions = 0
    correct_answers = 0
    incorrect_answers = 0
    opted_out_questions = 0

    while True:
        # Select a random .m3u file
        file = random.choice(m3u_files)
        file_path = os.path.join(folder_path, file)
        artist, album = extract_info_from_m3u(file_path)

        print(f"File: {file}")
        print(f"Artist: {artist}")
        print(f"Album: ")
        print()
        if artist == album:
            continue
        if artist == "Music":
            print("Error parsing the song information. Skipping this question.\n")
            continue
        elif artist == "- 2":
            print("Error parsing the song information. Skipping this question.\n")
            continue
        elif artist == "New Folder (6)":
            print("Error parsing the song information. Skipping this question.\n")
            continue
        elif artist == "None":
            print("Error parsing the song information. Skipping this question.\n")
            continue
        elif artist == "untitled folder 2":
            print("Error parsing the song information. Skipping this question.\n")
            continue
        elif artist == "untitled folder":
            print("Error parsing the song information. Skipping this question.\n")
            continue
        elif artist == "untitled folder 3":
            print("Error parsing the song information. Skipping this question.\n")
        elif artist == "Unknown Artist":
            print("Error parsing the song information. Skipping this question.\n")
            continue
        elif artist == "Unknown Album":
            print("Error parsing the song information. Skipping this question.\n")
            continue
        elif artist == "Compilations":
            print("Error parsing the song information. Skipping this question.\n")
            continue
        elif artist == "Media":
            print("Error parsing the song information. Skipping this question.\n")
            continue
        elif artist == "share":
            print("Error parsing the song information. Skipping this question.\n")
            continue
        elif artist == "mom and dad stuff":
            print("Error parsing the song information. Skipping this question.\n")
            continue
        elif album == "None":
            print("Error parsing the song information. Skipping this question.\n")
            continue
        elif artist == "Music":
            print("Error parsing the song information. Skipping this question.\n")
            continue

        user_answer = input("Your answer for the album (or enter ' to opt out, or '0' to exit): ")
        if user_answer == '0':
            break

        total_questions += 1

        if user_answer == "'":
            opted_out_questions += 1
            print("Question opted out.\n")
        elif user_answer.lower() in album.lower():
            print("Correct! You guessed correctly.\n")
            correct_answers += 1
        else:
            print(f"Sorry, the correct answer is '{album}'.\n")
            incorrect_answers += 1

    print("Game Over!")
    print(f"Total Correct Answers: {correct_answers}")
    print(f"Total Incorrect Answers: {incorrect_answers}")
    print(f"Total Opted Out Questions: {opted_out_questions}")

def extract_info_from_m3u2(file_path):
    with open(file_path, "r") as m3u_file:
        content = m3u_file.read()

    # Use regular expressions to find the artist and album information
    artist_match = re.search(r"# Artist: (.+)", content)
    album_match = re.search(r"# Album: (.+)", content)

    artist = artist_match.group(1) if artist_match else None
    album = album_match.group(1) if album_match else None

    return artist, album

def clean_string(s):
    # Remove non-letter and non-number characters
    return re.sub(r'[^a-zA-Z0-9]', '', s)

def game_question2():
    folder_path = "/home/riley"  # Replace with the correct folder path

    # Get a list of all .m3u files in the folder
    m3u_files = [file for file in os.listdir(folder_path) if file.endswith('.m3u') and len(file) <= 25]

    total_questions = 0
    correct_answers = 0
    incorrect_answers = 0
    opted_out_questions = 0

    while True:
        # Select a random .m3u file
        file = random.choice(m3u_files)
        file_path = os.path.join(folder_path, file)
        artist, album = extract_info_from_m3u(file_path)

        print(f"File: {file}")
        print(f"Artist: ")
        print(f"Album: {album}")
        print()
        if artist == album:
            continue
        if album == "None":
            print("Error parsing the song information. Skipping this question.\n")
            continue
        elif artist == "- 2":
            print("Error parsing the song information. Skipping this question.\n")
            continue
        elif artist == "New Folder (6)":
            print("Error parsing the song information. Skipping this question.\n")
            continue
        elif album == "None":
            print("Error parsing the song information. Skipping this question.\n")
            continue
        elif artist == "untitled folder 2":
            print("Error parsing the song information. Skipping this question.\n")
            continue
        elif artist == "untitled folder":
            print("Error parsing the song information. Skipping this question.\n")
            continue
        elif artist == "untitled folder 3":
            print("Error parsing the song information. Skipping this question.\n")
        elif artist == "Unknown Artist":
            print("Error parsing the song information. Skipping this question.\n")
            continue
        elif artist == "Unknown Album":
            print("Error parsing the song information. Skipping this question.\n")
            continue
        elif artist == "Compilations":
            print("Error parsing the song information. Skipping this question.\n")
            continue
        elif album == "Media":
            print("Error parsing the song information. Skipping this question.\n")
            continue
        elif artist == "share":
            print("Error parsing the song information. Skipping this question.\n")
            continue
        elif artist == "mom and dad stuff":
            print("Error parsing the song information. Skipping this question.\n")
            continue
        elif album == "None":
            print("Error parsing the song information. Skipping this question.\n")
            continue
        elif artist == "Music":
            print("Error parsing the song information. Skipping this question.\n")
            continue

        user_answer = input("Your answer for the artist (or enter ' to opt out, or '0' to exit): ")
        if user_answer == '0':
            break

        total_questions += 1

        if user_answer == "'":
            opted_out_questions += 1
            print("Question opted out.\n")
        elif user_answer.lower() in artist.lower():
            print("Correct! You guessed correctly.\n")
            correct_answers += 1
        else:
            print(f"Sorry, the correct answer is '{album}'.\n")
            incorrect_answers += 1

    print("Game Over!")
    print(f"Total Correct Answers: {correct_answers}")
    print(f"Total Incorrect Answers: {incorrect_answers}")
    print(f"Total Opted Out Questions: {opted_out_questions}")

def write_history_to_playlist(output_file):
    with open(output_file, "a") as f_out:
        subprocess.run(["bash", "-c", "history"], stdout=f_out)

# Call the function with the desired output file name


# Call the function with the desired output file name




def select_open_commands(input_file, output_file):
    with open(input_file, "r") as f_in:
        lines = f_in.readlines()

    with open(output_file + ".m3u", "w") as f_out:
        for line in reversed(lines):
            # Keep only the lines that contain the text "open" and end with ".m3u'"
            if "vlc '" in line and line.strip().endswith(".m3u'"):
                # Use regex to remove numbers at the beginning of the line and "open " and one space
                line_without_numbers = re.sub(r"^\d+\s*vlc\s+", "", line.strip())
                # Remove single quote marks from the line
                line_without_quotes = line_without_numbers.replace("'", "")
                # Remove the ".m3u" extension from the line
                line_without_extension = re.sub(r"\.m3u", "", line_without_quotes)
                # Write the modified line to the output file
                f_out.write(line_without_extension + "\n")


def load_history_to_m3u(output_file):
    try:
        result = subprocess.run('history', capture_output=True, text=True, shell=True)
        history_lines = result.stdout.splitlines()
        with open(output_file, 'w') as f_out:
            for line in history_lines:
                f_out.write(line + '\n')
        print("History successfully loaded to the .m3u file.")
    except Exception as e:
        print(f"Error: {e}")


# Call the function to execute the writing of history to history3333.m3u file

    
if __name__ == "__main__":
    existing_entries = set()
    while True:
        print("1. type zx before any title to play any playlist")
        print("2. type qw to append any playlist")
        print("3. type . and a number to go back a number of tracks")
        print("4. type a number to go forward a number of tracks")
        print("5. type .. to play a random song")
        print("5. type ww to play the listening to a random song game")
        print("6. type xx for playlist game")
        print("7. type zz for other playlist game")
        try:
                    choice = input("Enter your choice: ")
                    if "qw" in choice:
                        clean_choice2 = choice.replace("qw", "").strip()  # Remove leading/trailing spaces
                        execute_command2(choice)
                        
                        # Check if the cleaned choice is an existing .m3u file in the directory
                        playlist_path = os.path.join("/home/riley", f"{clean_choice2}.m3u")
                        if os.path.exists(playlist_path):
                            vlc_enqueue_playlist(clean_choice2)
                            
                            with open("history3333.m3u", "a+") as file:
                                file.seek(0)
                                existing_entries.update(file.read().splitlines())
                                
                                if clean_choice2 not in existing_entries:
                                    file.write(clean_choice2 + "\n")
                                    existing_entries.add(clean_choice2)
                                    print("Input written to history3333.m3u")
                                else:
                                    print("Duplicate entry. Skipping.")
                        else:
                            print(f"'{clean_choice2}.m3u' does not exist in the directory.")
                    else:
                        print("Invalid input. Please enter a valid choice.")

                    if "zx" in choice:
                        clean_choice2 = choice.replace("zx", "").strip()  # Remove leading/trailing spaces
                        execute_command(clean_choice2)
                        
                        # Check if the cleaned choice is an existing .m3u file in the directory
                        playlist_path = os.path.join("/home/riley", f"{clean_choice2}.m3u")
                        if os.path.exists(playlist_path):
                            with open("history3333.m3u", "a+") as file:
                                file.seek(0)
                                existing_entries.update(file.read().splitlines())
                                
                                if clean_choice2 not in existing_entries:
                                    file.write(clean_choice2 + "\n")
                                    existing_entries.add(clean_choice2)
                                    print("Input written to history3333.m3u")
                                else:
                                    print("Duplicate entry. Skipping.")
                        else:
                            print(f"'{clean_choice2}.m3u' does not exist in the directory.")
                    else:
                        print("Invalid input. Please enter a valid choice.")
                    if "qq" in choice:
                        output_file = "history3333.m3u"
                        try:
                            history_playlist_path = os.path.join(os.path.expanduser("~"), "history3333.m3u")
                            random_song = select_random_song_from_history2(history_playlist_path)
                            if random_song:
                                print(f"Random song selected: {random_song}")
                                    # Run the bash command "open '{random_song}.m3u'"
                                command = f"open '{random_song}.m3u'"
                                subprocess.run(command, shell=True)
                        except ValueError:
                            print("Invalid input. Please enter a valid number.")
                    if ".." in choice:
                        output_file = "history3333.m3u"
                        try:
                            history_playlist_path = os.path.join(os.path.expanduser("~"), "history3333.m3u")
                            random_song = select_random_song_from_history2(history_playlist_path)
                            if random_song:
                                print(f"Random song selected: {random_song}")
                                    # Run the bash command "open '{random_song}.m3u'"
                                command = f"open '{random_song}.m3u'"
                                subprocess.run(command, shell=True)
                        except ValueError:
                            print("Invalid input. Please enter a valid number.")
            # Add "open '" to the beginning and ".m3u' to the end of the cleaned command
            # Remove "zx" from the command
            # Add "open '" to the beginning and ".m3u' to the end of the cleaned command
            # Remove "zx" from the command
            # Add "open '" to the beginning and ".m3u' to the end of the cleaned 
                    if "." in choice:
                        clean_choice22 = choice.replace(".", "")
                        clean_choice22 = int(clean_choice22)
                        for i in range(clean_choice22):
                            vlc_next()
                            time.sleep(0.1)
                    if choice.isdigit() == True:
                        choice = int(choice)
                        if choice > 0:
                            for i in range(choice):
                                vlc_previous()
                                time.sleep(0.1)
                    elif choice != "d" and choice != "u" and choice != "s" and choice != "a":
                        execute_command(choice)
        # Add "open '" to the beginning and ".m3u' to the end of the cleaned command
        # Remove "zx" from the command
        # Add "open '" to the beginning and ".m3u' to the end of the cleaned command
        # Remove "zx" from the command
        # Add "open '" to the beginning and ".m3u' to the end of the cleaned
                    if choice == "skip":
                        vlc_next()
                    if choice == ";;;":
                        output_file = "history3333.m3u"
                        load_history_to_m3u(output_file)
                    elif choice == ";;":
                        input_file = "history3333.m3u"
                        output_file = input("Enter history3333: ")

                        select_open_commands(input_file, output_file)

                        while True:
                            num_songs = input("Enter the number of random songs to play (type '0' to stop): ")
                            if num_songs == "0":
                                break
                            try:
                                history_playlist_path = os.path.join(os.path.expanduser("~"), "history3333.m3u")
                                random_song = select_random_song_from_history2(history_playlist_path)
                                if random_song:
                                    print(f"Random song selected: {random_song}")
                                    # Run the bash command "open '{random_song}.m3u'"
                                    command = f"open '{random_song}.m3u'"
                                    subprocess.run(command, shell=True)
                            except ValueError:
                                print("Invalid input. Please enter a valid number.")
                    elif choice == "--":
                        vlc_pause()
                    elif choice == "==":
                        vlc_play()
                    elif choice == "s":
                        vlc_next()
                    elif choice == "next":
                        vlc_next()
                    elif choice == "last":
                        vlc_previous()
                    elif choice == "a":
                        vlc_previous()
                    elif choice == "back":
                        vlc_previous()
                    elif choice == "1/":
                        change_volume(1)
                    elif choice == "2/":
                        change_volume(2)
                    elif choice == "3/":
                        change_volume(3)
                    elif choice == "4/":
                        change_volume(4)
                    elif choice == "5/":
                        change_volume(5)
                    elif choice == "6/":
                        change_volume(6)
                    elif choice == "7/":
                        change_volume(7)
                    elif choice == "8/":
                        change_volume(8)
                    elif choice == "9/":
                        change_volume(9)
                    elif choice == "10/":
                        change_volume(10)
                    elif choice == "u":
                        change_volume2()
                    elif choice == "d":
                        change_volume3()
                    elif choice == "ww":
                        # Call the listening_game function
                        listening_game()
                    elif choice == "xx":
                        # Call the listening_game function
                        game_question()
                    elif choice == "zz":
                        # Call the listening_game function
                        game_question2()
        except ValueError:
            print("Invalid input. Please enter a valid number.")
            # Remove "zx" from the command
            
            # Add "open '" to the beginning and ".m3u' to the end of the cleaned command
            # Remove "zx" from the command
            # Add "open '" to the beginning and ".m3u' to the end of the cleaned command
            # Remove "zx" from the command
            # Add "open '" to the beginning and ".m3u' to the end of the cleaned c


            
            # Execute the command using the custom function to track executed commands
