from logging import raiseExceptions
import tkinter
from tkinter import *
from tkinter import messagebox
from turtle import pen
from numpy import imag
import serial, time
import tkinter
from tkinter import *
import pandas as pd
import buttonClass

red = 'red.png'
green = 'green.png'
dataFile = 'InventoryData.csv'

positionIndex = 0 # the position that read from data list
arduino = serial.Serial("COM3")
arduino.baudrate = 9600
time.sleep(2)
line = "" # variable to store command send from arduino
previousMaterial = '' 
redFlashSignal = 0
greenFlashSignal = 0
homeBtnFlashSignal = 0

def disable_closing_window():
    # this function to bypass the Close window event. So not able to close window
    pass

def jogMotorFWRoot(obj, cmd):
    obj.focus()
    #cmd = 'j'
    write_to_arduino(cmd)

# def jogMotorBWRoot(obj):
#   obj.focus()
#   cmd = 'k'
#   write_to_arduino(cmd)

def stopJogMotorRoot(obj, cmd):
    obj.focus()
    #cmd = 'n'
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

  def jogXPlus(event):
    jogMotorFWRoot(pxEntry, 'j')
   
  def jogXMinus(event):
    jogMotorFWRoot(pxEntry, 'k')

  def jogYPlus(event):
    jogMotorFWRoot(pyEntry, 'i')
   
  def jogYMinus(event):
    jogMotorFWRoot(pyEntry, 'l')

  def jogXYPlus(event):
    jogMotorFWRoot(pxEntry, 'e')

  def jogXMinusYPlus(event):
    jogMotorFWRoot(pxEntry, 'v')

  def jogXYMinus(event):
    jogMotorFWRoot(pxEntry, 'u')

  def jogXPlusYMinus(event):
    jogMotorFWRoot(pxEntry, 'w')
    
  def stopJogMotor(event):
    stopJogMotorRoot(partHomeButton, 'n')
    
  def writeData(mat, xpos, ypos):
    global dataFile
    # dataFile = matEntry.get() + ".csv"
    try:
        with open(dataFile, 'r') as rf:
            rf.readline()
    except FileNotFoundError:
        with open(dataFile, 'a') as wf:
            print('MATERIAL', 'XPOS', 'YPOS', sep=',', file=wf)
            print(mat, xpos, ypos, sep=',', file=wf)
    else:
        with open(dataFile, 'a') as wf:
            print(mat, xpos, ypos, sep=',', file=wf)
  
  def readMotorPosition(data):
      motorPos = {} # store motor positions
      xtemp = ''
      ytemp = ''
      xPos = data.find('X')
      yPos = data.find('Y')
      
      if ((xPos >= 0) and (yPos >= 0)):
          for i in range(xPos+1, yPos):
              xtemp += data[i]
          for y in range(yPos+1, len(data)):
              ytemp += data[y]
          motorPos['X'] = xtemp
          motorPos['Y'] = ytemp
          return motorPos
      else:
          if (xPos == -1 and yPos >= 0):
              for i in range(yPos+1, len(data)):
                  ytemp += data[i]
              motorPos['Y'] = ytemp
              return motorPos
          else:
              if (yPos == -1 and xPos >= 0):
                  for i in range(xPos+1, len(data)):
                      xtemp += data[i]
                  motorPos['X'] = xtemp
                  return motorPos
              else:
                  motorPos = {}
                  return motorPos 

  def savePosition():
    mat = matEntry.get()
    if (mat == ""):
      messagebox.showerror("DATA INPUT ERROR", 'MATERIAL CAN NOT BE BLANK')
    else:
      xpos = pxEntry.get()
      ypos = pyEntry.get()
      writeData(mat, xpos, ypos)

  def finishSetup():
    # cmd = 'b'
    # write_to_arduino(cmd)
    materialEntry.delete(0, tkinter.END)
    materialEntry.insert(0, matEntry.get())
    entry_pos.delete(0, tkinter.END)
    entry_pos.insert(0, '0')
    entry_posY.delete(0, tkinter.END)
    entry_posY.insert(0, '0')
    mainWindow.after_cancel(showing_position)
    mainWindow.after_cancel(flashHomeBtn)
    mainWindow.destroy()
    root.wm_state('normal')
    
  def flashHomeBtn():
    global homeBtnFlashSignal
    if homeBtnFlashSignal == 1:
      homeButton.config(background='#ffcead')
      homeButton.after(100, lambda: homeButton.config(background='#3d84b8'))
    if homeBtnFlashSignal == 0:
      homeButton.config(background=originalColor)
    if (pxEntry.get() == '0' and pyEntry.get() == '0'):
      homeBtnFlashSignal = 0
      homeButton.config(background=originalColor)
    mainWindow.after(500, flashHomeBtn)

  def showing_position():
    global line, redFlashSignal, greenFlashSignal, homeBtnFlashSignal, positionIndex
    if arduino.inWaiting()>0:
        line = str(arduino.readline().decode("utf-8"))
        line = line.strip()
        if (len(line) >= 2):
          
          myMotorXY = readMotorPosition(line)
          if (len(myMotorXY) == 2):
            pxEntry.delete(0, tkinter.END)
            pxEntry.insert(0, myMotorXY['X'])
            pyEntry.delete(0, tkinter.END)
            pyEntry.insert(0, myMotorXY['Y'])
          else:
            if (len(myMotorXY) == 1):
              if ('X' in line):
                pxEntry.delete(0, tkinter.END)
                pxEntry.insert(0, myMotorXY['X'])
              else:
                pyEntry.delete(0, tkinter.END)
                pyEntry.insert(0, myMotorXY['Y'])
    else:
      pass     
    mainWindow.after(100, showing_position)

  mainWindow = tkinter.Tk()
  mainWindow.title('SET UP PROGRAM')
  locateGUI(mainWindow, 550, 450)
  arr_00 = 'arr00.png'
  arr_90 = 'arr90.png'
  arr_90minus = 'arr-90.png'
  arr_180 = 'arr180.png'
  arr_30minus = 'arrow-30.png'
  arr_120minus = 'arrow-120.png'
  arr_120 = 'arrow120.png'
  arr_30 = 'arrow.png'
  arr_00Btn = PhotoImage(file=arr_00, width=60, height=60)
  arr_90Btn = PhotoImage(file=arr_90, width=60, height=60)
  arr_90minusBtn = PhotoImage(file=arr_90minus, width=60, height=60)
  arr_30minusBtn = PhotoImage(file=arr_30minus, width=60, height=60)
  arr_180Btn = PhotoImage(file=arr_180, width=60, height=60)
  arr_120minusBtn = PhotoImage(file=arr_120minus, width=60, height=60)
  arr_120Btn = PhotoImage(file=arr_120, width=60, height=60)
  arr_30Btn = PhotoImage(file=arr_30, width=60, height=60)
  mainWindow.protocol('WM_DELETE_WINDOW', disable_closing_window)
  matLabel = tkinter.Label(mainWindow, text='MATERIAL NUMBER')
  matLabel.grid(row=0, column=0, padx=40, pady=15)
  matEntry = tkinter.Entry(mainWindow, width=20)
  matEntry.config(justify='center')
  matEntry.focus()
  matEntry.grid(row=0, column=1)
  pxLabel = tkinter.Label(mainWindow, text='X-POSITION')
  pxLabel.grid(row=1, column=0, padx=40)
  pxEntry = tkinter.Entry(mainWindow, width=20)
  pxEntry.grid(row=1, column=1)
  pxEntry.config(justify='center')
  pyLabel = tkinter.Label(mainWindow, text='Y-POSITION')
  pyLabel.grid(row=2, column=0, padx=40, pady=10)
  pyEntry = tkinter.Entry(mainWindow, width=20)
  pyEntry.grid(row=2, column=1)
  pyEntry.config(justify='center')
  partHomeButton = tkinter.Button(mainWindow, text="HOME PART POS", width=15, command=home_part)
  partHomeButton.grid(row=3, column=0, pady=20,)
  saveButton = tkinter.Button(mainWindow, text="SAVE PSOSITION", width=15, command=savePosition)
  saveButton.grid(row=3, column=1)
  finishButton = tkinter.Button(mainWindow, text="FINISH SETUP", width=15, command=finishSetup)
  finishButton.grid(row=4, column=1)
  homeButton = tkinter.Button(mainWindow, text="HOME MACHINE", width=15, command=home_machine)
  homeButton.grid(row=4, column=0)
  originalColor = homeButton.cget("background")
  frame = tkinter.Frame(mainWindow)
  frame.grid(row=5, column=0, columnspan=2)
  jogMotor1XPlus = buttonClass.MyButtons(frame,'X+', 2, 4, 10, 10, width=10)
  jogMotor1XPlus.bind('<ButtonPress-1>', jogXPlus)
  jogMotor1XPlus.bind('<ButtonRelease-1>', stopJogMotor)
  jogMotor1XMinus = buttonClass.MyButtons(frame,'X-', 2, 0, 30, 10, width=10)
  jogMotor1XMinus.bind('<ButtonPress-1>', jogXMinus)
  jogMotor1XMinus.bind('<ButtonRelease-1>', stopJogMotor)
  jogMotor2YPlus = buttonClass.MyButtons(frame,'Y+', 0, 2, 10, 10, width=10)
  jogMotor2YPlus.bind('<ButtonPress-1>', jogYPlus)
  jogMotor2YPlus.bind('<ButtonRelease-1>', stopJogMotor)
  jogMotor2YMinus = buttonClass.MyButtons(frame,'Y-', 4, 2, 10, 10, width=10)
  jogMotor2YMinus.bind('<ButtonPress-1>', jogYMinus)
  jogMotor2YMinus.bind('<ButtonRelease-1>', stopJogMotor)
  jogMotor45 = buttonClass.MyButtons(frame,'X+Y+', 1, 3, 10, 10, width=10)
  jogMotor45.bind('<ButtonPress-1>', jogXYPlus)
  jogMotor45.bind('<ButtonRelease-1>', stopJogMotor)
  jogMotor135 = buttonClass.MyButtons(frame,'X-Y+', 1, 1, 10, 10, width=10)
  jogMotor135.bind('<ButtonPress-1>', jogXMinusYPlus)
  jogMotor135.bind('<ButtonRelease-1>', stopJogMotor)
  jogMotor225 = buttonClass.MyButtons(frame,'X-Y-', 3, 1, 10, 10, width=10)
  jogMotor225.bind('<ButtonPress-1>', jogXYMinus)
  jogMotor225.bind('<ButtonRelease-1>', stopJogMotor)  
  jogMotor315 = buttonClass.MyButtons(frame,'X+Y-', 3, 3, 10, 10, width=10)
  jogMotor315.bind('<ButtonPress-1>', jogXPlusYMinus)
  jogMotor315.bind('<ButtonRelease-1>', stopJogMotor)    
  mainWindow.after(100, showing_position)
  mainWindow.after(500, flashHomeBtn)
  mainWindow.mainloop()
