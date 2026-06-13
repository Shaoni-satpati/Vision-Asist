import pyttsx3
import queue
import threading
import time
from config import config

class Narrator:
    def __init__(self):
        self._queue = queue.Queue()
        self._last_said: dict[str, float] = {}   # label -> last narration time
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def _run(self):
        engine = pyttsx3.init()
        engine.setProperty("rate", config.TTS_RATE)
        engine.setProperty("volume", config.TTS_VOLUME)
        while True:
            text = self._queue.get()
            if text is None:   # shutdown signal
                break
            engine.say(text)
            engine.runAndWait()

    def narrate(self, label: str, distance_m: float | None):
        now = time.monotonic()
        last = self._last_said.get(label, 0.0)
        
        if now - last < config.TTS_COOLDOWN_SEC:
            return
            
        self._last_said[label] = now
        
        if distance_m is not None:
            text = f"{label}, approximately {distance_m:.1f} metres away"
        else:
            text = f"{label} detected"
            
        self._queue.put(text)

    def shutdown(self):
        self._queue.put(None)
