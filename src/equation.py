from math import cos 
e = float(input("Eccentricity: ")) # eccentricity
a_or_b = input("Dou you have a or b? ") # do we pick a value for a or b
a = 2
b = 2
theta = float(input("theta: ")) # theta (obtained from stepper motor)
# a = float(input("a: ")) # a 





if a_or_b.lower() == "b":
    b = a*((1+e)*(1-e))**(1/2)
if a_or_b.lower() == "a":
    a = ((b*((1+e)*(1-e))**(1/2))/((1+e)*(1-e)))

formula = lambda a, b, theta : (((a*(1-(((a**2-b**2))/a)**(2)))/(1+(((a**2-b**2)/a)*cos(theta))))**(2)) + (a**2-b**2)-(2*(abs((a*(1-((a**2-b**2)/a**2)))/(1+(((a**2-b**2)/a)*cos(theta))))*cos(theta)))

distance = formula(a,b,theta)
print(distance)