#---------------------------RUN PROGRAM GUI --------------------------#
def locateGUI(window, w, h):
  widthScreen = window.winfo_screenwidth()
  heightScreen = window.winfo_screenheight()
  #calculate coordinates x, y for tk root window
  x = widthScreen/2 - w/2
  y = heightScreen/2 - h/2

  window.geometry('%dx%d+%d+%d' % (w, h, x, y))

def readData(matNum):
  #dataFile = matNum + '.csv'
  try:
      with open(dataFile, 'r') as rf:
          rf.readline()
  except FileNotFoundError:
    messagebox.showerror('PROGRAM STATUS', 'Could not find the program. Please verify material number')
    return False
  else:
    xyPos = []
    dataPos = {}
    data = pd.read_csv(dataFile)
    for row in data.itertuples():
      if (row.MATERIAL == matNum):
        xyPos.append(row.XPOS)
        xyPos.append(row.YPOS)
        dataPos[row.MATERIAL] = xyPos
    if len(dataPos) > 0:
      return dataPos
    else:
      messagebox.showerror('CURRENT MATERIAL STATUS', 'Could not find the material number in database.')
      return False

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

def turn_on_bw():
  global redFlashSignal, greenFlashSignal
  if redFlashSignal == 0:
      redFlashSignal = 1
      greenFlashSignal = 0
  cmd = 'f' + str(slider.get())
  write_to_arduino(cmd)
   
