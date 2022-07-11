import tkinter
from tkinter import *
#import string
from tkinter import messagebox
from turtle import pen
import serial, time
import tkinter
from tkinter import *
import pandas as pd

red = 'red.png'
green = 'green.png'
dataFile = ''
dataPos = [] # data of positions
positionIndex = 0 # the position that read from data list
arduino = serial.Serial("COM3")
arduino.baudrate = 9600
time.sleep(2)
line = "" # variable to store command send from arduino
previousMaterial = '' 
redFlashSignal = 0
greenFlashSignal = 0
homeBtnFlashSignal = 0

def jogMotorFWRoot(obj):
    obj.focus()
    cmd = 'j'
    write_to_arduino(cmd)

def jogMotorBWRoot(obj):
  obj.focus()
  cmd = 'k'
  write_to_arduino(cmd)

def stopJogMotorRoot(obj):
    obj.focus()
    cmd = 'n'
    write_to_arduino(cmd)

def home_part():
    cmd = 'a'
    write_to_arduino(cmd)

def setupProgram():

  def home_machine():
    global homeBtnFlashSignal
    homeBtnFlashSignal = 1
    cmd = 'h'
    write_to_arduino(cmd)

  def jogMotorFW(event):
    jogMotorFWRoot(pEntry)
   
  def jogMotorBW(event):
    jogMotorBWRoot(pEntry)
    
  def stopJogMotor(event):
    stopJogMotorRoot(partHomeButton)
    
  def writeData(pos):
    global dataFile
    dataFile = matEntry.get() + ".csv"
    try:
        with open(dataFile, 'r') as rf:
            rf.readline()
    except FileNotFoundError:
        with open(dataFile, 'a') as wf:
            print('POSITION', file=wf)
            print(pos, file=wf)
    else:
        with open(dataFile, 'a') as wf:
            print(pos, file=wf)

  def savePosition():
    data = matEntry.get()
    if (data == ""):
      messagebox.showerror("DATA INPUT ERROR", 'MATERIAL CAN NOT BE BLANK')
    else:
      writeData(line)

  def finishSetup():
    cmd = 'b'
    write_to_arduino(cmd)
    materialEntry.delete(0, tkinter.END)
    materialEntry.insert(0, matEntry.get())
    mainWindow.destroy()
    root.wm_state('normal')

  def flashHomeBtn():
    if homeBtnFlashSignal == 1:
      homeButton.config(background='#ffcead')
      homeButton.after(100, lambda: homeButton.config(background='#3d84b8'))
    if homeBtnFlashSignal == 0:
      homeButton.config(background=originalColor)
    mainWindow.after(500, flashHomeBtn)

  def showing_position():
    global line, redFlashSignal, greenFlashSignal, homeBtnFlashSignal, positionIndex
    if arduino.inWaiting()>0:
        line = str(arduino.readline().decode("utf-8"))
        line = line.strip()
        if (line == 'a'):
          pEntry.delete(0, tkinter.END)
          pEntry.insert(0, '0')
        else:
          if (line != 'd'):
            line = int(line)
            if(line != 0):
              #showed_pos = "{:.5f}".format(line)
              pEntry.delete(0, tkinter.END)
              pEntry.insert(0, line)
            if(line == 0):
              homeBtnFlashSignal = 0
              entry_pos.delete(0, tkinter.END)
              entry_pos.insert(0, "Home Position")
    mainWindow.after(100, showing_position)

  def disable_event():
    # this function to bypass the Close window event. So not able to close window
    pass

  mainWindow = tkinter.Tk()
  mainWindow.title('SET UP PROGRAM')
  locateGUI(mainWindow, 450, 220)
  mainWindow.protocol('WM_DELETE_WINDOW', disable_event)
  matLabel = tkinter.Label(mainWindow, text='MATERIAL NUMBER')
  matLabel.grid(row=0, column=0, padx=40, pady=15)
  matEntry = tkinter.Entry(mainWindow, width=20)
  matEntry.config(justify='center')
  matEntry.focus()
  matEntry.grid(row=0, column=1)
  pLabel = tkinter.Label(mainWindow, text='POSITION')
  pLabel.grid(row=1, column=0, padx=40)
  pEntry = tkinter.Entry(mainWindow, width=20)
  pEntry.config(justify='center')
  pEntry.grid(row=1, column=1)
  jog_fwButton = tkinter.Button(mainWindow, text="JOG-FW MACHINE", width=15)
  jog_fwButton.grid(row=2, column=0, pady=20, padx=30)
  jog_fwButton.bind('<ButtonPress-1>', jogMotorFW)
  jog_fwButton.bind('<ButtonRelease-1>', stopJogMotor)
  jog_bwButton = tkinter.Button(mainWindow, text="JOG-BW MACHINE", width=15)
  jog_bwButton.grid(row=2, column=1, padx=40)
  jog_bwButton.bind('<ButtonPress-1>', jogMotorBW)
  jog_bwButton.bind('<ButtonRelease-1>', stopJogMotor)
  partHomeButton = tkinter.Button(mainWindow, text="HOME PART POS", width=15, command=home_part)
  partHomeButton.grid(row=3, column=0)
  finishButton = tkinter.Button(mainWindow, text="FINISH SETUP", width=15, command=finishSetup)
  finishButton.grid(row=4, column=1)
  homeButton = tkinter.Button(mainWindow, text="HOME MACHINE", width=15, command=home_machine)
  homeButton.grid(row=4, column=0, pady=10)
  originalColor = homeButton.cget("background")
  saveButton = tkinter.Button(mainWindow, text="SAVE PSOSITION", width=15, command=savePosition)
  saveButton.grid(row=3, column=1)
  mainWindow.after(100, showing_position)
  mainWindow.after(500, flashHomeBtn)
  mainWindow.mainloop()

