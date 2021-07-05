import pandas as pd
from guizero import *
from math import cos, pi

G = 6.67408e-11

EARTH_E = 0.017 #eccentricities
MOON_E = 0.0549 #relative to earth
MERCURY_E = 0.2056
EARTH_MASS = 5.97216787e+24 #kg
MOON_MASS = 7.34767309e+22 #kg
SUN_MASS = 1.989e+30 #kg
MERCURY_MASS = 3.285e+23 #kg
A = 18 * 2.54 / 100 #m
EARTH_A = 149.60e+9 #m
MOON_A = 384748000 #m
MERCURY_A = 57.909e+9 #m
EARTH_PERIOD = 365 #days
MOON_PERIOD = 28 #days
MERCURY_PERIOD = 88 #days
theta = 0

ORBIT_STATUS = True # orbit status for turning on and off servo motor

# import orbital dataset
df = pd.read_csv("../data/sol_data.csv")

# formula = lambda a, b, theta : (((a*(1-(((a**2-b**2))/a)**(2)))/(1+(((a**2-b**2)/a)*cos(theta))))**(2)) + (a**2-b**2)-(2*(abs((a*(1-((a**2-b**2)/a**2)))/(1+(((a**2-b**2)/a)*cos(theta))))*cos(theta)))


b_calc = lambda a, e : a*((1+e)*(1-e))**(1/2) # Derive b with a known a 
distance_calc = lambda a, b, theta : ((a ** 2) - ((a ** 2 - b ** 2) ** (1 / 2)) ** (2)) / (a + ((a ** 2 - b ** 2) ** (1 / 2)) * (cos(theta)))
velocity_calc = lambda g, m, r, a : (g * m * ((2 / r) - (1 / a))) ** (1 / 2)


app = App(title='test')

message = Text(app, text='Orbit Simulator', size=20)

def earth_preset(period=45):
    sf = A / EARTH_A
    b = b_calc(A, EARTH_E) #m
    d = distance_calc(A, b, theta) #m
    v = velocity_calc(G, (EARTH_MASS + SUN_MASS) * (sf) ** (3), d, A) #m/s
    v *= (EARTH_PERIOD * 24 * 60 * 60) / period
    w = v/d # maybe factor in height of planet
    print(f"Distance: {d}, Velocity: {v}, Angular Velocity: {w}")

def moon_preset(period=45):
    sf = A / MOON_A
    b = b_calc(A, MOON_E)
    d = distance_calc(A, b, theta)
    v = velocity_calc(G, (MOON_MASS + EARTH_MASS) * (sf) ** (3), d, A) #m/s
    v *= (MOON_PERIOD * 24 * 60 * 60) / period
    w = v/d
    print(f"Distance: {d}, Velocity: {v}, Angular Velocity: {w}")

def mercury_preset(period=45):
    sf = A / MERCURY_A
    b = b_calc(A, MERCURY_E)
    d = distance_calc(A, b, theta)
    v = velocity_calc(G, (MERCURY_MASS + SUN_MASS) * (sf) ** (3), d, A)  # m/s
    v *= (MERCURY_PERIOD * 24 * 60 * 60) / period
    w = v / d
    print(f"Distance: {d}, Velocity: {v}, Angular Velocity: {w}")

def presetselector():
    drawing = Drawing(app, width=220, height=220)
    selection = str(text_box.value)
    ind = df[df["eName"]==selection].index.values
    e = float(df["eccentricity"][ind].values)
    b = b_calc(a, e)
    print(b)
    
    #drawing.oval(170, 30, 190, 50, color="white", outline=True)
    
    drawing.oval(0, 30, 0 + (a*30), 30 + (b*30), color="blue")

    distance = distance_calc(a, b, theta)

    # insert movement code
    
    print(distance)



earthPresetButton = PushButton(master=app, command=earth_preset, text='Earth', align="left")

moonPresetButton = PushButton(master=app, command=moon_preset, text='Moon', align="left")
mercuryPresetButton = PushButton(master=app, command=mercury_preset, text='Mercury', align="left")

text_box = TextBox(app, text="enter text", align="left")
submit = PushButton(master=app, command=presetselector, text='Submit', align="left")


app.display()