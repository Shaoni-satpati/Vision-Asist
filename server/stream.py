from flask_sock import Sock
from core.pipeline import Pipeline
import threading

_pipeline: Pipeline | None = None
_lock = threading.Lock()

def get_pipeline() -> Pipeline:
    global _pipeline
    with _lock:
        if _pipeline is None:
            _pipeline = Pipeline()
    return _pipeline

def register_stream(app, sock: Sock):
    @sock.route("/stream")
    def stream(ws):
        pipeline = get_pipeline()
        while True:
            frame_bytes = pipeline.process_frame()
            if frame_bytes:
                ws.send(frame_bytes)
