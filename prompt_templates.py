import os

# Get the directory of this Python file
directory = os.path.dirname(os.path.abspath(__file__))

# Add 'prompt_templates' to the directory path
directory = os.path.join(directory, "prompt_templates")


# Recursively map the directory structure
def map_directory(path):
    dir_dict = {}
    for name in os.listdir(path):
        full_path = os.path.join(path, name)
        if os.path.isdir(full_path):
            dir_dict[name] = map_directory(full_path)
        elif os.path.isfile(full_path) and name.endswith(".md"):
            with open(full_path, "r") as file:
                content = file.read()
            dir_dict[name[:-3]] = content  # Remove '.md' from the name
    return dir_dict


# Save structure to a variable
prompt_templates = map_directory(directory)
