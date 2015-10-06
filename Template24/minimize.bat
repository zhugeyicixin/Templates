@echo off
python _a_PM6FromInitialGjf.py
python _b_gjfFromLog.py
python _c_confSearchFromGjf.py
python _d_PM6FromConfSearch.py
python _e_B3YPFromPM6.py
python _f_lowestEnergyFromB3LYP.py
python _g_SPEnergyFromOpt.py
pause