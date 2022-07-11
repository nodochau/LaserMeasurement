import serial, time
import tkinter

arduino = serial.Serial("COM3")
arduino.baudrate = 9600
#time.sleep(2)

def write_to_arduino(in_put):
    arduino.write(in_put.encode())

def turnOn():
    write_to_arduino('o')

def turnOff():
    write_to_arduino('q')

root = tkinter.Tk()
root.title('TURN ON/OFF')
root.geometry('400x300')
onBtn = tkinter.Button(root, text='TURN ON', command=turnOn)
onBtn.grid(row=0, column=0)
offBtn = tkinter.Button(root, text='TURN OFF', command=turnOff)
offBtn.grid(row=0, column=1)
root.mainloop()