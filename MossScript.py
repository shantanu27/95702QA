import logging

import mosspy
import zipfile
import re
import os
import shutil

from io import BytesIO
from zipfile import BadZipFile

# Obtain your own free user id
# To obtain a Moss account, send a mail message to moss@moss.stanford.edu. The body of the message should appear exactly as follows:
# registeruser 
# mail username@domain
userid = 411763981


def execute(submission, basefiles=None, task=None):
    """
    This method is the main driver function. It does the following steps:
    1. Extracts code files from submission zip file. Currently, it works for java files.
    2. Adds basefiles if specified
    3. Sends the folders to moss server
    4. Once report is generated, provides the url and also downloads it locally
    5. Once everything is complete (or if there's an error in between), it cleans
       all the temporary folders that were created.
    :param submission: Name of the submission zip file
    :param basefiles: Base files, if any
    :param task: Name of the task. If nothing specified, it extracts all java files. 
    :return:
    """
    dir_list = list()
    try:
        print("Extracting code files from submissions")

        dir_list = extract_code_files(submission, task)

        # Execute mos
        # m = mosspy.Moss(userid, "java")
        # m.setDirectoryMode(mode=1)

        # print("\nSetting MOSS parameters")

        # if basefiles is not None:
           #  for file in basefiles:
           #      m.addBaseFile(file)

        # m.addFilesByWildcard("submissions/*/*")

        # print("Sending to MOSS server")
        # print("Waiting for response from MOSS server")

        # url = m.send()
        # print("Report URL: {}".format(url))

        # print("Result received. Saving to {}".format("report_{}.html".format(task)))
        # m.saveWebPage(url, "report_{}.html".format(task))

        # report_dir = "report_{}".format(task)

        # if os.path.isdir(report_dir):
        #     shutil.rmtree(report_dir)

        # print("Downloading whole report locally for {}".format(task))
        # mosspy.download_report(url, "report_{}/".format(task), connections=8, log_level=logging.ERROR)

        # print("\nDeleting directories")
        # # Delete created files
        # for directory in dir_list:
        #     if os.path.isdir(directory):
        #         shutil.rmtree(directory)

        # print("Finished")
    except BaseException as e:
        print("Exception thrown! {}".format(str(e)))
        print("Deleting dirs")

        # In case of any exception, delete the temporary directories which might have been created
        for directory in dir_list:
            if os.path.isdir(directory):
                shutil.rmtree(directory)


def extract_code_files(submission_zip_path, task=None):
    """
    This function prepares the directory structure needed for moss.
    For project submissions on Canvas, it typically downloads as a single zip - submissions.zip
    with the following structure

    submissions.zip
        - <andrewid1_somecode>.zip
        - <andrewid2_somecode>.zip
        .
        .. and so on

    The method goes through each of those zipped submissions and prepares the folder structure
    inside the extract_zip method. The final folder structure is:

    submissions
        - andrewid1
            - file1.java
            - file2.java
            ....
        - andrewid2
            - file1.java
            - file2.java
            ....
        ....

    :param submission_zip_path:
    :param task: name of the task to extract. If none, then extract all java files
    :return: Returns the list of directories created
    """
    dir_list = list()
    count = 0

    basepath = "submissions"

    if not os.path.isdir(basepath):
        os.makedirs(basepath)

    # Try opening the submissions zip
    try:
        with zipfile.ZipFile(submission_zip_path, 'r') as zip_ref:
            # The submission zip in turn contains individual zipped submissions
            for submission in zip_ref.namelist():
                # Create directory by andrew id for each submission
                andrew_id = str(submission).split("_")[0]
                dirpath = os.path.join(basepath, andrew_id)

                print("Processing Submission: {}".format(andrew_id))

                submission_io = BytesIO(zip_ref.read(submission))
                extract_zip(submission_io, dirpath, task)
                dir_list.append(dirpath)
                count += 1
    except BadZipFile:
        # print("Bad ZipFile: {}".format(submission_zip_path))
        return

    print("\nTotal submissions processed: {}".format(count))

    return dir_list


def extract_zip(submission, output_dir, task=None):
    """
    This function keeps going recursively to extract all the java files.
    The .java files may be nested inside .zip.
    Stores the java files in the <output_dir> in a flattened structure.
    :param task: task name, if any
    :param submission: submission zip to extract 
    :param output_dir: directory to put the extracted files into
    :return:
    """
    try:
        with zipfile.ZipFile(submission, 'r') as zip_ref:
            for file in zip_ref.namelist():
                # Check for zip extension. If yes, call extract_zip again
                if re.search(r'\.zip$', file) is not None:
                    file_data = BytesIO(zip_ref.read(file))
                    extract_zip(file_data, output_dir, task)
                # Else, if it is a java file, then write it to output_dir
                elif re.search(r'\.java$', file) and (task is None or belongs_to_task(file, task)):
                    if not os.path.isdir(output_dir):
                        os.makedirs(output_dir)
                    source = zip_ref.open(file)
                    target = open(os.path.join(output_dir, os.path.basename(file)), "wb")
                    with source, target:
                        shutil.copyfileobj(source, target)
    except BadZipFile:
        # print("Bad ZipFile")
        return


def belongs_to_task(file, task):
    path_split = os.path.normpath(file).split(os.sep)
    return path_split[0].lower() in task.lower()


if __name__ == "__main__":
    # basefiles = ["InterestingPicture/InterestingPictureModel.java",
    #              "InterestingPicture/InterestingPictureServlet.java",
    #              "InterestingPicture/sslfetch.java"]

    submissionfile = "submissions.zip"
    taskname = "Project2Task1"

    # execute(submission=submissionfile, basefiles=basefiles, task=taskname)
    execute(submission=submissionfile, task=taskname)

