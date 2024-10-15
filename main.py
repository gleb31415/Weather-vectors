import time
import tkinter as tk
import random
import math
import colorsys

root = tk.Tk()

dt = 1  # time step
dn = 5  # number of lines generated per second
k = 4  # "strength" of the vectors
lifetime = 120  # time before a point is erased
linecol = (0, 0, 255)  # color of the vectors

screen_width, screen_height = 1000, 1000
canvas = tk.Canvas(root, width=screen_width, height=screen_height, background='black')
vectors = []
lines = []
startp = None
plv = True


def color(dst):
    max = 30
    normalized_dist = min(dst / max, 1)
    hue = (1 / 3) * normalized_dist
    r, g, b = colorsys.hsv_to_rgb(hue, 1, 1)
    return '#{0:02x}{1:02x}{2:02x}'.format(int(r * 255), int(g * 255), int(b * 255))


def travel(traject):
    global vectors
    hs, vs = 0, 0
    for vector in vectors:
        distance = math.dist(vector[0], traject[-1][:2])
        if distance <= 10:
            continue

        phreal = vector[1][0] - vector[0][0]
        phdist = phreal * k / distance
        hs += phdist

        pvreal = vector[1][1] - vector[0][1]
        pvdist = pvreal * k / distance
        vs += pvdist

    return [traject[-1][0] + hs, traject[-1][1] + vs, color(math.sqrt(hs ** 2 + vs ** 2))]


def handle_point(traject, i):
    global lines
    cnt = len(traject)
    if cnt <= lifetime:
        newp = travel(traject)
        lines[i].append(newp)
        for j in range(1, len(traject)):
            canvas.create_line(traject[j][0], traject[j][1], traject[j - 1][0], traject[j - 1][1], fill=traject[j][2],
                               tags='line')
    else:
        lines.pop(i)


def add_vector(event):
    global vectors, startp, lines
    mouse_pos = [event.x, event.y]
    if startp == None:
        startp = mouse_pos
    else:
        vectors.append([startp, mouse_pos])
        startp = None
        lines = []


def clear(event):
    global plv
    canvas.delete('vectors')
    plv = (plv + 1) % 2


def main():
    # canvas.delete('vectors')
    canvas.delete('all')
    if plv:
        for vector in vectors:
            canvas.create_oval((vector[0][0] - 5, vector[0][1] - 5), (vector[0][0] + 5, vector[0][1] + 5), fill='red',
                               tags='vectors')
            canvas.create_line((vector[0][0], vector[0][1], vector[1][0], vector[1][1]), fill='blue', tags='vectors',
                               width=3, arrow='last')
    for _ in range(dn):
        lines.append([[random.randint(0, screen_width), random.randint(0, screen_height)]])
    for j in range(len(lines) - 1, -1, -1):
        handle_point(lines[j], j)
    root.after(dt, main)


canvas.bind('<Button-1>', add_vector)
root.bind('e', clear)
main()
canvas.pack()
root.mainloop()
