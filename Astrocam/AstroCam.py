#!/usr/bin/python3

"""
Created on Saturday Jun  6 10:14:33 2020

@author: Santiago Rodriguez
@based on code by Erik at http://helloraspberrypi.blogspot.com/2015/12/python-to-capture-image-from-pi-camera_17.html
"""
import picamera
import tkinter as Tkinter
import time
from PIL import ImageTk, Image
from threading import Thread
from tkinter import ttk
import io
import sys

RQS_0=0
RQS_QUIT=1
RQS_CAPTURE=2
RQS_RECORD=3
rqs=RQS_0

def camHandler():
    global rqs
    rqs = RQS_0
    
    camera = picamera.PiCamera()
    #stream = io.BytesIO()

    #set default
    camera.sharpness = 0
    camera.contrast = 0
    camera.brightness = 50
    camera.saturation = 0
    camera.ISO = 0
    camera.video_stabilization = False
    camera.shutter_speed = camera.exposure_speed
    camera.exposure_mode = 'auto'
    camera.awb_mode = 'auto'
    camera.meter_mode = 'average'
    camera.exposure_compensation = 0
    camera.image_effect = 'none'
    camera.color_effects = None
    camera.rotation = 270
    camera.hflip = False
    camera.vflip = False
    camera.crop = (0.0, 0.0, 1.0, 1.0)
    camera.resolution = (350, 300)
    DynamicCaptureResolution = (4056,3040) #default camera resolution
    RecordingResolution = (1920,1080) #default recording resolution
    #recording default
    recording_duration = 0
    #end of set default
    #camera.start_preview()

    while rqs != RQS_QUIT:
        if rqs == RQS_CAPTURE:
            print("Capture")
            rqs=RQS_0
            camera.resolution = DynamicCaptureResolution    #set photo size
            time.sleep(2)                                   #sensor adjustment
            camera.shutter_speed = int(scaleShutterSpeed.get()*10e4) #set exposure time/shutter speed
            camera.exposure_mode = 'off'                    #fix exposure
            g = camera.awb_gains                            #fix white balance
            camera.awb_mode = 'off'
            camera.awb_gains = g
            if recording_duration==1:
              timeStamp = time.strftime("%Y%m%d-%H%M%S")
              #jpgFile='/home/pi/Pictures/Astrophotography/JPG/img_'+timeStamp+'.jpg' #uncomment alongside line 72 for RAW ad JPG capture
              rawFile='/home/pi/Pictures/Astrophotography/RAW/img_'+timeStamp+'.rgb'
              #camera.capture(jpgFile)
              camera.capture(rawFile, format='rgb')
              labelCapVal.set('Picture taken!')
            else:
                camera.start_preview()
                timeStamp = time.strftime("%Y%m%d-%H%M%S")
                camera.capture_sequence(['/home/pi/Pictures/Astrophotography/RAW/img_'+timeStamp+'seq_%04d.rgb' % i for i in range(recording_duration)], format='rgb')                
                #uncomment the for loop below and delete lines 77-78 for JPG and RAW capture
                #for i in range(0,recording_duration,1):
                    #timeStamp = time.strftime("%Y%m%d-%H%M%S")
                    #jpgFile='/home/pi/Pictures/Astrophotography/JPG/img_'+timeStamp+'.jpg'
                    #rawFile='/home/pi/Pictures/Astrophotography/RAW/img_'+timeStamp+'.rgba'
                    #camera.capture(jpgFile)
                    #camera.capture(rawFile, format='rgba')
                camera.stop_preview()
                labelCapVal.set('Picture Row taken!')
            camera.exposure_mode = 'auto'
            camera.awb_mode = 'auto'
            camera.shutter_speed = camera.exposure_speed
            camera.resolution = (350, 300)      #resume preview size
        if rqs == RQS_RECORD:
            print("Record")
            rqs=RQS_0
            timeStamp = time.strftime("%Y%m%d-%H%M%S")
            h264File='/home/pi/Pictures/Astrophotography/H264/recording_'+timeStamp+'.h264'
            camera.resolution = RecordingResolution
            camera.framerate = 30
            camera.start_preview()
            camera.start_recording(h264File)
            camera.wait_recording(recording_duration)
            camera.stop_recording()
            camera.stop_preview()
            camera.resolution = (350, 300)      #resume preview size
            labelCapVal.set('Recording done!')
        else:
            #set parameter
            #camera.shutter_speed = camera.exposure_speed
            DynamicCaptureResolution = (int(4056/scaleBinning.get()),int(3040/scaleBinning.get()))
            camera.ISO = scaleISO.get()
            recording_duration = scaleRecordingDuration.get()
            camera.sharpness = scaleSharpness.get()
            camera.contrast = scaleContrast.get()
            camera.brightness = scaleBrightness.get()
            camera.saturation = scaleSaturation.get()
            stream = io.BytesIO()
            camera.capture(stream, format='jpeg')
            stream.seek(0)
            tmpImage = Image.open(stream)
            tmpImg = ImageTk.PhotoImage(tmpImage)
            previewPanel.configure(image = tmpImg)
            #sleep(0.5)
                
    print("Quit")        
    #camera.stop_preview()
    
