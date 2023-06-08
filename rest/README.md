# Powerplant-coding-challenge
## Installation
First you will need to install all needed dependencies (here fastapi used for the REST API and uvicorn to run the app) <br />
You have to make: pip install -r requirements.txt <br />
<br />
## Run the main.py with uvicorn 
Then to run the program you will have to type: <br />
uvicorn main:app --port=8888 <br />
The prompt ask you to enter a file that you want to analyse, just type the .json file <br />
Then it will ask you to enter the file where you want to output the result <br />
Then go to http://127.0.0.1:8888/docs to see the endpoint /productionplan and then execute the POST method. <br />
Yout file mentionned above is now full with the analysis
<br />
## Run the main.py with docker
First you will have to install docker by your own (https://docs.docker.com/engine/install/ubuntu/) <br />
In the folder named **rest** type:  <br />
*docker image build --tag powerplant_coding_challenge .* (don't forget the point at the end to locate the Dockfile) <br />
Then when everything is setup type: <br />
*docker run -it --publish 8888:8888 --name engie_challenge powerplant_coding_challenge* <br />
As before you have to mention a file to analyse and a file to display the result of the analysis <br />
You can now connect either on localhost:8888 or on 127.0.0.1:8888
## Few explanations
For the merit order i saw that it is a way of ranking available sources of energy, especially electrical generation, based on ascending order of price so i calculated this to rank all the powerplants. <br />
Then it is said that the cost of generating power using windmills however is zero, so for me it means that we have to switch on windmills first because it is free so it will lower the consumption of fuels used to generate the load. <br />
When I have my list ranked with the merit order i just loop through it and use the pmax until we reach the load.<br />
## Example
I need to generate 480MW in one hour and after my rank i have: <br />
["windpark2",0,36,21.6],["windpark1",0,150,90],["gasfiredsomewhatsmaller",40,210,4.96],["gasfiredbig1",100,460,7.1],["gasfiredbig2",100,460,7.1],["tj1",0,16,15.24] <br />
['name_powerplant",pmin,pmax,meritorder] <br />
pmin and pmax are the power that we can use in a powerplant (pmin = switch on and we let it in the minimum and pmax = switch on and boost to max use) <br />
<br />
I first switch on the windpark2 to get 36MW, there is still 480 - 36 = 444Mw so i continue:<br />
- windpark2 switch on to have 150MW there is still 444 - 150 = 294MW <br />
- gasfiredsomewhatsmaller switch on to have 210MW there is still 294 - 210 = 84MW <br />
<br />
Now we can see that the next powerplant can generate between 100 and 460MW and we need only 84MW so for the last one we use pmin and we will generate all the load needed. <br />
<br />
I decided to do that because i saw Belgium grid operator: <br />


![grid](https://github.com/SamyBO98/powerplant-coding-challenge/assets/90256223/2a8d9da5-560e-4079-beca-4340fa466bb2)  <br />
 
 As you can see the orange curve is the load predicted (here in our example 480MWh) and the blue one is the actual load created by all the powerplants. So, it is quite normal that instead of having 480MW we have here in my case a little bit more.


