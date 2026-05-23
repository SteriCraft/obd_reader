# TODO LIST
## Record dialog
- Ask the user to confirm recording deletion
- Recordings must be saved on disk somewhere (and files removed when the recording is deleted)
- Add a horizontal scrollbar on graphs, to see more than 30 seconds of data (except when recording)
- Matplotlib issue may require a check, given that on linux this may not be an issue

## Connection
- Catch "Failed to set baudrate" to enrich the information label ("Invalid baudrate")
- Catch "Failed to read port" to enrich the information label ("Unable to reach port "<port>"")
- Catch "ATE0 did not return 'OK'" to enrigh the information label ("Car response invalid")

## General
- Move TODO list to a specific *.md file
- Right a proper README file with details on installing the software on Linux and Windows
- Add details on installing ELM327-emulator in the README

# BUGS
- x_data is not updated properly when recording selection changes (on graph 2 only it seems)
- Units have vanished from the Y axis on graphs (when showing recorded graph, not on record)
- On Windows (check linux), showing a recorded graph shows all 4 lines instead of just recorded PIDs'