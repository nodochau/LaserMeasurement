from email.mime import image
import tkinter

class MyButtons(tkinter.Button):
    def __init__(self, master, text, row, col, padx, pady, **kw):
        self.text = text
        self.row = row
        self.col = col
        self.padx = padx
        self.pady = pady
        # self.rowsp = rowsp
        # self.colspan = colspan
        
        super().__init__(master=master, **kw)
        self['text'] = text
        self.grid(row=row, column=col, padx=padx, pady=pady)


# arr_00 = 'arr00.png'
# root = tkinter.Tk()
# root.title("Testing imgages")
# root.geometry('200x200')
# arr_00Btn = tkinter.PhotoImage(file=arr_00, width=300, height=300)
# btn = MyButtons(root, '', 0, 0, 1, 1, 10, 10, image=arr_00Btn)
# root.mainloop()