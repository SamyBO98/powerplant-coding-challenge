# Powerplant-coding-challenge
## Installation
First you will need to install all needed dependencies (here fastapi used for the REST API and uvicorn to run the app) <br />
You have to make: pip install -r requirements.txt <br />
<br />
## Run the main.py
Then to run the program you will have to type: <br />
python3 main.py file_to_analyse.json file_to_display.json <br />
<br />
## Few explanations
For the merit order i saw that it is a way of ranking available sources of energy, especially electrical generation, based on ascending order of price so i calculated this to rank all the powerplants. <br />
Then it is said that the cost of generating power using windmills however is zero, so for me it means that we have to switch on windmills first because it is free so it will lower the consumption of fuels used to generate the load. <br />
When I have my list ranked with the merit order i just loop through it and use the pmax until we reach the load.<br />
## Example
I need to generate 480MW in one hour and after my rank i have: <br />
["windpark2",0,36,21.6],["windpark1",0,150,90],["gasfiredsomewhatsmaller",40,210,4.96],["gasfiredbig1",100,460,7.1],["gasfiredbig2",100,460,7.1],["tj1",0,16,15.24]
