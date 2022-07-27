from tkinter import *

window = Tk()
window.title("Classifier for Halliday")
window.configure(width=500, height=300)
window.configure(bg='lightgray')

submitButton = Button(window, text='Submit')
submitButton.place(x=380, y=30)

classTextField = Entry(window)
classTextField.place(x=380, y=10)

canvas = Canvas(window, bg='black')
canvas.place(x=0, y=0)

window.mainloop()

