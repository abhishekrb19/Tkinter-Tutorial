from Tkinter import *

root = Tk()

equation = StringVar()
calculation = Label(root, textvariable=equation)
equation.set("1+0")
calculation.grid(columnspan=4)

equa = ""
def btnPress(num):
    global equa
    equa = equa + str(num)
    equation.set(equa)

Button0 = Button(root,text="0",command=lambda:btnPress(0))
Button1 = Button(root,text="1",command=lambda:btnPress(1))
Button2 = Button(root,text="2",command=lambda:btnPress(2))

Button0.grid(row=1, column=0)
Button1.grid(row=1, column=1)
Button2.grid(row=1, column=2)


root.mainloop()
