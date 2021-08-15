import os, sys

# Determine the command which was originally used
command = "cd engine && " # Append a `change directory` to the original command
for arg in sys.argv:
    command += arg + " "

# Execute that same command in the 'engine' folder
print("Redirecting compilation to Godot ...")
os.system(command)
