@echo off
for %%c in (*.dat) do thermo %%c
if not exist thermoOutput mkdir thermoOutput
for %%c in (*.out) do move %%c thermoOutput