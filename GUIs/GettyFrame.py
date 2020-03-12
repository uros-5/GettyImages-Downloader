from tkinter import *


class GettyFrame(Frame):

    def __init__(self,master):
        super(GettyFrame,self).__init__(master)
        self.grid()
        self.create_widgets()

    def create_widgets(self):

        """"
        search keywords
        sort by
        date range
        orientation
        imageresolution
        locations
        """
        Label(self,text='Search').grid(row=0,column=0,sticky=W)

        self.searchEntry = Entry(self,width=30)
        self.searchEntry.grid(row=0,column=1,sticky=W)

        self.sortByVar = StringVar()
        self.sortByVar.set(None)
        Label(self, text='Sort by',bg='red').grid(row=1, column=0, sticky=W)

        Radiobutton(self,text='best match',value='best',variable=self.sortByVar,command=self.getSort).grid(
            row=1,column = 1,sticky=W
        )
        Radiobutton(self, text='newest', value='newest', variable=self.sortByVar, command=self.getSort).grid(
            row=1, column=2, sticky=W
        )
        Radiobutton(self, text='oldest', value='oldest', variable=self.sortByVar, command=self.getSort).grid(
            row=1, column=3, sticky=W
        )
        Radiobutton(self, text='most popular', value='mostpopular', variable=self.sortByVar, command=self.getSort).grid(
            row=1, column=4, sticky=W
        )



        Label(self, text='Date range').grid(row=2, column=0, sticky=W)

        self.rangeVar = StringVar()
        self.rangeVar.set(None)

        Radiobutton(self, text='Any date', value='anydate', variable=self.rangeVar, command=self.getRange).grid(
            row=2, column=1, sticky=W
        )
        Radiobutton(self, text='last 24 hours', value='last24hours', variable=self.rangeVar, command=self.getRange).grid(
            row=2, column=2, sticky=W
        )
        Radiobutton(self, text='last 48 hours', value='last48hours', variable=self.rangeVar, command=self.getRange).grid(
            row=2, column=3, sticky=W
        )
        Radiobutton(self, text='last 72 hours', value='last72hours', variable=self.rangeVar, command=self.getRange).grid(
            row=2, column=4, sticky=W
        )
        Radiobutton(self, text='last 7 days', value='last7days', variable=self.rangeVar, command=self.getRange).grid(
            row=3, column=1, sticky=W
        )
        Radiobutton(self, text='last 30 days', value='last30days', variable=self.rangeVar, command=self.getRange).grid(
            row=3, column=2, sticky=W
        )
        Radiobutton(self, text='last 12 months', value='last12months', variable=self.rangeVar, command=self.getRange).grid(
            row=3, column=3, sticky=W
        )

        Label(self, text='Orientation').grid(row=4, column=0, sticky=W)

        self.orVertical = BooleanVar()
        self.orHorizontal = BooleanVar()
        self.orSquare = BooleanVar()
        self.orPanoramicHorizontal = BooleanVar()
        Checkbutton(self,
                    text="vertical",
                    variable= self.orVertical,
                    command=self.getOrientation
                    ).grid(row=4, column=1, sticky=W)
        Checkbutton(self,
                    text="horizontal",
                    variable=self.orHorizontal,
                    command=self.getOrientation
                    ).grid(row=4, column=2, sticky=W)
        Checkbutton(self,
                    text="square",
                    variable=self.orSquare,
                    command=self.getOrientation
                    ).grid(row=5, column=1, sticky=W)
        Checkbutton(self,
                    text="panaromicHorizontal",
                    variable=self.orPanoramicHorizontal,
                    command=self.getOrientation
                    ).grid(row=5, column=2, sticky=W)

        self.imgRes = StringVar()
        self.imgRes.set(None)
        Label(self, text='Image resolution').grid(row=6, column=0, sticky=W)

        Radiobutton(self, text='All', value=' ', variable=self.imgRes,
                    command=self.getResolution).grid(
            row=7, column=0, sticky=W
        )

        Radiobutton(self, text='12 MP and larger', value='xlarge', variable=self.imgRes, command=self.getResolution).grid(
            row=7, column=1, sticky=W
        )
        Radiobutton(self, text='16 MP and larger', value='xxlarge', variable=self.imgRes,
                    command=self.getResolution).grid(
            row=7, column=2, sticky=W
        )
        Radiobutton(self, text='21 MP and larger', value='xxxlarge', variable=self.imgRes,
                    command=self.getResolution).grid(
            row=7, column=3, sticky=W
        )
        for i in GettyFrame.winfo_children(self):
            if(str(i) =='.!gettyframe.!entry'):
                i.config(bg="#dcf0fa")
            else:
                i.config(bg="#81cbf0")

    def getSort(self):
        print(self.sortByVar.get())
    def getRange(self):
        print(self.rangeVar.get())
    def getOrientation(self):
        orientation = ""
        if self.orVertical.get():
            orientation += 'vertical'+','
        if self.orHorizontal.get():
            orientation+= 'horizontal'+','
        if self.orSquare.get():
            orientation+= 'square'+','
        if self.orPanoramicHorizontal.get():
            orientation+= 'panaromicHorizontal'
        print(orientation)
    def getResolution(self):
        print(self.imgRes.get())