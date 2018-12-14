# MOSS for Distributed Systems for ISM (95-702)
#### Shantanu Mukherjee

This document outlines the steps to setup moss on your machine and running moss against the submissions per project. The script is written using the Python wrapper for moss - [MossPy](https://github.com/soachishti/moss.py)
Script File – MossScript.py
The script is documented, and it explains the steps it performs. Feel free to modify the script if requirements change. It works in both Windows and Mac environments.

### Installing dependencies
The script uses some python libraries like mosspy, zipfile etc. If it throws errors saying dependencies not found, then you'll need to install those depencies using `pip` or `pip3` (the code is written in Python 3)
So for example - to install `mosspy`, use the command
```
pip3 install mosspy
```

### Obtaining MOSS user id
The script uses a user id for running the script. 
To obtain a Moss account, send a mail message to moss@moss.stanford.edu. The body of the message should appear exactly as follows:
```
registeruser 
mail username@domain
```

You'll soon receive a mail which will have the userid. Replace the userid in code with the new userid.

### Running the script
1. Download the submissions for a project from Canvas. It downloads as `submissions.zip`.
2. Place the `submissions.zip` file in the same folder as the `MossScript.py` file.
3. You'll need to modify the script based on the project and task you are running it for. Normally, you'd run the script for each task in the project separately, and run once for all the tasks combined. The only parameters that need to be changed are in the `main` method.
    1. Suppose you are running the script for `Project2Task1`. Change the `taskname` variable to `Project2Task1`.
    2. If there are some code files which have been provided by the professor to everyone, we don't want to match those parts of the code. Put those files in the `basefiles` array. 
4. To run the script
```
python3 MossScript.py
```
The script will extract all the submissions, send them to MOSS, get the results back, print the url, and download the report locally. The script takes around 5 mins to run. It is recommended to use the generated url for inspecting the matches, rather than the local report as links don't work perfectly in the local report. 


**Note:** 
The url remains active only for **7 days**, after which you'll have to run the script again. 
Also, weirdly, the script runs well in the morning or afternoon, but it times out in the evening. I don't know, ask the people who implemented the MOSS server, or just run it in the morning. 