def locateGUI(window, w, h):
  widthScreen = window.winfo_screenwidth()
  heightScreen = window.winfo_screenheight()
  #calculate coordinates x, y for tk root window
  x = widthScreen/2 - w/2
  y = heightScreen/2 - h/2

  window.geometry('%dx%d+%d+%d' % (w, h, x, y))

def readData(matNum):
  dataFile = matNum + '.csv'
  try:
      with open(dataFile, 'r') as rf:
          rf.readline()
  except FileNotFoundError:
    messagebox.showerror('PROGRAM STATUS', 'Could not find the program. Please verify material number')
    return False
  else:
    data = pd.read_csv(dataFile)
    posList = list(data['POSITION'])
    return posList



def Flashing ():
  if redFlashSignal == 1 and greenFlashSignal == 0:
    redBtn.grid_forget()
    on_bwButton.grid_configure(row=1, column=1)
    redBtn.after(300, lambda: redBtn.grid(row=0, column=1, pady=5))
  if greenFlashSignal == 1 and redFlashSignal == 0:
    greenBtn.grid_forget()
    on_fwButton.grid_configure(row=1, column=0, pady=5)
    greenBtn.after(300, lambda: greenBtn.grid(row=0, column=0, pady=5))
  
  root.after(500, Flashing)

def turn_on_fw():
    global redFlashSignal, greenFlashSignal
    if greenFlashSignal == 0:
        greenFlashSignal = 1
        redFlashSignal = 0
    cmd = 'o' + str(slider.get())
    write_to_arduino(cmd)
    partHomeButton.config(state=DISABLED)

def turn_on_bw():
    global redFlashSignal, greenFlashSignal
    if redFlashSignal == 0:
        redFlashSignal = 1
        greenFlashSignal = 0
    cmd = 'f' + str(slider.get())
    write_to_arduino(cmd)
    partHomeButton.config(state=DISABLED)
    
def turn_off():
    global redFlashSignal, greenFlashSignal
    redFlashSignal = 0
    greenFlashSignal = 0
    cmd = 'q'
    write_to_arduino(cmd)
    partHomeButton.config(state=NORMAL)

def runProgram():
    global redFlashSignal, greenFlashSignal, dataPos, positionIndex, previousMaterial
    myMaterial = materialEntry.get()
    if (readData(myMaterial)):
      if(previousMaterial == ''):
        previousMaterial = myMaterial
        if (len(dataPos) == 0):
          dataPos = readData(myMaterial)
      else:
        if(previousMaterial != myMaterial):
          dataPos = readData(myMaterial)
          previousMaterial = myMaterial
      if(positionIndex == 0):
        if greenFlashSignal == 0:
          greenFlashSignal = 1
          redFlashSignal = 0
          cmd = 'p' + str(dataPos[positionIndex])
          entry_pos.delete(0, tkinter.END)
          entry_pos.insert(0, str(dataPos[positionIndex]))
          write_to_arduino(cmd)
      else:
        cmd = 'p' + str(dataPos[positionIndex])
        entry_pos.delete(0, tkinter.END)
        entry_pos.insert(0, str(dataPos[positionIndex]))
        write_to_arduino(cmd)

def jogMotorFWR(event):
    jogMotorFWRoot(entry_pos)
   
