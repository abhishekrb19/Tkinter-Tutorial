import Tkinter

class Calculator:

  def __init__(self):
    window = Tkinter.Tk()
    window.geometry("200x300")
    window.title("Calculator")

    self.labelText = ""
    equation = Tkinter.StringVar() # Added this
    lbl = Tkinter.Label(window, text="placeholder", bg="blue", textvariable=equation)

    lbl.grid(row=0, column=0, columnspan=3)

    self.firstNumArray = []
    self.secondNumArray = []
    self.operation = ""
    self.currentNum = "first"


    #equa = ""


    def btnPress(self,num):
      #global labelText, equation
      print "Num?",num
      self.labelText = self.labelText + str(num)
      equation.set(self.labelText)


    def appendNumber(self, number):
      print("Appending Number")
      if self.currentNum == "first":
        self.firstNumArray.append(number)
        print("".join(str(x) for x in self.firstNumArray))
        lbl.config(text="".join(str(x) for x in self.firstNumArray))
        window.update()
      else:
        self.secondNumArray.append(number)

    for i in range(1,4):
      string = "Creating button at ({0},{1})".format(0,i)
      print(string)
      button = Tkinter.Button(text=i, command=lambda: btnPress(self, i))
      button.grid(row=1, column=i-1)

    for i in range(1,4):
      string = "Creating button at ({0},{1})".format(1,i)
      print(string)
      button = Tkinter.Button(text=i+3, command=lambda: appendNumber(self, i+3))
      button.grid(row=2, column=i-1)

    for i in range(1,4):
      string = "Creating button at ({0},{1})".format(2,i)
      print(string)
      button = Tkinter.Button(text=i+6, command=lambda: appendNumber(self, i+6))
      button.grid(row=3, column=i-1)


    div = Tkinter.Button(text="/")
    mult = Tkinter.Button(text="*")
    add = Tkinter.Button(text="+")
    sub = Tkinter.Button(text="-")

    add.grid(row=1, column=3)
    sub.grid(row=2, column=3)
    mult.grid(row=3, column=3)
    div.grid(row=4, column=3)

    button = Tkinter.Button(text="0")
    button.grid(row=4, column=1)

    window.mainloop()



calc = Calculator()