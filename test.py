from tkinter import *

# Input Output File
file1 = open('myfile.txt', 'r')
Lines = file1.readlines()
text_input = []
text_output = []
text_center = ''
for line in Lines:
    x = [s.strip() for s in line.split(' ')]
    if 'module' in x:
        text_center = x[1]
    if 'input' in x:
        text_input.append(x[1])
    if 'output' in x:
        text_output.append(x[1])


root = Tk()
root.geometry('700x500')

c = Canvas(root)
c.pack()


# Rectangle
length = 200
width = 100
bottom_left = 100, 150

points = [(bottom_left[0], bottom_left[1]), (bottom_left[0] + length, bottom_left[1] - width)]
c.create_rectangle(points, fill='', outline='black')
c.create_text(bottom_left[0] + int(length/2), bottom_left[1] - int(width/2), text=text_center)

# Triangle Properties
floor = 20
height = 25

points_triangle = [(0, 0), (0, floor),  (height, int(floor/2))]

# Input Loop
for i in range(0, len(text_input)):
    newxy = []
    offset = [bottom_left[0] - height, bottom_left[1] - width + i*(floor + 5)]
    for x,y in points_triangle:
        newxy.append((x+offset[0], y+offset[1]))
        c.create_polygon(newxy, fill='', outline='black')
    c.create_text(x+offset[0]-5*(len(text_input[i])+1), y+offset[1], text=text_input[i], justify='right')


# Output Loop
for i in range(0, len(text_output)):
    newxy = []
    offset = [bottom_left[0] + length, bottom_left[1] - width + i*(floor + 5)]
    for x, y in points_triangle:
        newxy.append((x+offset[0], y+offset[1]))
        c.create_polygon(newxy, fill='', outline='black')
    c.create_text(x+offset[0]+height, y+offset[1], text=text_output[i], justify='left')

root.mainloop()
