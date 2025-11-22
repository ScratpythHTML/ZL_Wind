import numpy as np
pi = np.pi
import matplotlib
import mecode
from mecode import G

# Note that the Y axis of the filament winder is in degrees, so distanc values need converting based off of the circumference
# Also note that angle will be defined as angle from horizontal

filename = "C:/Users/zakle/OneDrive - Imperial College London/ICLR\Winder Stuff/ZL Wind\wind1.gcode"

mandrel_dia = 181
wind_length = 700

initial_revs = 3
final_revs = initial_revs

base_speed = 4000

mandrel_circumference = pi * mandrel_dia

tow_width = 40

def helical(angle, pattern_number, speed=3000):

    g.feed(speed)

    end_wrap = 360 * 4

    if angle >= 90:
        return None
    y_dist = wind_length / np.cos(np.deg2rad(angle))
    revolutions = y_dist/mandrel_circumference
    y_angle = revolutions * 360
    line_spacing = end_wrap + (360 / pattern_number)

    for i in range(pattern_number):
        g.move(wind_length, y_angle)
        g.move(0,end_wrap)
        g.move(-wind_length, y_angle)
        g.move(0,line_spacing)

def hoop(angle, terminal, speed=3000, length=wind_length):

    g.feed(speed)

    if angle >= 90:
        return None
    y_dist = length / np.cos(np.deg2rad(angle))
    revolutions = y_dist/mandrel_circumference
    y_angle = revolutions * 360
    g.move(length, y_angle)

    if terminal == False:
        g.move(-length, y_angle)


with G(outfile="wind1.gcode") as g:

    g.feed(base_speed)
    g.write("G28 X") # Homing the X axis
    g.write("G4 S5") # Wait 5s
    g.move(0, initial_revs * 360)
    g.write("G4 S2") # Wait 2s
    helical(55, 5, 8000)
    g.write("G4 S2") # Wait 2s
    g.feed(base_speed)
    g.move(0, final_revs * 360)


with G(outfile="hoopwind.gcode") as g:
    g.feed(base_speed)
    g.write("G28 X") # Homing the X axis
    g.write("G4 S8") # Wait 8s
    g.move(0, 3 * 360)
    hoop_angle = np.rad2deg(np.arctan(mandrel_circumference / tow_width))
    hoop(hoop_angle, True, 4500) # have changed angle!!
    g.move(0, 5 * 360)

with G(outfile="rotisserie.gcode") as g:
    rpm = 6
    mm_speed = rpm * 360
    g.feed(mm_speed)

    hours = 40
    minutes = hours * 60
    distance = mm_speed * minutes
    g.move(0, distance)