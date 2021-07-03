import pandas as pd
from guizero import *
from math import cos

EARTH = 0.017
MOON = 0.0549
a = 2
theta = 0

# import orbital dataset
df = pd.read_csv("../data/sol_data.csv")

formula = lambda a, b, theta : (((a*(1-(((a**2-b**2))/a)**(2)))/(1+(((a**2-b**2)/a)*cos(theta))))**(2)) + (a**2-b**2)-(2*(abs((a*(1-((a**2-b**2)/a**2)))/(1+(((a**2-b**2)/a)*cos(theta))))*cos(theta)))
b_calc = lambda a, e: a*((1+e)*(1-e))**(1/2) # Derive b with a known a 

app = App(title='test')

message = Text(app, text='Orbit Simulator', size=20)

def earth_preset():
    b = b_calc(a, EARTH)
    distance = formula(a,b,theta)
    print(distance)

def moon_preset():
    b = b_calc(a, MOON)
    distance = formula(a,b,theta)

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