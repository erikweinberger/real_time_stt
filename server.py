from flask import Flask, request, jsonify
import asyncio
import os
from transcriber import WhisperTranscriber
import sys

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/receive_data', methods=['POST'])
async def recive_data():
    if 'file' not in request.files or 'id' not in request.form:
        return jsonify({"message": "Missing file or id"}), 400

    file = request.files['file']
    user_id = request.form['id']

    trans = await WhisperTranscriber.transcribe(user_id, file)
    app.logger.info(trans)
    return jsonify({"message": "File received", "Transcription": trans, "id": user_id})




@app.route('/record', methods=['POST'])
def record():
    if 'id' not in request.form:
        return jsonify({"message": "Missing file or id"}), 400
    user_id = request.form['id']

    sucess = WhisperTranscriber.start_transcribe(user_id)

    return jsonify({"sucess": sucess,"id": user_id})




@app.route('/end_record', methods=['POST'])
async def end_record():
    if 'id' not in request.form:
        return jsonify({"message": "Missing file or id"}), 400
    user_id = request.form['id']

    sucess = WhisperTranscriber.end_transcribe(user_id)

    return jsonify({"sucess": sucess,"id": user_id})

if __name__ == '__main__':
    app.run(debug=True)
