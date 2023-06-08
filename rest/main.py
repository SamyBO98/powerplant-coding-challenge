# Imports
from fastapi import FastAPI ,HTTPException
import json
import sys

# File input and result output 
file_input = ''
res_output = ''
while file_input == '':
    file_input = input("Please enter the file you want to analyse: ")


# API Start
app = FastAPI()

# Open the file that we want to analyse 
try:
    with open(str(file_input), 'r') as f:
        file_ = json.load(f)
        fuel = file_['fuels']
        powerplants = file_['powerplants']
except:
    print('File to analyse does not exist')
    sys.exit(1)


while res_output == '':
    res_output = input("Please enter the file to display the result: ")

# Message in root to find all functions
@app.get("/")
async def root():
    return {"message": "Root, you can go to /docs to find all functions"}


# POST method on /productionplan endpoint
# You can access all endpoints by typing http://127.0.0.1:8888/docs
# We will store our final_dictionnary into a file provided by the 2nd argument in our command
@app.post('/productionplan')
def prod_plan(fi = res_output):
    # PowerPlant + Turbojet list
    pp = []
    # WindTurbine list
    wind = []
    # Loop through all powerplants
    # The merit order is a way of ranking available sources of energy, especially electrical generation, based on ascending order of price.
    # We calculate foreach powerplants the price (efficiency * price of fuel)
    # However the cost of generating power using windmills is zero so we have to switch on them first that's why we have 2 lists (pp and wind).
    for i in range(0,len(powerplants)):
        if(powerplants[i]['type'] == 'gasfired'):
            res = round(powerplants[i]['efficiency'] * fuel['gas(euro/MWh)'],2)
            pp.append((powerplants[i]['name'],powerplants[i]['pmin'],powerplants[i]['pmax'],res))
        elif(powerplants[i]['type'] == 'turbojet'):
            res = round(powerplants[i]['efficiency'] * fuel['kerosine(euro/MWh)'],2)
            pp.append((powerplants[i]['name'],powerplants[i]['pmin'],powerplants[i]['pmax'],res))
        elif(powerplants[i]['type'] == 'windturbine'):
            res = round((powerplants[i]['pmax'])* (fuel['wind(%)']/100),2)
            wind.insert(0,[powerplants[i]['name'],powerplants[i]['pmin'],powerplants[i]['pmax'],res])
        else:
            return HTTPException(status_code=404, detail='Document json not correct')

    
    # We sort them by the price
    pp.sort(key = lambda x: x[3])
    wind.sort(key = lambda x: x[3])

    # We concatenate the 2 lists to have the best windturbine first and then the best powerplants (gasfired and turbojet)
    all_pp = wind+pp

    final_dict = []
    # Get the load that need to be generated during one hour
    last = file_['load']

    # We loop through our sorted list (all_pp)
    # We switch on as long as we need to reach the load needed (pmax of the turbines)
    for i in range(0,len(all_pp)):
        if(last-all_pp[i][2] > 0):
            final_dict.append({'name': all_pp[i][0], 'p': all_pp[i][2]})
            last-=all_pp[i][2]
        # For the last turbine we switch on and put it on the min (pmin) to reach the load or a bit higher.
        else:
            try:
                final_dict.append({'name': all_pp[i][0], 'p': all_pp[i][1]})
                break
            except:
                raise HTTPException(status_code=404)

    # We store it in a json
    if(len(final_dict) > 0):
        with open(fi , 'w') as f:
            json.dump(final_dict,f)    

        return final_dict
    else:
        return HTTPException(status_code=404)



