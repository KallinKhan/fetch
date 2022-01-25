First, the latest version of python must be downloaded an installed. This can be done by following the instructions at: 
https://www.python.org/downloads/
In development I used python 3.10.2.

Once python is installed, add it to the system path using the instructions here: 
https://www.tutorialspoint.com/python/python_environment.htm

Now create a new directory called 'project', cd into the directory with the command "cd project", and add the code from
GitHub either by downloading a ZIP and unzipping here or, if you have git installed, run the command 
"git clone https://github.com/KallinKhan/fetch.git"

Now run the command "cd fetch" to go into the project directory. Next, run the command 
"python -m pip install -r requirements.txt"

Once the requirements are installed, run the command "python -m pytest tests". If all the tests pass, the tool has been
set up correctly. The API can now be run with the command "python run.py"