@echo off
python extractData.py
python getThermoInput.py
python getReverseThermoInput.py
python getThermoATM.py
python runThermo.py
python runReverseThermo.py
python collectEquilibriumConstants.py
python arrheniusFitting.py
pause