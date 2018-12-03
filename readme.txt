# Upgrade pip
python -m pip install --upgrade pip

# Create a virtual environment in the current directory:
python -m venv venv

# Activate the virtual environment:
# On Mac/Linux:
source venv/bin/activate
# On Windows:
call venv\scripts\activate.bat

# The remainder of the tutorial assumes that the virtual environment is active.
# Install the required libraries (most notably, fbs and PyQt5):
pip install fbs PyQt5==5.9.2 PyInstaller==3.4

# Execute the following command to start a new fbs project (ме мюдн. сфе ядекюмн):
fbs startproject

# To run the basic PyQt application from source, execute the following command:
fbs run