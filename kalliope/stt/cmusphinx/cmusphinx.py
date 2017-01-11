import speech_recognition as sr

from kalliope.core import Utils
from kalliope.stt.Utils import SpeechRecognition


class Cmusphinx(SpeechRecognition):

    def __init__(self, callback=None, **kwargs):
        """
        Start recording the microphone and analyse audio with CMU sphinx api
        :param callback: The callback function to call to send the text
        :param kwargs:
        """
        SpeechRecognition.__init__(self)

        # callback function to call after the translation speech/tex
        self.callback = callback

        # start listening in the background
        self.stop_listening = self.start_listening(self.sphinx_callback)

    def sphinx_callback(self, recognizer, audio):
        """
        called from the background thread
        """
        try:
            captured_audio = recognizer.recognize_sphinx(audio)
            Utils.print_success("Sphinx Speech Recognition thinks you said %s" % captured_audio)
            self._analyse_audio(captured_audio)

        except sr.UnknownValueError:
            Utils.print_warning("Sphinx Speech Recognition could not understand audio")
            # callback anyway, we need to listen again for a new order
            self._analyse_audio(audio=None)
        except sr.RequestError as e:
            Utils.print_danger("Could not request results from Sphinx Speech Recognition service; {0}".format(e))
            # callback anyway, we need to listen again for a new order
            self._analyse_audio(audio=None)

    def _analyse_audio(self, audio):
        """
        Confirm the audio exists and run it in a Callback
        :param audio: the captured audio
        """
        if self.callback is not None:
            self.callback(audio)
