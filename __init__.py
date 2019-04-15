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
	time.sleep(30)

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

		subprocess.call(["python", "/opt/AlexaPi/src/main.py"])
		p0.join()
		
		subprocess.call(["python", "-m mycroft.audio"])
		subprocess.call(["python", "-m mycroft.client.speech"])
		

def create_skill():
	return AlexaSkill()