def jogMotorBWR(event):
  jogMotorBWRoot(entry_pos)
  
def stopJogMotorR(event):
  stopJogMotorRoot(partHomeButton)

def runPartHome():
  global redFlashSignal, greenFlashSignal
  if greenFlashSignal == 0:
    greenFlashSignal = 1
    redFlashSignal = 0
  cmd = 'm'
  write_to_arduino(cmd)

def write_to_arduino(in_put):
    arduino.write(in_put.encode())

def slider_change(event):
    current_value = str(slider.get())

def setProgram():
  root.wm_state('iconic')
  setupProgram()

def showing_pos():
    global line, redFlashSignal, greenFlashSignal, homeBtnFlashSignal, positionIndex
    if arduino.inWaiting()>0:
        line = str(arduino.readline().decode("utf-8"))
        line = line.strip()
        if (line == 'a'):
          entry_pos.delete(0, tkinter.END)
          entry_pos.insert(0, '0')
        else:
          if (line == "s"):
            positionIndex += 1
            if positionIndex < len(dataPos):
                runProgram()
                entry_pos.delete(0, tkinter.END)
                entry_pos.insert(0, str(dataPos[positionIndex]))
            else:
              runPartHome()
              entry_pos.delete(0, tkinter.END)
              entry_pos.insert(0, '0')
          else:
            if (line == "d"):
              turn_off()
              line = ""
              positionIndex = 0
              
    root.after(100, showing_pos)
    
root = tkinter.Tk()
root.title("B&G LASER PROGRAM")
locateGUI(root, 400, 380)
#arduino.open()
if arduino.isOpen():
        print("{} is connected".format(arduino.port))


red_btn = PhotoImage(file=red, width=60, height=60)
green_btn = PhotoImage(file=green, width=60, height=60)
redBtn = tkinter.Button(root,image=red_btn, border=0)
redBtn.grid(row=0, column=1, pady=5)
greenBtn = tkinter.Button(root, image=green_btn, border=0)
greenBtn.grid(row=0, column=0, padx=20, pady=5)
on_fwButton = tkinter.Button(root, text="FORWARD", width=15, command=turn_on_fw)
on_fwButton.grid(row=1, column=0, pady=5, padx= 20)

on_bwButton = tkinter.Button(root, text="BACKWARD", width=15, command=turn_on_bw)
on_bwButton.grid(row=1, column=1)
offButton = tkinter.Button(root, text="TURN OFF", width=15, command=turn_off)
offButton.grid(row=2, column=0, pady=5)
partHomeButton = tkinter.Button(root, text="PART HOME POS", width=15, command=home_part)
partHomeButton.grid(row=2, column=1, pady=5)
speedLabel = tkinter.Label(root, text="MOTOR SPEED")
speedLabel.grid(row=3, column=0)
current_value = tkinter.DoubleVar
slider = tkinter.Scale(root, from_=100, to=1000, orient='horizontal', variable=current_value, command=slider_change)
slider.grid(row=3, column=1, pady=20, padx=50)
materialLabel = tkinter.Label(root, text="MATERIAL NUMBER")
materialLabel.grid(row=4, column=0)
materialEntry = tkinter.Entry(root, width= 17)
materialEntry.grid(row=4, column=1)
materialEntry.config(justify="center")
materialEntry.focus()
position_label = tkinter.Label(root, text="POSITION")
position_label.grid(row=5, column=0)
entry_pos = tkinter.Entry(root, width= 17)
entry_pos.grid(row=5, column=1)
entry_pos.config(justify="center")
jog_fwButton = tkinter.Button(root, text="JOG-FW MACHINE", width=15)
jog_fwButton.grid(row=6, column=0, pady=10)
jog_fwButton.bind('<ButtonPress-1>', jogMotorFWR)
jog_fwButton.bind('<ButtonRelease-1>', stopJogMotorR)
jog_bwButton = tkinter.Button(root, text="JOG-BW MACHINE", width=15)
jog_bwButton.grid(row=6, column=1, pady=10)
jog_bwButton.bind('<ButtonPress-1>', jogMotorBWR)
jog_bwButton.bind('<ButtonRelease-1>', stopJogMotorR)
saveButton = tkinter.Button(root, text="SET UP PROGRAM", width=15, command=setProgram)
saveButton.grid(row=7, column=0)
runProgramButton = tkinter.Button(root, text="RUN PROGRAM", width=15, command=runProgram)
runProgramButton.grid(row=7, column=1)
root.after(500,Flashing)
root.after(100, showing_pos)
root.mainloop()


