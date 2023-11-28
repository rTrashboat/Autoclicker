import sys
import math
if sys.version_info[0] >= 3:
    import PySimpleGUI as sg
else:
    import PySimpleGUI27 as sg
import pyautogui as ag
import win32api
import time
import keyboard
import multiprocessing as mp
import pynput
from pynput.keyboard import Key, Listener

def on_key_release(key,clicking_process,Button1):
    #global running
    #global clicking_process
    Button1=Button1
    if key == Key.f6:
        clicking_process.terminate()
        Button1.update("Start")
        running=False


def clicking(Hours,Minutes,Seconds,Mousebutton,Clicknumber,Keyboardbutton,Position):
    Position_list = list(Position.split(","))
    Delay = (Hours * 60 * 60 + Minutes * 60 + Seconds)


    if isinstance(Hours, float) and isinstance(Minutes, float) and isinstance(Seconds, float):
        Pressing = True
        ag.PAUSE = 0
        #ag.moveTo(Position)
        if Mousebutton == "None":
            pass
        else:
            if Mousebutton == "Left" or Mousebutton == "Right" or Mousebutton == "Middle":
                if Clicknumber == 0:
                    while Pressing:
                        try:
                            if Position!= "------>" and Position is not None and Position: 
                                ag.moveTo(int(Position_list[0]),int(Position_list[1]))
                        except ValueError:
                            pass

                        ag.click(button = Mousebutton)
                        time.sleep(Delay)
                else:
                    Clickdone = 0
                    while Pressing:
                        try:
                            if Position!= "------>" or not Position : 
                                ag.moveTo(int(Position_list[0]),int(Position_list[1]))
                        except ValueError:
                            pass

                        ag.click(button = Mousebutton)
                        Clickdone += 1
                        if Clickdone == Clicknumber:
                            exit()
                        time.sleep(Delay)

        if Keyboardbutton == "None" or Keyboardbutton == "":
            pass
        else:
            while Pressing:
                ag.write(Keyboardbutton)
                time.sleep(Delay)
    else:
        pass

def gui():
    running = False
    sg.theme("LightPurple")
    sg.set_options(icon = "icon.ico")
    
    input_size= (5,5)
    layout = [
    [sg.Text("Delay"),sg.Text("H"), sg.Input(0,key = "-Input-1", size = input_size),sg.Text("M"),sg.Input(0,key = "-Input-2", size = input_size),sg.Text("S"),sg.Input(0.1,key = "-Input-3", size = input_size),sg.Text("Number of clicks (enter 0 for infinity)"),sg.Input(0,key = "-Input-4", size = input_size, expand_x = True)],
    [sg.Text("Mouse button", expand_x = True),sg.Spin(["None", "Left", "Middle", "Right"], key = "Spin1"),sg.Text("Keyboard button"), sg.Input("None", key = "-Input-5", size = input_size),sg.Text("Failsafe (Recommended)"),sg.Spin(["Enabled","Disbled"],key = "Spin2"), sg.Text("Stop and Start key"),sg.Input("F6", key = "-Input-6", size = input_size)],
    [sg.Text("Mouse position (Leave empty for current mouse position)"),sg.Input("------>" , key = "-Input-7"),sg.Button("Detect Mouse postion", key = "Button")],
    [sg.Button("Start",key = "Button1", expand_x = True),sg.Button("Stop",key = "Button2", expand_x = True)]
    ]
    
    window = sg.Window("Autoclicker", layout)
    
    while True:

        #if keyboard.is_pressed("F6"):
        #    break
    
        event, values = window.read()
        if event == "Button":
            window["Button"].update("Wait for 5 seconds")
            Detectinginput = True
            while Detectinginput:
                time.sleep(2)
                Position = ag.position()
                #Detectinginput = False
                window["Button"].update("Detect Mouse postion")
                window["-Input-7"].update(Position)
                Detectinginput = False
        # Start listening for key releases

        elif event == "Button1" and window["Button1"].get_text() == "Start":
            try:
                Hours = float(values["-Input-1"])
                Minutes = float(values["-Input-2"])
                Seconds = float(values["-Input-3"])
                Mousebutton = values["Spin1"]
                Clicknumber = float(values["-Input-4"])
                #Position = ag.position()
                Keyboardbutton = values["-Input-5"]
                Position_raw = values["-Input-7"]
                Position = Position_raw.replace("(", "").replace(")", "")
                clicking_process = mp.Process(target=clicking,args=(Hours,Minutes,Seconds,Mousebutton,Clicknumber,Keyboardbutton,Position))
                try:
                    clicking_process.start()
                except ValueError:
                    running = False
                    window["Button1"].update("Start")

                if Mousebutton != "None" or not Mousebutton:
                    window["Button1"].update("Clicking!")
                    running = True
                    placeholder_arg = 0
                    listener = pynput.keyboard.Listener(on_release=lambda event: on_key_release(event, clicking_process=clicking_process,Button1=window["Button1"]))
                    listener.start()
    
            except ValueError:
                running = False
                window["Button1"].update("Start")
            except Exception:
                running = False
                window["Button1"].update("Start")

            #clicking_process.join()

        elif event == sg.WIN_CLOSED:
            if running:
                clicking_process.terminate()
            break
            sys.exit()

        elif event == "Button2":
            if running:clicking_process.terminate()
            running = False
            window["Button1"].update("Start")
    
    window.close()

def main():
    gui_process = mp.Process(target=gui)
    gui_process.start()
    #gui_process.join()

if __name__ == '__main__':
    main()