# A Python Service Task for Camunda

This is an example of spawning a python script from a JavaScript service worker for Python.
The python code creates a prediction model for risk assessment for a loan.

## What's included

Included in this project is the following:
* A BPMN Model using a manual task to verify risk
* A BPMN Model that replaces the manual task with the python script and JavaScript
* DMN for BPMN models
* Forms for the models (the models share the forms)
* Python code to predict the risk
* A CSV file to access 
* JavaScript to spawn the python code for risk assessment
* A small application (HTML and python) to call the risk assessment from an HTML form for the manual Verify Risk step
* creditLookup.json file to be used to look at financial information used to run the python prediction model
* A document that plays the role of the Google Doc template that is used to generate the "loan documentation".

### Notes

You will need to modify the code to match locations for files and other code used in the application.
You will need to create a REST service (or other connector) to look up the financial information by applicant ID. This is current set to use a mock API request.
You will need to run the app.py code so that you can launch http://170.0.0.1:5000 to run the python script from the HTML form.
You may want to update the Google document steps or remove this part of the workflow.
You may want to remove the email (SendGrid) connector from the workflow.

## See the blog

To see how this works and what to expect, please read the blog (PUT LINK HERE).
