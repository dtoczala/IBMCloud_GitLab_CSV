#!/usr/bin/python
# uses python 2.7
#
import sys
import unicodecsv as csv

# Imports for GitLab (the IBM Cloud Git repo)
import gitlab

#################################################################
#
# Setup GitHub constants
#
OUTPUT_CSV_ALL = "GitHubStatus_ALL.csv"
LOGFILE = "github.output.log"

GITHUB_BASE = 'https://git.ng.bluemix.net'
GITHUB_USERID = "jonedoe"
GITHUB_TOKEN = "abcde1fg23er4hy69d"
GITHUB_REPO = "my_cool_cloud_project"
GITHUB_PROJECT = GITHUB_USERID + "/" + GITHUB_REPO
DBLQUOTE = '"'
#
# Debug flag - will dump debug output to the logfile
#
DEBUG = False

#################################################################
#
# Check for proper version of python
#
outputLog = open(LOGFILE, "w")
req_version_major = 2
req_version_minor = 7
cur_version_major = sys.version_info.major
cur_version_minor = sys.version_info.minor
if ((cur_version_major != req_version_major) or (cur_version_minor != req_version_minor)):
    outputLog.write("This program runs with Python version " + str(req_version_major) + "." + str(req_version_minor) + ", and you are running version " + str(cur_version_major) + "." + str(cur_version_minor))
    outputLog.write(" \n\n")

#
#################################################################
#  MAIN
#################################################################
#
# Start main program
#
def main(argv):
    if len(argv) != 0:
        outputLog.write("USAGE: python export_IBMCloud_GitHub_issues.py \n\n")
    #
    # Login to IBM GitHub repo
    #
    gh = gitlab.Gitlab(GITHUB_BASE, GITHUB_TOKEN)
    #
    # grab the right project
    #
    project = gh.projects.get(GITHUB_PROJECT)
    if (DEBUG):
        dump = " Dump of repo project " + GITHUB_PROJECT + "\n\n"
        outputLog.write(dump)
        outputLog.write(str(project))
        outputLog.write("\n\n")
    #
    # Grab ALL issues
    #
    # see http://python-gitlab.readthedocs.io/en/stable/gl_objects/issues.html
    # for more details
    #
    allIssues = project.issues.list()
    #
    # Debug text out
    #
    if (DEBUG):
        outputLog.write(" Dump of ALL repo issues \n\n")
        outputLog.write(str(allIssues))
        outputLog.write("\n\n")
    #
    # Open the ouput CSV file
    #
    fileCSVall = csv.writer(open(OUTPUT_CSV_ALL, "w"))

    #################################################################
    #
    # Look at ALL Issues - dump to a CSV
    #
    outputLog.write("\n ** ALL Issues in CSV ** \n\n")
    #
    # Write CSV Header line
    #
    fileCSVall.writerow(('Id','State','Label','Title','Owner','Description'))
    #
    # Initialize issue counter
    #
    count = 0
    #
    # Loop thru and process each issue
    #
    for issue in sorted(allIssues):
        #
        # Set flags
        # (Note: I use this to filter issues - you can test for certian labels, dates, etc.)
        #
        writeGitCSV = True
        #
        # Grab the current issue
        #
        thisIssue = project.issues.get(issue.id)
        if (DEBUG):
            outputLog.write("Issue id " + str(thisIssue.iid) + "\n")
            outputLog.write(str(thisIssue))
            outputLog.write("\n")
        #
        # Get any labels
        #
        # see http://python-gitlab.readthedocs.io/en/stable/gl_objects/labels.html
        # for more details
        #
        allLabels = thisIssue.labels
        newout = ""
        #
        # Loop thru all labels
        #
        for label in allLabels:
            #
            # Grab label
            #
            thisLabel = label
            #
            # Add label to the string, append a comma and a newline if string already has something
            #
            if (newout != ""):
                newout = newout + ", \n" + str(thisLabel)
            else:
                newout = str(thisLabel)
        #
        # Save off the label string
        #
        issueLabel = newout
        #
        # Figure out the owner
        #
        # see http://python-gitlab.readthedocs.io/en/stable/gl_objects/users.html
        # for more details
        #
        thisOwner = ""
        ownedBy = thisIssue.assignee
        if (ownedBy != ""):
            ownedId = ownedBy.id
            user = gh.users.get(ownedId)
            thisOwner = user.username
        else:
            thisOwner = ""
        #
        # If a good issue, then print out a line for issue in output CSV
        #
        if (writeGitCSV):
            #
            # Clear out the output values
            #
            col_1 = ""
            col_2 = ""
            col_3 = ""
            col_4 = ""
            col_5 = ""
            col_6 = ""
            #
            # Set the Issue ID
            # (Note: I use iid here because it is the displayed ID, id is the internal ID)
            #
            try:
                col_1 = str(thisIssue.iid)
            except UnicodeDecodeError:
                errout = "ERROR - Unicode decode error on NUMBER with ISSUE " + str(thisIssue.iid) + "\n"
                print(errout)
                outputLog.write(errout)
            #
            # Set the Issue state
            #
            try:
                col_2 = str(thisIssue.state)
            except UnicodeDecodeError:
                errout = "ERROR - Unicode decode error on NUMBER with ISSUE " + str(thisIssue.state) + "\n"
                print(errout)
                outputLog.write(errout)
            #
            # Set the Issue labels
            #
            try:
                col_3 = str(issueLabel)
            except UnicodeDecodeError:
                errout = "ERROR - Unicode decode error on LABEL with ISSUE " + str(issueLabel) + "\n"
                print(errout)
                outputLog.write(errout)
            #
            # Set the Issue title
            #
            try:
                col_4 = str(thisIssue.title)
            except UnicodeDecodeError:
                errout = "ERROR - Unicode decode error on TITLE with ISSUE " + str(thisIssue.title) + "\n"
                print(errout)
                outputLog.write(errout)
            #
            # Set the Issue owner
            #
            try:
                if (thisOwner):
                    col_5 = str(thisOwner)
                else:
                    col_5 = " "
            except UnicodeDecodeError:
                errout = "ERROR - Unicode decode error on OWNER with ISSUE " + str(thisOwner) + "\n"
                print(errout)
                outputLog.write(errout)
            #
            # Set the Issue description
            #
            try:
                col_6 = str(thisIssue.description)
            except UnicodeDecodeError:
                errout = "ERROR - Unicode decode error on DESCRIPTION with ISSUE " + str(thisIssue.description) + "\n"
                print(errout)
                outputLog.write(errout)
            #
            # Dump Issue to CSV
            #
            try:
                fileCSVall.writerow([col_1, col_2, col_3, col_4, col_5, col_6])
            except UnicodeDecodeError:
                errout = "ERROR - Unicode OUTPUT error to CSV with ISSUE " + str(thisIssue.iid) + "\n"
                print(errout)
                outputLog.write(errout)
        #
        # Increment the issue counter
        #
        count = count + 1
    #
    # Print number of issues processed to logfile
    #
    outputLog.write("\n ** " + str(count) + " Issues processed in CSV ** \n\n")
    #
    # DONE WITH ALL ISSUES FILE
    #
    #################################################################
#
# Check if main
#
if __name__ == "__main__":
    main(sys.argv[1:])
