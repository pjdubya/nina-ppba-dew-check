# nina-ppba-dew-check

## Description

Pegasus Astro's Pocket Powerbox Advance Gen2 today makes it possible to automate the use of dew heaters for the primary OTA and guide scope based on current weather conditions. NINA makes it possible to automate nearly everything else, including whether the Powerbox Advance is enabled to control those dew heaters. Some modern astrophotography cameras also have their own dew heaters to control dew forming on the camera's lens plate, and while this is possible to enable via NINA, the Powerbox Advance can't initiate that when current weather conditions dictate. 

This project includes a python script that checks for a local Powerbox Advance running on astrophotography imaging rig (or another designated location), retrieves current temperature and humidity data, and determines whether those conditions indicate that dew is imminent. NINA advanced sequencer templates are also provided that provide an example of how this script can then be executed during an imaging sequence to enable the camera dew heater based on the current weather conditions.

## Pre-Requisites

### Hardware

- Pegasus Powerbox Advance Gen2
- Astrophotography camera that contains a dew heater such as the ZWO ASI 2600MC Pro

### Software
- Pegasus Astro
  - Install Unity Platform and TheSkyX Plugin; see [Pegasus Astro Website](https://pegasusastro.com/products/pocket-powerbox-advance-gen2)
- NINA
  - Install NINA v3 if you haven't already (see [NINA Website](https://nighttime-imaging.eu))
  - In NINA's Plugin system, install the Sequencer Powerups plugin (requires NINA v3 for the features used here)
- Python 3
  - Install Python 3 and ensure the python executable is in your path. The simplest method is to install via the Microsoft App Store as it automatically updates the path.

## Installation

- Download latest scripts.zip (see [Releases](releases))
- Unzip contents into %UserProfile%\Documents\N.I.N.A and verify you have a %UserProfile%\Documents\N.I.N.A\scripts\nina-camera-dew-heater directory afterward

## NINA Sequence

- Download templates\nina-camera-dew-heater.json and place into your %UserProfile%\Documents\N.I.N.A\Templates direcctory
- In NINA, navigate to Sequencer, Advanced Sequencer, select the icon to open a sequence, then open the above file
- In the External Script command, edit the USERNAME to your username, or otherwise edit the path to the batch file to match where you placed it

## Notes

This is something of a proof of concept as to how to communicate with the Powerbox Advance using the APIs they provide. If you don't wish to run the python script for some reason, another approach is to change the "When" expression in the sequencer to simply check whether DewA or DewB is > 0, which is an indication that the Powerbox Advance determined the conditions warranted at least some dew heater power. Be sure to configure and connect to your Powerbox Advance in NINA's Equipment > Switch first for DewA and DewB to be valid variables for the "When" expression.

Pegasus Astro provides other APIs for this and their other devices, so the script can be easily extended to perform more complex actions. To see the API documentation, open Pegasus Astro Unity Platform, select Application/Configuration > API Docs > Development API. 