def turn_off():
  global redFlashSignal, greenFlashSignal
  redFlashSignal = 0
  greenFlashSignal = 0
  cmd = 'q'
  write_to_arduino(cmd)
  
def runProgram():
  global redFlashSignal, greenFlashSignal, positionIndex, previousMaterial
  myMaterial = int(materialEntry.get())
  
  if (readData(myMaterial)):
    myMaterialPos = readData(myMaterial)
    greenFlashSignal = 1
    redFlashSignal = 0
    entry_pos.delete(0, tkinter.END)
    entry_pos.insert(0, str(myMaterialPos[myMaterial][0]))
    entry_posY.delete(0, tkinter.END)
    entry_posY.insert(0, str(myMaterialPos[myMaterial][1]))
    cmd = 'p' + 'X' + str(myMaterialPos[myMaterial][0]) + 'Y' + str(myMaterialPos[myMaterial][1])
    write_to_arduino(cmd)
    # (Output will be pX1234Y5689)

# def jogMotorFWR(event):
#   jogMotorFWRoot(entry_pos)
   
# def jogMotorBWR(event):
#   jogMotorBWRoot(entry_pos)
  
# def stopJogMotorR(event):
#   stopJogMotorRoot(partHomeButton)

# def runPartHome():
#   global redFlashSignal, greenFlashSignal
#   if greenFlashSignal == 0:
#     greenFlashSignal = 1
#     redFlashSignal = 0
#   cmd = 'm'
#   write_to_arduino(cmd)

