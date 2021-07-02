from math import cos


def presets(satellite: str):
    a = 60.96
    theta = 0


    # Satellite Eccentricity Presets
    EARTH = 0.017
    MOON = 0.0549
    PHOBOS = 0.0151

    # Functions 
    formula = lambda a, b, theta : (((a*(1-(((a**2-b**2))/a)**(2)))/(1+(((a**2-b**2)/a)*cos(theta))))**(2)) + (a**2-b**2)-(2*(abs((a*(1-((a**2-b**2)/a**2)))/(1+(((a**2-b**2)/a)*cos(theta))))*cos(theta)))
    b_calc = lambda a, e: a*((1+e)*(1-e))**(1/2) # Derive b with a known a 

    # Select a Preset
    preset = input("Choose a preset: ")


    if satellite.lower() == "earth":
        b = b_calc(a, EARTH)
        distance = formula(a,b,theta)
        # insert distance in for loop w stepper motor val as theta
    if satellite.lower() == "moon":
        b = b_calc(a, MOON)
        distance = formula(a,b,theta)
    if satellite.lower() == "phobos":
        b = b_calc(a, PHOBOS)
        distance = formula(a,b,theta)








