import time
from unittest.mock import patch
from core.narrator import Narrator
from config import config

@patch("pyttsx3.init")
def test_narrator(mock_init):
    n = Narrator()
    n.narrate("chair", 1.5)
    
    # Needs a small delay as thread runs asynchronously
    time.sleep(0.1)
    
    assert "chair" in n._last_said
    
    last_time = n._last_said["chair"]
    n.narrate("chair", 1.5)
    assert n._last_said["chair"] == last_time
    
    n.shutdown()