def write_to_arduino(in_put):
    arduino.write(in_put.encode())

def slider_change(event):
    current_value = str(slider.get())

def setProgram():
  root.wm_state('iconic')
  setupProgram()

def showing_pos():
  global line, redFlashSignal, greenFlashSignal, homeBtnFlashSignal
  if arduino.inWaiting()>0:
      line = str(arduino.readline().decode("utf-8"))
      line = line.strip()
      if (line == 'a'):
        entry_pos.delete(0, tkinter.END)
        entry_pos.insert(0, '0')
      else:
        if (line == "s"):
          greenFlashSignal = 0
          #print(greenFlashSignal)
          line = ""
        else:
          if (line == "d"):
            turn_off()
            line = ""
  else:
    pass      
            
  root.after(100, showing_pos)

def exit_program():
  try:
    root.after_cancel(showing_pos)
    arduino.close()
    root.destroy()
  except:
    pass

root = tkinter.Tk()
root.title("B&G LASER PROGRAM")
locateGUI(root, 400, 380)
#arduino.open()
if arduino.isOpen():
        print("{} is connected".format(arduino.port))
root.protocol('WM_DELETE_WINDOW', disable_closing_window)

red_btn = PhotoImage(file=red, width=60, height=60)
green_btn = PhotoImage(file=green, width=60, height=60)
greenBtn = buttonClass.MyButtons(root, '', 0, 0, 20, 5, image=green_btn, border=0)
redBtn = buttonClass.MyButtons(root, '', 0, 1, 0, 5, image=red_btn, border=0)
on_fwButton = buttonClass.MyButtons(root, 'FORWARD', 1, 0, 40, 5, width=15, command=turn_on_fw)
on_bwButton = buttonClass.MyButtons(root, 'BACKWARD', 1, 1, 0, 0, width=15, command=turn_on_bw)
offButton = buttonClass.MyButtons(root, 'TURN OFF', 2, 0, 0, 5, width=15, command=turn_off)
exitbwButton = buttonClass.MyButtons(root, 'EXIT PROGRAM', 2, 1, 0, 0, width=15, command=exit_program)
# offButton = tkinter.Button(root, text="TURN OFF", width=15, command=turn_off)
# offButton.grid(row=2, column=0, columnspan=2, pady=5)
speedLabel = tkinter.Label(root, text="MOTOR SPEED")
speedLabel.grid(row=3, column=0)
current_value = tkinter.DoubleVar
slider = tkinter.Scale(root, from_=100, to=1000, orient='horizontal', width=20, variable=current_value, command=slider_change)
slider.grid(row=3, column=1, pady=20, padx=50)
materialLabel = tkinter.Label(root, text="MATERIAL NUMBER")
materialLabel.grid(row=4, column=0)
materialEntry = tkinter.Entry(root, width= 17)
materialEntry.grid(row=4, column=1, pady=5)
materialEntry.config(justify="center")
materialEntry.focus()
positionX_label = tkinter.Label(root, text="X-POSITION")
positionX_label.grid(row=5, column=0)
#entry_posX
entry_pos = tkinter.Entry(root, width= 17)
entry_pos.grid(row=5, column=1)
entry_pos.config(justify="center")
positionY_label = tkinter.Label(root, text="Y-POSITION")
positionY_label.grid(row=6, column=0)
entry_posY = tkinter.Entry(root, width= 17)
entry_posY.grid(row=6, column=1, pady=5)
entry_posY.config(justify="center")
setupButton = buttonClass.MyButtons(root, 'SETUP PROGRAM',7, 0, 0, 20, width=15, command=setProgram)
runProgramButton = buttonClass.MyButtons(root, 'RUN PROGRAM',7, 1, 0, 0, width=15, command=runProgram)
root.after(500,Flashing)
root.after(100, showing_pos)
root.mainloop()


