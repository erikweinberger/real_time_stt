<p align="center">
  <h2 align="center">real time speach to text (STT) with http calls</h2>
</p>

Set up:
Clone repository
git clone <link>

set up virtual enviroment use python 3.9 (3.12 not supported)\\
python3.9 -m venv <$PATH>
source <$PATH>/bin/activate

pip install -r requierments.txt

Then start server in terminal window
python server.py 
Will take a while first time since dowloading model

Start client
python client.py
