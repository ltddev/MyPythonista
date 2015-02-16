# coding: utf-8
import ui, speech, console
svgInHtml='''
<?xml version="1.0"?>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 400 400" width="400" height="400" version="1.0">
  <defs>
    <linearGradient id="a" x1="0%" y1="100%" x2="0%" y2="0%">
      <stop offset="0%" style="stop-color:#777799"/>
      <stop offset="100%" style="stop-color:#ffffff"/>
    </linearGradient>
    <linearGradient id="b" x1="0%" y1="100%" x2="0%" y2="0%">
      <stop offset="0%" style="stop-color:#ffffff"/>
      <stop offset="25%" style="stop-color:#b6b6cc"/>
      <stop offset="40%" style="stop-color:#515177"/>
      <stop offset="48%" style="stop-color:#ffffff"/>
      <stop offset="56%" style="stop-color:#ffffff"/>
      <stop offset="75%" style="stop-color:#8b8baa"/>
      <stop offset="98%" style="stop-color:#efeff4"/>
      <stop offset="100%" style="stop-color:#fbfbfc"/>
    </linearGradient>
    <linearGradient id="c" x1="0%" y1="100%" x2="0%" y2="0%">
      <stop offset="0%" style="stop-color:#ffffff"/>
      <stop offset="100%" style="stop-color:#777799"/>
    </linearGradient>
    <radialGradient id="d" cx="50%" cy="50%" r="50%" fx="50%" fy="50%">
      <stop offset="0%" style="stop-color:#ffffff"/>
      <stop offset="40%" style="stop-color:#ffffff"/>
      <stop offset="70%" style="stop-color:#e6e6ee"/>
      <stop offset="92%" style="stop-color:#b6b6cc"/>
      <stop offset="100%" style="stop-color:#636388"/>
    </radialGradient>
    <radialGradient id="e" cx="50%" cy="150%" r="200%" fx="50%" fy="150%">
      <stop offset="0%" style="stop-color:#ffffff;stop-opacity:0"/>
      <stop offset="59%" style="stop-color:#ffffff;stop-opacity:0"/>
      <stop offset="60%" style="stop-color:#ffffff;stop-opacity:0.6"/>
      <stop offset="70%" style="stop-color:#ffffff;stop-opacity:0.3"/>
      <stop offset="100%" style="stop-color:#ffffff;stop-opacity:0.0"/>
    </radialGradient>
  </defs>
  <g transform="translate(200 200)">
    <circle cx="0" cy="0" r="200" fill="#cecedd"/>
    <circle cx="0" cy="0" r="196" stroke="url(#a)" stroke-width="5" fill="url(#b)"/>
    <circle cx="0" cy="0" r="170" stroke="url(#c)" stroke-width="4" fill="url(#d)"/>
    <circle cx="0" cy="0" r="172" stroke="#ffffff" stroke-width="0.5" fill="none"/>
    <circle cx="0" cy="0" r="193.5" stroke="#ffffff" stroke-width="0.5" fill="none"/>
    <g id="O">
      <polygon points="4,155 4,130 -4,130 -4,155" style="fill:#777799;stroke:#313155;stroke-width:1"/>
      <polygon points="4,-155 4,-130 -4,-130 -4,-155" style="fill:#777799;stroke:#313155;stroke-width:1"/>
    </g>
    <g transform="rotate(30)"><use xlink:href="#O"/></g>
    <g transform="rotate(60)"><use xlink:href="#O"/></g>
    <g transform="rotate(90)"><use xlink:href="#O"/></g>
    <g transform="rotate(120)"><use xlink:href="#O"/></g>
    <g transform="rotate(150)"><use xlink:href="#O"/></g>
    <polygon id="h" points="6,-80 6,18 -6,18 -6,-80" style="fill:#232344">
      <animateTransform id="ht" attributeType="xml" attributeName="transform" type="rotate" from="000" to="000" begin="0" dur="86400s" repeatCount="indefinite"/>
    </polygon>
    <polygon id="m" points="3.5,-140 3.5,23 -3.5,23 -3.5,-140" style="fill:#232344">
      <animateTransform id="mt" attributeType="xml" attributeName="transform" type="rotate" from="000" to="000" begin="0" dur="3600s" repeatCount="indefinite"/>
    </polygon>
    <polygon id="s" points="2,-143 2,25 -2,25 -2,-143" style="fill:#232344">
      <animateTransform id="st" attributeType="xml" attributeName="transform" type="rotate" from="000" to="000" begin="0" dur="60s" repeatCount="indefinite"/>
    </polygon>
    <circle cx="0" cy="0" r="163" fill="url(#e)"/>
  </g>
  <script type="text/javascript"><![CDATA[
    var d = new Date();
    var s = d.getSeconds();
    var m = d.getMinutes() + s/60;
    var h = (d.getHours() % 12) + m/60 + s/3600;
    document.getElementById('st').setAttribute('from',s*6);
    document.getElementById('mt').setAttribute('from',m*6);
    document.getElementById('ht').setAttribute('from',h*30);
    document.getElementById('st').setAttribute('to',360+s*6);
    document.getElementById('mt').setAttribute('to',360+m*6);
    document.getElementById('ht').setAttribute('to',360+h*30);
  ]]></script>
</svg>
'''

fmt = 'The current local time in {} is {} {} {} {}.'  # ccc: use str.format() for complex concatenation

numbersZeroToTwenty = '''zero one two three four five six seven eight nine ten eleven
    twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty'''.split()

