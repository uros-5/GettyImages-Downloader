from tkinter import *
import tkinter.constants as constants
from GUIs.GettyFrame import Root,GettyFrame,PicturesFrame
root = Root()
root.title("Namenski racunarski sistemi")
root.config(bg="#81cbf0")
root.grid()
root.mainloop()


# def unisti():
#     for i in root.winfo_children():
#         i.destroy()
#     print('evo ko')
#     for i in root.winfo_children():
#         print(i)
#     global label1
#     print(label1)
#
# root = Tk()
# label1 = Label(root,text='<-', font='Courier 18 bold',background="#81cbf0")
# label2 = Label(root,text='<', font='Courier 18 bold',background="#81cbf0")
# label3 = Label(root,text='>', font='Courier 18 bold',background="#81cbf0")
# label4 = Label(root,text='0', font='Courier 18 bold',background="#81cbf0")
# btn1 = Button(root,text='UNISTI',command=unisti)
#
# label1.pack(side=constants.LEFT,fill="both", expand=True)
# label2.pack(side=constants.LEFT,fill="both", expand=True)
# label3.pack(side=constants.LEFT,fill="both", expand=True)
# label4.pack(side=constants.LEFT,fill="both", expand=True)
# btn1.pack(side=constants.LEFT,fill="both", expand=True)
# root.mainloop()