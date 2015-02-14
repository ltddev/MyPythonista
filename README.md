# MyPythonista
All Pythonista apps and coding

## PythonistaClockGadget
When I'm happily coding away on stuff I always seem to lose track of time and even though I can see the digital clock on the upper status area of my iPad I like to look at an analog clock like a widget on Windows and marvel at a smooth second hand. I have also been experimenting with redering svg graphics in Pythonista to create some very cool, smooth transitions so I created a very simple "Pythonista Gadget" to constantly view the time on a smooth second handed analog clock that I present As"sidebar" which lets me continue to use the live editor and even run other Python at the the prompt. Nothing fancy -- I never was a "ui guy", my expertise was on the back end, and the ui could use work -- but it it is practical for my personal use.

It also has the ability to speak the time and location on demand.

I was working on making this a "talking clock" which was my original intention. I had controls to choose whether or not to announce the time, if so the duration between announcements and so on but I simply could not get a background thread going to do what I wanted to. Any suggestions on how to add a background task to poll for current time and then do something about it on a given schedule - in the Pythonista environment, and in Python -- would be helpful to finish this goal.

See: http://omz-forums.appspot.com/pythonista/post/6162554669760512
