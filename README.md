# A Python Service Task for Camunda

This is an example of spawning a python script from a JavaScript service worker for Python.
The python code creates a prediction model for risk assessment for a loan.

## What's included

Included in this project is the following:
* A BPMN Model using a manual task to verify risk
* A BPMN Model that replaces the manual task with the python script and JavaScript
* Forms for the models (the models share the forms)
* Python code to predict the risk
* JavaScript to spawn the python code for risk assessment
* A small application (HTML and python) to call the risk assessment from an HTML form for the manual Verify Risk step

