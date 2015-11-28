@echo off
python extractData.py
python getThermoInput.py
python runThermo.py
python getReverseThermoInput.py
python runReverseThermo.py
pause