def startCamHandler():
    camThread = Thread(target=camHandler)
    camThread.start()

def quit():
    global rqs
    rqs=RQS_QUIT

    global tkTop
    tkTop.destroy()

def capture():
    global rqs
    rqs = RQS_CAPTURE
    labelCapVal.set("Capturing")

def record():
    global rqs
    rqs = RQS_RECORD
    labelCapVal.set("Recording")

tkTop = Tkinter.Tk()
tkTop.wm_title("Settings")
tkTop.geometry("130x300+350+0")

previewWin = Tkinter.Toplevel(tkTop)
previewWin.title('AstroCam')
previewWin.geometry('350x300+1+0')
previewPanel = Tkinter.Label(previewWin)
previewPanel.pack(side = "bottom", fill = "both", expand = "yes")

tkBottom = Tkinter.Toplevel(tkTop)
tkBottom.wm_title("Advanced Settings")
tkBottom.geometry("610x300+0+330")

tkButtonQuit = Tkinter.Button(
    tkTop, text="Quit", command=quit)
tkButtonQuit.pack(padx=0, pady=0, side=Tkinter.TOP)

tkButtonCapture = Tkinter.Button(
    tkTop, text="Capture", command=capture)
tkButtonCapture.pack(padx=0, pady=0, side=Tkinter.TOP)

tkButtonRecord = Tkinter.Button(
    tkTop, text="Record", command=record)
tkButtonRecord.pack(padx=0, pady=0, side=Tkinter.TOP)

SCALE_WIDTH = 130;
SCALE_LENGHT = 250
labelCapVal = Tkinter.StringVar()
Tkinter.Label(tkTop, textvariable=labelCapVal).pack()

scaleShutterSpeed = Tkinter.Scale(
    tkTop,
    from_=0, to=200,
    length=SCALE_WIDTH,
    orient=Tkinter.HORIZONTAL,
    label="ShutterSpeed")
scaleShutterSpeed.set(3)
scaleShutterSpeed.pack(anchor=Tkinter.CENTER)

scaleISO = Tkinter.Scale(
    tkTop,
    from_=100, to=800,
    length=SCALE_WIDTH,
    orient=Tkinter.HORIZONTAL,
    label="ISO")
scaleISO.set(100)
scaleISO.pack(anchor=Tkinter.CENTER)

scaleRecordingDuration = Tkinter.Scale(
    tkTop,
    from_=1, to=600,
    length=SCALE_WIDTH,
    orient=Tkinter.HORIZONTAL,
    label="Recording Length")
scaleRecordingDuration.set(1)
scaleRecordingDuration.pack(anchor=Tkinter.CENTER)

scaleBinning = Tkinter.Scale(
    tkBottom,
    from_=1, to=4,
    length=SCALE_LENGHT,
    orient=Tkinter.VERTICAL,
    label="Binning"
    )
scaleBinning.set(1)
scaleBinning.pack(side="left")


scaleSharpness = Tkinter.Scale(
    tkBottom,
    from_=-100, to=100,
    length=SCALE_LENGHT,
    orient=Tkinter.VERTICAL,
    label="Sharpness")
scaleSharpness.set(0)
scaleSharpness.pack(side="left")

scaleContrast = Tkinter.Scale(
    tkBottom,
    from_=-100, to=100,
    length=SCALE_LENGHT,
    orient=Tkinter.VERTICAL,
    label="Contrast")
scaleContrast.set(0)
scaleContrast.pack(side="left")

scaleBrightness = Tkinter.Scale(
    tkBottom,
    from_=0, to=100,
    length=SCALE_LENGHT,
    orient=Tkinter.VERTICAL,
    label="Brightness")
scaleBrightness.set(50)
scaleBrightness.pack(side="left")

scaleSaturation = Tkinter.Scale(
    tkBottom,
    from_=-100, to=100,
    length=SCALE_LENGHT,
    orient=Tkinter.VERTICAL,
    label="Saturation")
scaleSaturation.set(0)
scaleSaturation.pack(side="left")

print("Start")
startCamHandler()

Tkinter.mainloop()
