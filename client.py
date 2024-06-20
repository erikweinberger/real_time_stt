import requests
import speech_recognition as sr
import threading
from queue import Queue
import time

url = 'http://127.0.0.1:5000'
user_id = '123'

def main():
    transcription_queue = Queue()

    def record_callback(recognizer, audio):
        """
        Callback function to handle audio data after recording.
        """
        try:
            # Convert AudioData to raw bytes
            audio_data = audio.get_raw_data(convert_rate=16000, convert_width=2)
            # Send audio data to server for transcription
            response = requests.post(url + '/receive_data', files={'file': audio_data}, data={'id': user_id})
            # Append transcription to queue
            transcription_queue.put(response.json()['Transcription'])
        except Exception as e:
            print(f"Error during transcription: {e}")

    # Initialize recognizer and microphone
    recognizer = sr.Recognizer()
    microphone = sr.Microphone(sample_rate=16000)

    # Adjust for ambient noise
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)

    # Start listening in the background
    stop_event = threading.Event()
    stop_listening = recognizer.listen_in_background(microphone, record_callback, phrase_time_limit=5)

    try:
        while not stop_event.wait(1):
            # Process transcriptions from the queue
            while not transcription_queue.empty():
                transcription = transcription_queue.get()
                print(f"Transcription: {transcription}")
    except KeyboardInterrupt:
        stop_listening(wait_for_stop=False)
        stop_event.set()

if __name__ == "__main__":
    # Start recording on the server side
    data = {'id': user_id}
    response = requests.post(url + "/record", data=data)
    if response.status_code != 200:
        print(f"Failed to start recording: {response.json()['message']}")
        exit()

    # Start main function
    main()

    # End recording on the server side
    requests.post(url + '/end_record', data=data)
