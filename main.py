from tkinter import *
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from rolgordijn import Rolgordijn
import threading

def thread_function():
    while True:
        time.sleep(1)
        for each in rolluiken:
            if rolluiken[each][2].error > 2:
                delete(each+1)
                error("ERROR Packets lost\nHet rolluik is verwijderd")
                break
            temperature = None
            indx = 0
            while temperature==None and indx < 10:
                temperature = rolluiken[each][2].get_temperature()
                indx = indx + 1

            if indx == 10:
                rolluiken[each][2].error = rolluiken[each][2].error + 1

            if temperature is not None:
                rolluiken[each][2].yt.append(temperature)
                rolluiken[each][2].error = 0
            indx = 0

            light = None
            indx = 0
            while light==None and indx < 10:
                light = rolluiken[each][2].get_light()
                indx = indx + 1

            if indx == 10:
                rolluiken[each][2].error = rolluiken[each][2].error + 1

            if light is not None:
                rolluiken[each][2].yl.append(light)
                rolluiken[each][2].error = 0
            indx = 0



def destroy():
    error_window.destroy()

def error(text):
    global error_window
    error_window = Tk()
    error_window.title("Error")
    error_window.geometry("200x125")
    Label(error_window,height=1,text="  ",font='verdana 9') .grid(row=1, column=0, sticky=NSEW)
    Label(error_window,height=1,text="",font='verdana 9') .grid(row=0, column=1, sticky=NSEW)
    Label(error_window,height=2,text=text,font='verdana 9') .grid(row=1, column=1, sticky=NSEW)
    Label(error_window,height=1,text="",font='verdana 9') .grid(row=2, column=0, sticky=NSEW)
    Button(error_window, text="OK",font='verdana 9',height=2, width=20, command=destroy) .grid(row=3, column=1, sticky=NSEW)
    error_window.mainloop()

def info(text):
    global error_window
    error_window = Tk()
    error_window.title("Info")
    error_window.geometry("200x125")
    Label(error_window,height=1,text="  ",font='verdana 9') .grid(row=1, column=0, sticky=NSEW)
    Label(error_window,height=1,text="",font='verdana 9') .grid(row=0, column=1, sticky=NSEW)
    Label(error_window,height=2,text=text,font='verdana 9') .grid(row=1, column=1, sticky=NSEW)
    Label(error_window,height=1,text="",font='verdana 9') .grid(row=2, column=0, sticky=NSEW)
    Button(error_window, text="OK",font='verdana 9',height=2, width=20, command=destroy) .grid(row=3, column=1, sticky=NSEW)
    error_window.mainloop()

def bee(string):
    x = "The bee, of course, flies anyway"
    if x in string:
        return True
    else:
        return False

def add_rolluik():
    global nameEntry,comEntry,add_window,rolluiken
    name= nameEntry.get()
    com = comEntry.get()
    if name == "" or com == "":
        error("Error\nVoer waardes in")
    elif len(name)>20:
        if bee(name):
            error("BEE MOVIE NOT ALLOWED!!!")
        else:
            error("Error\nNaam is te lang")

    else:
        index1 = True
        index2 = False

        for i in rolluiken:
            if rolluiken[i][0] == name:
                error("Rolluik met deze waarde\nbestaat al")
                index1 = False
        for x in ports:
            if com == x:
                index2 = True
                for i in rolluiken:
                    if rolluiken[i][1] == com:
                        error("Dit Rolluik is al\n verbonden")
                        index2 = False


        if not index2:
            error("Voer geldige COM port in")

        if index1 and index2:
            add(name, com)
            add_window.destroy()




def delete(ndex):
    list = main_window.grid_slaves(row=ndex)
    for l in list:
        l.destroy()
    list = main_window.grid_slaves(row=ndex-1)
    for l in list:
        l.destroy()
    if rolluiken[ndex-1][2].port.is_open:
        rolluiken[ndex-1][2].port.close()
    del rolluiken[ndex-1][2]
    del rolluiken[ndex-1]



def toevoegen():
    global nameEntry,comEntry,add_window
    add_window = Tk()
    add_window.title("Toevoegen")
    Label(add_window,text="Naam:",height=2,font='verdana 9') .grid(row=1,column=0,sticky=W)
    nameEntry = Entry(add_window, width=20, bg="white",font='verdana 9')
    nameEntry.grid(row=1,column=1,sticky=W)
    Label(add_window,text="\nCOM:",height=2,font='verdana 9') .grid(row=2,column=0,sticky=W)
    comEntry = Entry(add_window, width=20, bg="white",font='verdana 9')
    comEntry.grid(row=2,column=1,sticky=W)
    Label(add_window,height=1,text="",font='verdana 9') .grid(row=3,column=0,sticky=W)
    Button(add_window, text="Voeg rolluik toe",font='verdana 9',height=2, width=20, command=add_rolluik) .grid(row=4,column=1,sticky=W)

    add_window.mainloop()

