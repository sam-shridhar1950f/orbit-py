def perihelion(satellite: str):
    a_unscaled = lambda r, e : (r)/(1-e)
    
    if satellite.lower() == "earth":
        return a_unscaled(1.47091144e+13, 0.017)
    elif satellite.lower() == "moon":
        return a_unscaled(3.829e+10, 0.0549)
    elif satellite.lower() == "phobos":
        return a_unscaled(9.234e+8,0.0151)
    else:
        print("invalid preset")

