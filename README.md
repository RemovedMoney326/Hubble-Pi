# Hubble-Pi
Documentation, Resources and Python Codes for portable Astrophotography and KStars Setup with Raspberry Pi 4 and HQ 12MP Camera Module
------------------------------------------------------------------------------------------------------------------------
#Introduction and Motivation
------------------------------------------------------------------------------------------------------------------------
First of all, hello and thank you for your interest in my Github repository about this little project of mine! 
My name is Santiago Rodriguez and I'm the creator of this homebrewed telescope imaging and skyguiding system 
I decided to call Hubble Pi after the american astronomer Edwin Hubble, whose work in the field of 
extragalactic astronomy and observational cosmolgy provided some of the first evidence of the universes expansion, 
as well as the Hubble Space Telescope also named in his honour, which has produced some of the most breathtaking 
images of the cosmos during its service lifetime and is due to be succeeded by the James Webb Telescope due to be
launched next year. 

Since I'm currently a physics student with a very huge interest in astrophysics, I'd wanted to work on a way to capture 
images/recordings with my telescope as well as easily finding objects in the night sky since a long time. Having recently 
taken up an introduction to astrophysics as a winter semester lecture and after getting started this year with Linux as 
well as Python, I recently came up with the idea of making such a setup with the Raspberry Pi 4 and the newly released 
HQ 12Mp camera module an esteemed friend of mine told me about. 

This was ideal, since the Raspberry Pi also has the future potential of being programmed for autoguiding as well as doing 
amateur stellar spectroscopy with the camera module and filters like the Star Analyser 100 due to being able to output the 
camera readings directly as Raw Bayer data captures or the more numerical YUV raw format for processing with spectrography 
software. In addition, the ability to fully and manually control the camera module using Python, with its high quality and 
high resolution Sony IMX477 sensor, meant these kind of applications would definitely be viable and highly adaptable for 
conventional astrophotography too thanks to the flexibility of the Picamera package as well as Python for scientific and 
numerical applications.

------------------------------------------------------------------------------------------------------------------------
#Github Repository Structure
------------------------------------------------------------------------------------------------------------------------
This GitHub repository contains all the code and relevant files I used in order to set up the software for the Hubble Pi.
A full documentation is available in the form of a LaTeX PDF document above. The AstroCam Python source code at the core 
of the Hubble Pi's camera functionality is also available, with the ability to make pull request for improvements on the 
code. Should any questions or problems with any of the content here arise, feel free to write it in the issues section 
or message me directly and I will try my best to address them as soon as possible.

I hope this repo can be helpful to anyone trying to build a similar project and become a useful source of information on
doing entry level Astrophotography with the Raspberry Pi :)

------------------------------------------------------------------------------------------------------------------------
#Update Log
------------------------------------------------------------------------------------------------------------------------
13.7.2020 - Changed the preview camera stream to use the picamera videoport option for stability on older Raspberry Pi models 
