import pandas as pd
from guizero import *
from math import cos

G = 6.67408e-11

EARTH_E = 0.017 #eccentricities
MOON_E = 0.0549
theta = 0

ORBIT_STATUS = True # orbit status for turning on and off servo motor

# import orbital dataset
df = pd.read_csv("../data/sol_data.csv")

# formula = lambda a, b, theta : (((a*(1-(((a**2-b**2))/a)**(2)))/(1+(((a**2-b**2)/a)*cos(theta))))**(2)) + (a**2-b**2)-(2*(abs((a*(1-((a**2-b**2)/a**2)))/(1+(((a**2-b**2)/a)*cos(theta))))*cos(theta)))


b_calc = lambda a, e : a*((1+e)*(1-e))**(1/2) # Derive b with a known a 
formula = lambda a, b, theta : ((a**2) - ((a**2-b**2)**(1/2))**(2))/(a+((a**2-b**2)**(1/2))*(cos(theta)))
velocity = lambda g, m, r, a : (g*m*((2/r)-(1/a)))**(1/2)


app = App(title='test')

message = Text(app, text='Orbit Simulator', size=20)

def earth_preset(period=45):
    a = 18 * 2.54 / 100 #m
    a_raw = 149.60e+9 #m
    sf = a / a_raw
    b = b_calc(a, EARTH_E) #m
    earth_mass = 5.97216787e+24 #kg
    sun_mass = 1.989e+30 #kg
    distance = formula(a, b, theta) #m
    v = velocity(G, (earth_mass + sun_mass)*(sf)**(3), distance, a) #m/s
    v *= (365 * 24 * 60 * 60) / period
    w = v/distance # maybe factor in height of planet
    print(f"Distance: {distance}, Velocity: {v}, Angular Velocity: {w}")

def moon_preset(period=45):
    a = 18 * 2.54 / 100 #m
    a_raw = 384748000 #m
    sf = a / a_raw
    b = b_calc(a, MOON_E)
    moon_mass = 7.34767309e+22 #kg
    earth_mass = 5.97216787e+24 #kg
    distance = formula(a, b, theta)
    v = velocity(G, (moon_mass + earth_mass)*(sf)**(3), distance, a) #m/s
    v *= (24 * 60 * 60) / period
    w = v/distance
    print(f"Distance: {distance}, Velocity: {v}, Angular Velocity: {w}")

def presetselector():
    drawing = Drawing(app, width=220, height=220)
    selection = str(text_box.value)
    ind = df[df["eName"]==selection].index.values
    e = float(df["eccentricity"][ind].values)
    b = b_calc(a, e)
    print(b)
    
    #drawing.oval(170, 30, 190, 50, color="white", outline=True)
    
    drawing.oval(0, 30, 0 + (a*30), 30 + (b*30), color="blue")

    distance = formula(a, b, theta)

    # insert movement code
    
    print(distance)



presetButton = PushButton(master=app, command=earth_preset, text='Earth', align="left")

presetButton2 = PushButton(master=app, command=moon_preset, text='Moon', align="left")

text_box = TextBox(app, text="enter text", align="left")
submit = PushButton(master=app, command=presetselector, text='Submit', align="left")


app.display()