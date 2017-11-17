# IBMCloud_GitLab_CSV
A quick python utility demonstrating how to extract issues to a CSV from the IBM Cloud GitHub

## Description
Users have asked for a way to export the GitHub data from their projects hosted on IBM Cloud to a CSV file.  This sample Python code shows how to export issues to a CSV file.

As currently written, the resulting CSV file will capture the following information from all issues associated with a particular project:
- Issue number
- Issue state
- Any labels associated with the issue
- Issue title
- Issue owner
- Issue description

## The Code
This was written (and somewhat tested) using Python 2.7.  You will also need to have the Python sys, unicodecsv (https://github.com/jdunck/python-unicodecsv) and gitlab (https://github.com/python-gitlab/python-gitlab) packages installed.  These can be installed with a simple pip command.

`pip install unicodecsv`

`pip install python-gitlab`

(Note: You should already have sys as part of your Python installation.)

Anyone using this will need to change the GITHUB_USERID, GITHUB_TOKEN, and GITHUB_REPO constants at the top of this code.

GITHUB_USERID - this is the name of the user who "owns" the project on GitHub.
GITHUB_REPO - this is the name of the project.  So when you look at the GitHub project, you typically see it as "user/project".
GITHUB_TOKEN - this is the access token for the project.  More on getting that is below.

This is meant as an example of what can be done.  I anticipate people will use this as a starting point for their own integrations with the GitHub repositories on the IBM Cloud.  I can easily see this being used in a number of different ways.

- to export issues to a spreadsheet for Agile teams who need to report to more traditional project management functions.
- to build live dashboards showing project health trends over time for projects hosted on IBM Cloud.
- to communicate selected development milestones and issues to business stakeholders.

## Getting your GitHub token on IBM Cloud

Getting an access token for your GitHub repositories on IBM Cloud is easy.

1. Log into the IBM Cloud, and navigate to your GitHub home (https://git.ng.bluemix.net/).
1. In the upper right hand corner of the screen, click on your picture or avatar, and select "Settings" from the drop down menu.
1. On the left hand nav bar of the Settings screen, select "Access Tokens"
1. Now create a new token with API access, and copy the contents of the token somewhere.  This is the character string that you will insert into the GITHUB_TOKEN constant.

A quick note on access tokens.  For security reasons, it is suggested that you periodically destroy tokens and re-create them (commonly called rotating your access tokens).  Then if someone had access to your data by having one of your tokens, they will lose this access.