def open(g):
    i = 0
    success = g.set_is_open(True)
    while not success:
        if i < 5:
            i = i + 1
            time.sleep(0.05)
            error("Lost packets\nklik niet te vaak op de knop")
            success = g.set_is_open(True)
        else:
            error("Lost packets\nArduino is niet aangesloten")
            break
    i = 0


def close(g):
    i = 0
    success = g.set_is_open(False)
    while not success:
        if i < 5:
            i = i + 1
            time.sleep(0.05)
            error("Lost packets\nklik niet te vaak op de knop")
            success = g.set_is_open(False)
        else:
            error("Lost packets\nArduino is niet aangesloten")
            break
    i = 0

def auto(g):
    i = 0
    success = g.set_is_automatic(True)
    while not success:
        if i < 5:
            i = i + 1
            time.sleep(0.05)
            error("Lost packets\nklik niet te vaak op de knop")
            success = g.set_is_automatic(True)
        else:
            error("Lost packets\nArduino is niet aangesloten")
            break
    i = 0

def open_all():
    for x in rolluiken:
        g = rolluiken[x][2]
        i = 0
        success = g.set_is_open(True)
        while not success:
            if i < 5:
                i = i + 1
                time.sleep(0.05)
                error("Lost packets\nklik niet te vaak op de knop")
                success = g.set_is_open(True)
            else:
                error("Lost packets\nArduino is niet aangesloten")
                break
        i = 0


def close_all():
    for x in rolluiken:
        g = rolluiken[x][2]
        i = 0
        success = g.set_is_open(False)
        while not success:
            if i < 5:
                i = i + 1
                time.sleep(0.05)
                error("Lost packets\nklik niet te vaak op de knop")
                success = g.set_is_open(False)
            else:
                error("Lost packets\nArduino is niet aangesloten")
                break
        i = 0


def auto_all():
    for x in rolluiken:
        g = rolluiken[x][2]
        i = 0
        success = g.set_is_automatic(True)
        while not success:
            if i < 5:
                i = i + 1
                time.sleep(0.05)
                error("Lost packets\nklik niet te vaak op de knop")
                success = g.set_is_automatic(True)
            else:
                error("Lost packets\nArduino is niet aangesloten")
                break
        i = 0

def update_rolluik(g):
    new_temp = slider_temp.get()
    new_licht = slider_licht.get()
    new_close = closeEntry.get()
    new_open = openEntry.get()
    index = True
    if "," in new_close or "," in new_open:
        error("ERROR\nPlease enter a number")
        index = False
    if index:
        try:
            int(new_close) and int(new_open)
        except ValueError:
            index = False
            error("ERROR\nPlease enter a number")
    if index:
        while g.set_temperature_border(new_temp) == False:
            None
        while g.set_light_border(new_licht) == False:
            None
        while g.set_open_distance_border(new_open) == False:
            None
        while g.set_close_distance_border(new_close) == False:
            None



def add(name,com):
    global x,rolluiken
    try:
        g = Rolgordijn(com)
    except Exception:
        error("Kan niet verbinden\nvia deze COM")
    rolluiken[x] = [name,com,g]
    Label(main_window,text=name, font='verdana 9') .grid(row=x,column=0,sticky=W)
    x = x + 1
    Button(main_window, text="Luik open",font='verdana 9', width=20, command=lambda ndex = g: open(ndex)) .grid(row=x,column=0,sticky=W)
    Button(main_window, text="Luik dicht",font='verdana 9', width=20, command=lambda ndex = g: close(ndex)) .grid(row=x,column=1,sticky=W)
    Button(main_window, text="Automatisch",font='verdana 9', width=20, command=lambda ndex = g: auto(ndex)) .grid(row=x,column=2,sticky=W)
    Button(main_window, text="Data",font='verdana 9', width=20, command=lambda ndex = g: data(ndex)) .grid(row=x,column=3,sticky=W)
    Button(main_window, text="Status",font='verdana 9', width=20, command=lambda g = g: info(('Open' if g.get_is_open() else 'Closed') + (' (Automatisch)' if g.get_is_automatic() else ''))) .grid(row=x,column=4,sticky=W)
    Button(main_window, text="x",font='verdana 9', width=5, command=lambda ndex = x: delete(ndex)) .grid(row=x,column=5,sticky=W)
    x = x + 1

