from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill, intent_handler
from mycroft.util.log import LOG, getLogger

import time
import os
import subprocess, signal

from multiprocessing import Process

def processRunning(name):
	return len(pgrep(name)) > 0


def pgrep(pattern):
    args = ["pgrep", str(pattern)]
    out = os.popen(" ".join(args)).read().strip()
    return list(map(int, out.splitlines()))


def stopProcess(name):
	pid = pgrep("-o -f " + name)[0]
	os.kill(pid, signal.SIGINT)
		
	c = 0
	while c < 50:
		if processRunning(name):
			time.sleep(.1)
			c += 1
		else:
			c = 100
	
	if processRunning(name):
		pids = pgrep(name)
		for pid in pids:
			os.kill(pid, signal.SIGKILL)


def AlexaTimer():
	print("30 seconds")
	time.sleep(10)
	print("20 seconds")
	time.sleep(10)
	print("10 seconds")
	time.sleep(10)

	stopProcess('AlexaPi')


__author__ = 'illusivedmg'
LOGGER = getLogger(__name__)

class AlexaSkill(MycroftSkill):
	def __init__(self):
		MycroftSkill.__init__(self)

	@intent_handler(IntentBuilder("").require("Alexa").optionally("Suggest"))

	def handle_start_game_intent(self, message):
		self.speak_dialog("ok")
		time.sleep(2)
		# timeout = time.time() + 30
		stopProcess('mycroft.client.speech')
		stopProcess('mycroft.audio')

		p0 = Process(target=AlexaTimer)
		p0.start()

		subprocess.call(["python3", "/opt/AlexaPi/src/main.py"])
		p0.join()
		
		#python3 -m ${_module} $_params >> /var/log/mycroft/${1}.log 2>&1 &
		# subprocess.call(["python3", "-m", "mycroft.audio", ">>", "/var/log/mycroft/audio.log", "2>&1", "&"])
		os.system("python3 -m mycroft.audio >> /var/log/mycroft/audio.log 2>&1 &")
		os.system("python3 -m mycroft.client.speech >> /var/log/mycroft/voice.log 2>&1 &")
		# subprocess.call(["python3", "-m", "mycroft.client.speech", ">>", "/var/log/mycroft/voice.log", "2>&1", "&"])
		# subprocess.call(["python3", "-m", "mycroft.client.speech", "&"]), 
		

def create_skill():
	return AlexaSkill()
