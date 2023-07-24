from flask import Flask, request
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

app = Flask(__name__)

# Define the input variables
oxygen_rate = ctrl.Antecedent(np.arange(0, 100, 1), 'oxygen_rate')
heart_rate = ctrl.Antecedent(np.arange(0, 160, 1), 'heart_rate')

# Define the output variable
hypoxia = ctrl.Consequent(np.arange(0, 160, 1), 'hypoxia')

# Define the fuzzy sets for each input and output variable
oxygen_rate ['severe_oxygen'] = fuzz.trimf(oxygen_rate.universe, [0, 85, 86])
oxygen_rate ['moderate_oxygen'] = fuzz.trapmf(oxygen_rate.universe, [85, 86, 90, 91])
oxygen_rate ['mild_oxygen'] = fuzz.trapmf(oxygen_rate.universe, [90, 91, 94, 95])
oxygen_rate ['normal_oxygen'] = fuzz.trimf(oxygen_rate.universe, [94, 95, 100])

# Membership functions for heart rate
heart_rate ['bradycardia'] = fuzz.trimf(heart_rate.universe, [0, 60, 80])
heart_rate ['normal_heart_rate'] = fuzz.trimf(heart_rate.universe, [60, 80, 100])
heart_rate ['tachycardia'] = fuzz.trimf(heart_rate.universe, [80, 100, 160])

hypoxia ['severe_hypoxia'] = fuzz.trimf(hypoxia.universe, [0, 30, 65])
hypoxia ['moderate_hypoxia']= fuzz.trimf(hypoxia.universe, [20, 50, 80])
hypoxia ['mild_hypoxia'] = fuzz.trimf(hypoxia.universe, [80, 100, 100])
hypoxia ['normal'] = fuzz.trimf(hypoxia.universe, [90, 100, 100])

# Define the rules for the fuzzy logic system
rule1 = ctrl.Rule(heart_rate['bradycardia'] & oxygen_rate['severe_oxygen'], hypoxia['severe_hypoxia'])
rule2 = ctrl.Rule(heart_rate['bradycardia'] & oxygen_rate['moderate_oxygen'], hypoxia['moderate_hypoxia'])
rule3 = ctrl.Rule(heart_rate['bradycardia'] & oxygen_rate['mild_oxygen'], hypoxia['mild_hypoxia'])
rule4 = ctrl.Rule(heart_rate['bradycardia'] & oxygen_rate['normal_oxygen'], hypoxia['normal'])

rule5 = ctrl.Rule(heart_rate['normal_heart_rate'] & oxygen_rate['severe_oxygen'], hypoxia['severe_hypoxia'])
rule6 = ctrl.Rule(heart_rate['normal_heart_rate'] & oxygen_rate['moderate_oxygen'], hypoxia['moderate_hypoxia'])
rule7 = ctrl.Rule(heart_rate['normal_heart_rate'] & oxygen_rate['mild_oxygen'], hypoxia['mild_hypoxia'])
rule8 = ctrl.Rule(heart_rate['normal_heart_rate'] & oxygen_rate['normal_oxygen'], hypoxia['normal'])

rule9 = ctrl.Rule(heart_rate['tachycardia'] & oxygen_rate['severe_oxygen'], hypoxia['severe_hypoxia'])
rule10 = ctrl.Rule(heart_rate['tachycardia'] & oxygen_rate['moderate_oxygen'], hypoxia['severe_hypoxia'])
rule11 = ctrl.Rule(heart_rate['tachycardia'] & oxygen_rate['mild_oxygen'], hypoxia['moderate_hypoxia'])
rule12 = ctrl.Rule(heart_rate['tachycardia'] & oxygen_rate['normal_oxygen'], hypoxia['mild_hypoxia'])

# Create the control system and pass the rules to it
hypoxia_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10, rule11, rule12])

# Create the simulation using the control system
hypoxia_sim = ctrl.ControlSystemSimulation(hypoxia_ctrl)

def calculate_hypoxia():
    # Get the input values from the request
    data = request.get_json()
    oxygen = data['oxygen']
    heart = data['heart']

    # Set the input values
    hypoxia_sim.input['oxygen_rate'] = oxygen
    hypoxia_sim.input['heart_rate'] = heart

    # Evaluate the output value
    hypoxia_sim.compute()

    # Get the output value
    hypoxia_level = hypoxia_sim.output['hypoxia']

    #kategory
    category = 'Not Detected'
    # if(oxygen > 91 and heart > 101) :
    #     category = 'Tachycardia'
    # elif(oxygen > 91 and heart < 60) :
    #     category = 'Bradycardia'   
    # elif(oxygen > 91 and heart < 100 ) :
    #     category = 'Normal'   
    # elif(oxygen < 90 and heart > 101) :
    #     category = 'Mild Hypoxia'   
    # elif(oxygen < 90 and heart < 60) :
    #     category = 'Mild Hypoxia'   
    # elif(oxygen < 90 and heart < 100) :
    #     category = 'Mild Hypoxia'   
    # elif(oxygen < 80 and heart > 101) :
    #     category = 'Moderate Hypoxia'   
    # elif(oxygen < 80 and heart < 60) :
    #     category = 'Moderate Hypoxia'   
    # elif(oxygen < 80 and heart < 100) :
    #     category = 'Moderate Hypoxia'
    # elif(oxygen < 65 and heart > 101) :
    #     category = 'Severe Hypoxia'   
    # elif(oxygen < 65 and heart < 60) :
    #     category = 'Severe Hypoxia'   
    # elif(oxygen < 65 and heart < 100) :
    #     category = 'Severe Hypoxia'   
    # else:
    #     category = 'Not Detected'
        
    if(hypoxia_level > 90 and hypoxia_level <= 100) :
        category = 'Normal'
    elif(hypoxia_level > 80 and hypoxia_level <= 90) :
        category = 'Mild Hypoxia'   
    elif(hypoxia_level > 65 and hypoxia_level <= 80) :
        category = 'Moderate Hypoxia'   
    elif(hypoxia_level <= 65) :
        category = 'Severe Hypoxia'   
    else:
        category = 'Not Detected'
    # Return the output value as a JSON response
    return {'hypoxia': hypoxia_level, 'category' : category}

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)