tens_dict = { 2 : 'twenty',
              3 : 'thirty',
              4 : 'forty',
              5 : 'fifty' }
am = "A.M."
pm = "P.M."
oclock = "oclock"

# Turn off tracing when not required for simple debug/trace
traceFlag = True

speechDelay = 0.05
locale = 'en-US'
#==============================================================================
class ClockGadget:
	def __init__(self):
		view = ui.load_view()
		
		# Set announce duration to a default of once per every 15 minutes.
		#view['rootview']['announceFreqTextfield'].text = '15'
		#view['rootview']['announceFreqSlider'].value = .25 # every 1/4 hour.
		
		# cache away the current location (if location services on for Pythonista)
		self.locationString = self.createCurrentLocationString()
		
		if traceFlag: print 'location string in __init__ is ->>' + self.locationString
		
		webview = view['rootview']['webview']

		# Place the analog clock in a location that is sensible for a "gadget"
		# and disable touch or multitouch gestures to prevent unwannted resizing
		# or movement to the underlying clock itself which has no need to do so.
		webview.height = 20
		webview.width = 10
		webview.frame= 15,25,120,125
		webview.multitouch_enabled = False
		webview.touch_enabled = False
		if traceFlag: print 'Presenting view now.'
		view.present('sidebar')
		if traceFlag: print 'Loading html with embedded svg now.'
		webview.load_html(svgInHtml)
#==============================================================================
	def speaknowButtonTapped(self, sender):
		assert sender.name == 'speakTimeButton', 'Invalid button name: ' + sender.name
		# Get the say seconds preference
		isSaySeconds = sender.superview['speakSecondsSwitch'].value
		if traceFlag: print 'isSaySeconds current value now->>' + str(isSaySeconds)
			
		timeMessage = self.getCurrentLocalTimeAnnouncement(isSaySeconds)
		if traceFlag: print 'Time message to announce ->>' + timeMessage
		speech.say(timeMessage,locale, speechDelay)
#=============================================================================
	def switchTapped(self,sender):
		assert sender.name == 'speakSecondsSwitch', 'Invalid switch name: ' + sender.name
		if traceFlag: print "speakSecondsSwitch tapped...current value is ->>" + str(sender.value)
#==============================================================================
	def createCurrentLocationString(self):
		import location
		location.start_updates()
		coordinates = location.get_location()
		location.stop_updates()

		try:
			addressDict = location.reverse_geocode(coordinates)[0]  # grab the first loc
			locationString = 'in {City} {Country}'.format(**addressDict)
		except (TypeError, KeyError) as e:
			if traceFlag: print('Error in createCurrentLocationString(): {}'.format(e))
			locationString = ''

		if traceFlag: print 'Returning location string ->>' + locationString
		return locationString
#==============================================================================
	def getCurrentLocalTimeAnnouncement(self, isSaySeconds):
		from datetime import datetime
		
		##todo maybe get time and pass in from another function since calc twice?
		now = datetime.now().time()
		nowHour = now.hour
		nowMinutes = now.minute
		nowSeconds = now.second

		# Get the current local hour
		hourString = self.getCurrentHourString(nowHour)
		if traceFlag: print "hourString is -->" + hourString

		# Get the local current minute
		minuteString = self.getCurrentMinutesString(nowMinutes)
		if traceFlag: print 'minuteString is ->>' + minuteString
		
		# If it is right on the hour, add "o'clock"; if not, bad English grammar to use it in this context.
		if nowMinutes == 0:
			hourString += " " + oclock  # ccc: use +=

		# If minutes less than 10 US english adds ' oh'begore saying minutes, eg. 'Two oh one'for 2:01, but make sure not to append 'owe' if its right on the hour. That is, when 'oclock' never 'owe' preventing 'nine oclock owe p.m.' phrases.
		if 0 < nowMinutes < 10:  # ccc: slight optimization if variable appears only once
			minuteString = "oh " + minuteString # Use 'oh' which is real word not to confuse speech synth.

		# Not using 24 hour system but instead a 12 hour one which uses a.m and p.m
		ampm = am if nowHour < 12 else pm

		if isSaySeconds:
			# English grammar, if seconds is 1, agrrement rules say use singular.
			seconds = "second" if nowSeconds == 1 else "seconds"
			secs_str = '{} {}'.format(nowSeconds, seconds)
		else:
			secs_str = ''
			
		announcement = fmt.format(self.locationString, hourString, minuteString, ampm, secs_str)  # ccc: use str.format() for complex concatenation
		if traceFlag: print announcement
		return announcement
#==============================================================================
	def getCurrentHourString(self, nowHour):
		if traceFlag: print "nowHour parameter to function ->>" + str(nowHour)
		assert -1 < nowHour < 24, 'Error: Invalid hour {}.'.format(nowHour)
		hourString = numbersZeroToTwenty[nowHour % 12 or 12]
		if traceFlag: print "Hour string to return ->>" + hourString
		return hourString
#==============================================================================
        def getCurrentMinutesString(self, nowMinutes):
                assert -1 < nowMinutes < 60, 'error: invalid minutes {}.'.format(nowMinutes)
                if nowMinutes == 0:  # special case for zero
                        return ''
                if nowMinutes < 21:
                        return numbersZeroToTwenty[nowMinutes]
                tens = nowMinutes / 10
                ones = nowMinutes % 10
                if ones:  # special case for zero
                        return '{} {}'.format(tens_dict[tens], numbersZeroToTwenty[ones])
                else:
                        return tens_dict[tens]
#==============================================================================
if traceFlag: console.clear()
ClockGadget()