def animate(i,z):

    yt = z.yt[::]
    yl = z.yl[::]
    xt = []
    xl = []

    ind = 0
    for x in yt:
        xt.append(ind)
        ind = ind + 2
    ind = 0
    for x in yl:
        xl.append(ind)
        ind = ind + 2
    ax1.clear()
    ax1.plot(xt, yt)
    ax1.set_ylim(bottom=0)
    ax1.set_ylim(top=40)
    ax2.clear()
    ax2.plot(xl,yl)
    ax2.set_ylim(top=1000)
    ax2.set_ylim(bottom=0)
    ax1.set_ylabel('Temperatuur in C')

    ax2.set_ylabel('Licht intensiteit')
    ax2.set_xlabel('Time in seconds')

def grafieken(g):
    global ax2,ax1
    z = g

    fig = plt.figure()
    ax1 = fig.add_subplot(211)
    ax2 = fig.add_subplot(212)

    ani = animation.FuncAnimation(fig, lambda i, asd = g: animate(i, asd), interval=2000)

    plt.show()

def data(g):
    global slider_temp,slider_licht,openEntry,closeEntry
    temp_indx = True
    light_indx = True
    open_indx = True
    close_indx = True

    data_window = Tk()
    data_window.title("Data")

    Label(data_window,text="Licht intensiteit:\nGrenswaarden: 0 - 1000",font='verdana 9') .grid(row=1,column=0,sticky=W)

    slider_licht = Scale(data_window, orient=VERTICAL, length=120, from_=1000, to=0,resolution=20)
    slider_licht.grid(row=1, column=1, sticky='w')
    while light_indx:
        light = g.get_light_border()
        time.sleep(0.05)
        if light is not None:
            light_indx = False
    slider_licht.set(light)

    Label(data_window,text="Temperatuur:\nGrenswaarden: 0 - 40 C",font='verdana 9') .grid(row=2,column=0,sticky=W)
    slider_temp = Scale(data_window, orient=VERTICAL, length=120, from_=40, to=0,resolution=0.5)
    slider_temp.grid(row=2, column=1, sticky='w')
    while temp_indx:
        temperature = g.get_temperature_border()
        time.sleep(0.05)
        if temperature is not None:
            temp_indx = False
    slider_temp.set(temperature)
    Label(data_window,text="Close grens:\nGrenswaarden: 0 - 300",font='verdana 9') .grid(row=1,column=2,sticky=W)
    openEntry = Entry(data_window, width=20, bg="white")
    openEntry.grid(row=1,column=3,sticky=W)
    while open_indx:
        open = g.get_open_distance_border()
        time.sleep(0.05)
        if open is not None:
            open_indx = False
    openEntry.insert(END, open)
    Label(data_window,text="Open grens:\nGrenswaarden: 0 - 300", font='verdana 9') .grid(row=2,column=2,sticky=W)
    closeEntry = Entry(data_window, width=20, bg="white")
    closeEntry.grid(row=2,column=3,sticky=W)
    while close_indx:
        close = g.get_close_distance_border()
        time.sleep(0.05)
        if close is not None:
            close_indx = False
    closeEntry.insert(END, close)
    Button(data_window, text="Verstuur",font='verdana 9', width=20, height = 2, command=lambda ndex = g: update_rolluik(ndex)) .grid(row=5,column=3,sticky=W)
    Button(data_window, text="Grafieken",font='verdana 9', width=20, height = 2, command=lambda ndex = g: grafieken(ndex)) .grid(row=5,column=0,sticky=W)

    data_window.mainloop()


ports = ['COM%s' % (i + 1) for i in range(256)]
rolluiken = {}
x = 2
global main_window
main_window = Tk()
main_window.title("Rolluiken Systeem")
main_window.configure()

Button(main_window, text="Voeg rolluik toe",font='verdana 9',height=2, width=20, command=toevoegen) .grid(row=0,column=0,sticky=W)
Button(main_window, text="Rolluiken open",font='verdana 9',height=2, width=20, command=open_all) .grid(row=0,column=1,sticky=W)
Button(main_window, text="Rolluiken dicht",font='verdana 9',height=2, width=20, command=close_all) .grid(row=0,column=2,sticky=W)
Button(main_window, text="Rolluiken Automatisch",font='verdana 9',height=2, width=20, command=auto_all) .grid(row=0,column=3,sticky=W)


thread = threading.Thread(target=thread_function)
thread.daemon = True
thread.start()

main_window.mainloop()
