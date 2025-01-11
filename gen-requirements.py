import os
import shutil
from pathlib import Path

root_dir = os.getcwd()
temp_dir = os.path.join(root_dir, "temp")

# Clear or create the temporary directory
if os.path.exists(temp_dir):
    shutil.rmtree(temp_dir)
os.makedirs(temp_dir)

# Copy all .py files to the temp directory recursively
for root, _, files in os.walk(root_dir):
    for file in files:
        if file.endswith(".py"):
            src_file = os.path.join(root, file)
            dest_file = os.path.join(temp_dir, Path(root).name + "_" + file)
            shutil.copyfile(src_file, dest_file)

# Run pipreqs on the temporary directory
os.system(f"pipreqs {temp_dir} --force")

# Move the generated requirements.txt to the original root directory
shutil.move(os.path.join(temp_dir, "requirements.txt"), os.path.join(root_dir, "requirements.txt"))

# Clean up the temporary directory
shutil.rmtree(temp_dir)

print("requirements.txt has been generated!")
