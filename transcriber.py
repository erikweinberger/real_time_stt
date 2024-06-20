import asyncio
import queue
import sys
import threading
import numpy as np
from typing import Dict

import whisper
import torch

users = {}

class WhisperTranscriber:
    model = whisper.load_model("base.en")



    @staticmethod
    async def transcribe(id, file):
        loop = asyncio.get_event_loop()
        audio_data = await loop.run_in_executor(None, file.read)
        audio_np = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32) / 32768.0
        res = await loop.run_in_executor(None, WhisperTranscriber.model.transcribe, audio_np)
        return res['text']

    @staticmethod
    def start_transcribe(user_id):
        users[user_id] = ""
        return user_id in users

    @staticmethod
    def end_transcribe(user_id):
        users.pop(user_id)
        return user_id not in users


