from tkinter import *
from tkinter.messagebox import *

true = True
false = False

class GUI:
    def __init__(self,title:str):
        self.win = Tk()
        self.win.title(title)
        self.win.geometry("300x300")
        self.win.resizable(false,false)
        # label
        Label(self.win,text='config freq:').grid(row=0,column=0,sticky='ew')
        # entry
        self.sec_entry=Entry(self.win,width=5)
        self.sec_entry.grid(row=0,column=1,sticky='w')
        Label(self.win, text='sec').grid(row=0,column=2,sticky='w')
        Label(self.win, text='').grid(row=1, column=0, sticky='w')
        Label(self.win, text='Choose CPU mode:').grid(row=2,column=0,columnspan=2,sticky='ew')
        # switch
        self.states = {}
        self.rb = {}
        i = 2
        for mode in getCPUmodes():
            self.states[mode] = False
            self.rb[mode] = Radiobutton(self.win, text=str(mode), value=mode,command=(lambda mode=mode: self.__onPress(str(mode))))
            i += 1
            self.rb[mode].grid(row=i,column=0,columnspan=2,sticky='w')
        self.__onPress('conservative')
        # button
        Button(self.win,command=self.__pressButton,text='Ok').grid(row=i+1,column=1,columnspan=3,ipadx=0,sticky='ew')
        self.win.mainloop()
        print(self.states)

    def __onPress(self,mode: str):
        self.rb[mode].select()
        for m in self.states.keys():
            self.states[m] = False
        self.states[mode] = True

    def __pressButton(self):
        entry_time = self.sec_entry.get()
        if entry_time.isnumeric() and entry_time.isdigit():
            pass
            # self.test_label["text"]=entry_time
            # self.win.quit()
        else:

            showerror(title='invalid data type',message=f'You must enter numbers but you entered "{self.sec_entry.get()}"')
            self.sec_entry.delete(first=0, last=END)
            self.sec_entry.focus()





def getCPUmodes()->list:
    return ['conservative', 'ondemand', 'userspace', 'powersave', 'performance', 'schedutil']


if "__main__" == __name__:
    # gui = GUI("Change CPU mode")
    print('Hello word')
    pass

