Product Sample & Technical Tools & Support & Reference

##### OPA340, OPA2340, OPA4340

SBOS073C – SEPTEMBER 1997 – REVISED AUGUST 2016

# OPAx340Single-Supply, Rail-to-Rail Operational Amplifiers MicroAmplifier ™Series

#### 1 Features

The OPA340 series operate on a single supply as low as 2.5 V with an input common-mode voltage range 1• Rail-to-Rail Input that extends 500 mV below ground and 500 mV

- Rail-to-Rail Output (Within 1 mV)
above the positive supply. Output voltage swing is to

- *Micro*Size Packages
within 1 mV of the supply rails with a 100-kΩ load.

- Wide Bandwidth: 5.5 MHz
These devices offer excellent dynamic response (BW = 5.5 MHz, SR = 6 V/µs), yet quiescent current

- High Slew Rate: 6 V/µs
is only 750 A. Dual and quad designs feature

- Low THD + Noise: 0.0007% (f = 1 kHz)
completely independent circuitry for lowest crosstalk

- Low Quiescent Current: 750 µA/Channel
and freedom from interaction.

- Single, Dual, and Quad Versions The single (OPA340) packages are the tiny 5-pin
SOT-23 surface mount, 8-pin SOIC surface mount,

#### 2 Applicationsand 8-pin DIP. The dual (OPA2340) comes in the

miniature 8-pin VSSOP surface mount, 8-pin SOIC

- Driving A/D Converters
surface mount, and 8-pin PDIP packages. The quad

- PCMCIA Cards (OPA4340) packages are the space-saving 16-pin
- Data Acquisition SSOP surface mount and 14-pin SOIC surface
mount. All are specified from –40°C to 85°C and

- Process Control
operate from –55°C to 125°C. A SPICE macromodel

- Audio Processing
is available for design analysis.

- Communications

|||(1)|
|---|---|---|
|PART NUMBER|PACKAGE|BODY SIZE (NOM)|
|OPA340|SOT-23 (5) PDIP (8)|3.00 mm × 3.00 mm 9.81 mm × 6.35 mm|
|OPA340, OPA2340|SOIC (8)|4.90 mm × 3.91 mm|
|OPA2340|VSSOP (8) SOIC (14)|3.00 mm × 3.00 mm 8.65 mm × 3.91 mm|
|OPA4340|SSOP (16)|4.90 mm × 3.90 mm|
|the end of the data sheet.|||

(1) For all available packages, see the orderable addendum at

##### <u>Device Information</u>

- Active Filters
- Test Equipment
#### 3 Description

The OPA340 series rail-to-rail CMOS operational amplifiers are optimized for low-voltage, single-supply operation. Rail-to-rail input and output and high- speed operation make them ideal for driving sampling analog-to-digital (A/D) converters. They are also well- suited for general purpose and audio applications as well as providing I/V conversion at the output of digital-to-analog (D/A) converters. Single, dual, and quad versions have identical specifications for design flexibility.

##### OPA340 in Noninverting Configuration Driving ADS7816

|+5V|||
|---|---|---|
|0.1 F|m|0.1 F m|

8 V+ REFV 1 7 500 W

|||500|W|+In ADS781612-Bit A/D||DCLOCK|Serial|
|---|---|---|---|---|---|---|---|
|V = 0V to 5V for 0V to 5V output.|V|RC network filters high-frequency noise.|3300pF|2 -In 3 GND 4 Copyright © 2016, Texas Instruments Incorporated|NOTE: A/D Input = 0 to V||D Interface|

+In DCLOCK Serial **OPA340** **ADS7816** 12-Bit A/DOUT INCS/SHDN

IN

REF

An IMPORTANT NOTICE at the end of this data sheet addresses availability, warranty, changes, use in safety-critical applications, intellectual property matters and other important disclaimers. PRODUCTION DATA.

SBOS073C – SEPTEMBER 1997 – REVISED AUGUST 2016 **www.ti.com**

#### Table of Contents

**1 Features**.................................................................. 1 7.4 Device Functional Modes........................................ 15
**2 Applications**........................................................... 1 **8 Application and Implementation**........................ 16
**3 Description**............................................................. 1 8.1 Application Information............................................ 16
**4 Revision History**..................................................... 2

8.2 Typical Applications................................................ 16
**5 Pin Configuration and Functions**......................... 3
**9 Power Supply Recommendations**...................... 19
**6 Specifications**......................................................... 5
**10 Layout**................................................................... 20

6.1 Absolute Maximum Ratings...................................... 5
10.1 Layout Guidelines................................................. 20
6.2 ESD Ratings............................................................ 5
10.2 Layout Example.................................................... 20
6.3 Recommended Operating Conditions....................... 5 **11 Device and Documentation Support**................. 21
6.4 Thermal Information – OPA340................................ 5 11.1 Device Support...................................................... 21
6.5 Thermal Information – OPA2340.............................. 6 11.2 Documentation Support........................................ 22
6.6 Thermal Information – OPA4340.............................. 6 11.3 Related Links........................................................ 22
6.7 Electrical Characteristics........................................... 6 11.4 Receiving Notification of Documentation Updates 22
6.8 Typical Characteristics.............................................. 8 11.5 Community Resources.......................................... 22
**7 Detailed Description**............................................ 12

11.6 Trademarks........................................................... 22
7.1 Overview................................................................. 12
11.7 Electrostatic Discharge Caution............................ 22
7.2 Functional Block Diagram....................................... 12
11.8 Glossary................................................................ 23
7.3 Feature Description................................................. 13 **12 Mechanical, Packaging, and Orderable**
**Information**........................................................... 23

**4 Revision History**

**Changes from Revision B (November 2007) to Revision C Page**

- Added *ESD Ratings* table, *Feature Description* section, *Device Functional Modes*, *Application and Implementation* section, *Power Supply Recommendations* section, *Layout* section, *Device and Documentation Support* section, and
*Mechanical, Packaging, and Orderable Information* section.................................................................................................. 1

- <u>Deleted Package/Ordering Information table, see POA at the end of the data sheet............................................................ 1</u>

|2 Submit Documentation Feedback|Copyright © 1997–2016, Texas Instruments Incorporated|
|---|---|
||OPA2340 OPA4340|

Product Folder Links: *OPA340*

**www.ti.com** SBOS073C – SEPTEMBER 1997 – REVISED AUGUST 2016

#### 5 Pin Configuration and Functions

**OPA340: DBV Package** **5-Pin SOT-23 OPA340: P and D Packages** **Top View 8-Pin PDIP and SOIC** **Top View**

##### Pin Functions: OPA340

**PIN** **I/O DESCRIPTION** **NAME SOT-23 SOIC, PDIP**

|NAME|SOT-23|SOIC, PDIP|||
|---|---|---|---|---|
|–IN|4|2|I|Negative (inverting) input|
|+IN|3|3|I|Positive (noninverting) input|
|NC|—|1, 5, 8|—|No internal connection (can be left floating)|
|OUT|1|6|O|Output|
|V–|2|4|—|Negative (lowest) power supply|
|V+|5|7|—|Positive (highest) power supply|

**OPA2340: P, D, and DGK Packages** **8-Pin PDIP, SOIC, and VSSOP** **Top View**

##### Pin Functions: OPA2340

**PIN** **VSSOP, SOIC, I/O DESCRIPTION**

|NAME|VSSOP, SOIC,|I/O||
|---|---|---|---|
||PDIP|||
|–IN A|2|I|Negative (inverting) input channel A|
|+IN A|3|I|Positive (noninverting) input channel A|
|–IN B|6|I|Negative (inverting) input channel B|
|+IN B|5|I|Positive (noninverting) input channel B|
|OUT A|1|O|Output channel A|
|OUT B|7|O|Output channel B|
|V–|4|—|Negative (lowest) power supply|
|V+|8|—|Positive (highest) power supply|

Copyright © 1997–2016, Texas Instruments Incorporated *Submit Documentation Feedback* Product Folder Links: *OPA340 OPA2340 OPA4340*

SBOS073C – SEPTEMBER 1997 – REVISED AUGUST 2016 **www.ti.com**

**OPA4340: D Package OPA4340: DBQ Package** **14-Pin SOIC 16-Pin SSOP** **Top View Top View**

##### Pin Functions: OPA4340

<u>PIN</u> **I/O DESCRIPTION** **NAME SOIC SSOP**

|4 Submit Documentation Feedback|Copyright © 1997–2016, Texas Instruments Incorporated|
|---|---|
||OPA2340 OPA4340|

|NAME|SOIC|SSOP|||
|---|---|---|---|---|
|–IN A|2|2|I|Negative (inverting) input channel A|
|–IN B|6|6|I|Negative (inverting) input channel B|
|–IN C|9|11|I|Negative (inverting) input channel C|
|–IN D|13|15|I|Negative (inverting) input channel D|
|+IN A|3|3|I|Positive (noninverting) input channel A|
|+IN B|5|5|I|Positive (noninverting) input channel B|
|+IN C|10|12|I|Positive (noninverting) input channel C|
|+IN D|12|14|I|Positive (noninverting) input channel D|
|NC|—|8, 9|—|No internal connection (can be left floating)|
|OUT A|1|1|O|Output, channel A|
|OUT B|7|7|O|Output, channel B|
|OUT C|8|10|O|Output, channel C|
|OUT D|14|16|O|Output, channel D|
|V–|11|13|—|Negative (lowest) power supply|
|V+|4|4|—|Positive (highest) power supply|

Product Folder Links: *OPA340*

**www.ti.com** SBOS073C – SEPTEMBER 1997 – REVISED AUGUST 2016

#### 6 Specifications

##### 6.1 Absolute Maximum Ratings

(1)
over operating free-air temperature range (unless otherwise noted) **MIN MAX UNIT** Supply voltage 5.5 Voltage V

(2)
Signal input terminals –0.5 0.5

(2)
Signal input terminals 10 mA Current

(3)
Output short circuit <u>Continuous</u> Operating, TA–55 125 Temperature Junction, TJ150 °C Storage, Tstg–55 125

(1) Stresses beyond those listed under *Absolute Maximum Ratings* may cause permanent damage to the device. These are stress ratings only, which do not imply functional operation of the device at these or any other conditions beyond those indicated under *Recommended* *Operating Conditions*. Exposure to absolute-maximum-rated conditions for extended periods may affect device reliability.
(2) Input terminals are diode-clamped to the power-supply rails. Input signals that can swing more than 0.5 V beyond the supply rails should be current limited to 10 mA or less.
(3) Short-circuit to ground, one amplifier per package.

|6.2|ESD Ratings||||
|---|---|---|---|---|
||||VALUE|UNIT|
||Electrostatic|Human-body model (HBM), per ANSI/ESDA/JEDEC JS-001|±600||
|V(ESD)|discharge|Charged-device model (CDM), per JEDEC specification JESD22-C101|±250|V|

(1) JEDEC document JEP155 states that 500-V HBM allows safe manufacturing with a standard ESD control process.
(2) JEDEC document JEP157 states that 250-V CDM allows safe manufacturing with a standard ESD control process.

(1)
(2)
##### 6.3 Recommended Operating Conditions

over operating free-air temperature range (unless otherwise noted) **MIN MAX UNIT**

||MIN|MAX|UNIT|
|---|---|---|---|
|Supply voltage|2.7|5.5|V|
|Specified temperature|–40|125|°C|

##### 6.4 Thermal Information – OPA340

||DBV (SOT-23)|P (PDIP)|D (SOIC)|D (SOIC)||
|---|---|---|---|---|---|
||5 PINS|8 PINS|8 PINS|14 PINS||

(1) THERMAL METRIC OPA340 UNIT

|R|Junction-to-ambient thermal resistance|207.9|53.1|142|83.8|°C/W|
|---|---|---|---|---|---|---|
|R|Junction-to-case (top) thermal resistance|71.2|42.5|90.2|70.7|°C/W|
|R|Junction-to-board thermal resistance|36.0|30.3|82.5|59.5|°C/W|
|ψ|Junction-to-top characterization parameter|2.0|19.7|39.4|11.6|°C/W|
|ψ|Junction-to-board characterization parameter|35.2|30.2|82|37.7|°C/W|
|R report.|Junction-to-case (bottom) thermal resistance|—|—|—|—|°C/W|

(1) For more information about traditional and new thermal metrics, see the Semiconductor and IC Package Thermal Metrics application

θJA θJC(top) θJB JT JB θJC(bot)

Copyright © 1997–2016, Texas Instruments Incorporated *Submit Documentation Feedback* Product Folder Links: *OPA340 OPA2340 OPA4340*

SBOS073C – SEPTEMBER 1997 – REVISED AUGUST 2016 **www.ti.com**

##### <u>6.5 Thermal</u> Information – OPA2340

||D (SOIC)|DGK (VSSOP)||
|---|---|---|---|
||8 PINS|8 PINS||

(1) THERMAL METRIC OPA2340 UNIT

|R|Junction-to-ambient thermal resistance|138.4|169.2|°C/W|
|---|---|---|---|---|
|R|Junction-to-case (top) thermal resistance|89.5|62.8|°C/W|
|R|Junction-to-board thermal resistance|78.6|89.8|°C/W|
|ψ|Junction-to-top characterization parameter|29.9|7.5|°C/W|
|ψ|Junction-to-board characterization parameter|78.1|88.2|°C/W|
|R report.|Junction-to-case (bottom) thermal resistance|—|—|°C/W|

(1) For more information about traditional and new thermal metrics, see the Semiconductor and IC Package Thermal Metrics application

θJA θJC(top) θJB JT JB θJC(bot)

##### <u>6.6 Thermal</u> Information – OPA4340

||DBQ (SSOP)||
|---|---|---|
||16 PINS||

(1) THERMAL METRIC OPA4340 UNIT

|R|Junction-to-ambient thermal resistance|115.8|°C/W|
|---|---|---|---|
|R|Junction-to-case (top) thermal resistance|67|°C/W|
|R|Junction-to-board thermal resistance|58.3|°C/W|
|ψ|Junction-to-top characterization parameter|19.9|°C/W|
|ψ|Junction-to-board characterization parameter|57.9|°C/W|
|R report.|Junction-to-case (bottom) thermal resistance|—|°C/W|

(1) For more information about traditional and new thermal metrics, see the Semiconductor and IC Package Thermal Metrics application

θJA θJC(top) θJB JT JB θJC(bot)

##### 6.7 Electrical Characteristics

<u>At TA= 25°C, RL= 10 kΩ connected to VS/2, and</u> VOUT= VS/2, unless otherwise noted. **PARAMETER TEST CONDITIONS MIN TYP(1)MAX UNIT** **OFFSET VOLTAGE** VOSInput offset voltage VS=5V ±150 ±500 µV dVOS/dt Input offset voltage vs temperature TA= –40°C to 85°C, VS=5V ±2.5 µV/°C VS= 2.7 V to 5.5 V, VCM=0V 30 120 µV/V Input voltage vs PSRR V poweroffset supply Over temperatureS= 2.7 V to 5.5 V, VCM= 0 V, 120 µV/°C TA= –40°C to 85°C, VS=5V Channel separation, DC 0.2 µV/V **INPUT BIAS CURRENT** ±0.2 ±10 ISInput bias current pA Over temperature TA= –40°C to 85°C, VS=5V ±60 IOSInput offset current ±0.2 ±10 pA **NOISE** Input voltage noise f = 0.1 kHz to 50 kHz 8 µVRMS enInput voltage noise density f = 1 kHz 25 nV/√Hz inCurrent noise density f = 1 kHz 3 fA/√Hz **INPUT VOLTAGE RANGE** VCMCommon-mode voltage range –0.3 (V+) + 0.3 V –0.3 V < VCM< (V+) – 1.8 V 80 92 CMRR Common-mode rejection ratio VS= 5 V, –0.3 V < VCM< 5.3 V 70 84 dB VS= 2.7 V, –0.3 V < VCM<3V 66 80

(1) VS= 5 V.

|6 Submit Documentation Feedback|Copyright © 1997–2016, Texas Instruments Incorporated|
|---|---|
||OPA2340 OPA4340|

Product Folder Links: *OPA340*

**www.ti.com** SBOS073C – SEPTEMBER 1997 – REVISED AUGUST 2016

|Electrical Characteristics (continued) At T = 25°C, R = 10 kΩ connected to V A L|/2, and V S|= V /2, unless otherwise noted. OUT S|||
|---|---|---|---|---|
|PARAMETER||TEST CONDITIONS|(1) MIN TYP MAX|UNIT|
|INPUT IMPEDANCE|||||
|Differential|||13 10 || 3|Ω || pF|
|Common-mode|||13 10 || 6|Ω || pF|
|OPEN-LOOP GAIN||R = 100 kΩ, L 5 mV < V < (V+) – 5 mV O R = 10 kΩ, L 5 mV < V < (V+) – 50 mV O R = 2 kΩ, L 200 mV < V < (V+) – 200 mV O|106 124 100 120 94 114||
|A Open-loop voltage gain OL||R = 100 kΩ, L 5 mV < V < (V+) – 5 mV, O T = –40°C to 85°C, V =5V A S|106|dB|
||Over temperature|R = 10 kΩ, L 5 mV < V < (V+) – 50 mV, O T = –40°C to 85°C, V =5V A S R = 2 kΩ, L 200 mV < V < (V+) – 200 mV, O T = –40°C to 85°C, V =5V A S|100 94||
|FREQUENCY RESPONSE|||||
|GBW Gain-bandwidth product||G=1|5.5|MHz|
|SR Slew rate||V = 5 V, G = 1, C = 100 pF S L|6|V/µs|
|Settling time, 0.1%||V = 5 V, 2-V step, C = 100 pF S L|1|µs|
|Settling time, 0.01%||V = 5 V, 2-V step, C = 100 pF S L|1.6|µs|
|Overload recovery time||V ×G=V IN S|0.2|µs|
|THD+N Total harmonic distortion + noise||(2) ,G= 1, V = V, V = 3V S O PP f = 1 5 kHz|0.0007%||
|OUTPUT||R = 100 kΩ, A ≥ 106 dB L OL R = 10 kΩ, A ≥ 106 dB L OL R = 2 kΩ, A ≥ 106 dB L OL|1 5 10 40||
|Voltage output swing from (2) rail||R = 100 kΩ, A ≥ 106 dB, L OL T = –40°C to 85°C, V =5V A S|5|mV|
||Over temperature|R = – 10 A 106 L OL T = 40k°Ω C, to 85≥°C, V dB, =5V A S R = 2 kΩ, A ≥ 106 dB, L OL T = –40°C to 85°C, V =5V A S|50 200||
|I Short-circuit current SC|||±50|mA|
|C Capacitive load drive LOAD|||See Typical Characteristics||
|POWER SUPPLY|||||
|V Specified voltage range S||Lower end|2.7 5 2.5|V|
|Operating voltage range||Higher end|5.5|V|
|Quiescent current||I = 0, V =5V O S|750 950||
|I Q (per amplifier)|Over temperature|I = 0, V = 5 V, T = –40°C to 85°C O S A|100|µA|
|TEMPERATURE RANGE|||||
|Specified range|||–40 85|°C|
|Operating range|||–55 125|°C|
|Storage range|||–55 125|°C|

(2) Output voltage swings are measured between the output and power-supply rails.

Copyright © 1997–2016, Texas Instruments Incorporated *Submit Documentation Feedback* Product Folder Links: *OPA340 OPA2340 OPA4340*

SBOS073C – SEPTEMBER 1997 – REVISED AUGUST 2016 **www.ti.com**

##### 6.8 Typical Characteristics

|At TA= 25°C, V|S= 5 V, and R|L= 10 kΩ connected to V|S/2, unless otherwise noted.||
|---|---|---|---|---|
||160||0 45|100|
||80||||
||0||-90|80|
||-20||||
||||-135 Phase ( )|0|
||||-|180|
|Voltage Gain (dB)||||PSRR, CMRR (dB)|

PSRR

0.1 1 10 100 1k 10k 100k 1M 10M
Frequency (Hz)

**Figure 1. Open-Loop Gain/Phase vs Frequency**

10k 1k Current Noise ) 1k) Hz Hz Voltage Noise

Voltage Noise (nV/ 10 Current Noise (fA/ Channel Separation (dB)

1 1 10 100 1k 10k 100k 1M Frequency (Hz) W

**Figure 3. Input Voltage and Current Noise Spectral Density vs Frequency**

0.1
RL= 600

RL= 2k W)

0.01 G = 10
RL= 10k W RL= 600 R L = 2k W THD+N (%)

0.001G = 1
Output Resistance ( RL= 10k W

0.0001 20 100 1k 10k
Frequency (Hz)

**Figure 5. Total Harmonic Distortion + Noise vs Frequency**

CMRR

1 10 100 1k 10k 100k 1M Frequency (Hz)

**Figure 2. Power-Supply and Common-Mode Rejection vs**

**Frequency** 140

100 10 100 1k 10k 100k

G = 1, All Channels

Frequency (Hz)

**Figure 4. Channel Separation vs Frequency**

5k G = 100

0 G = 10

G = 1

|8 Submit Documentation Feedback|Copyright © 1997–2016, Texas Instruments Incorporated|
|---|---|
||OPA2340 OPA4340|

Product Folder Links: *OPA340*

20k 10 100 1k 10k 100k 1M 10M Frequency (Hz)

**Figure 6. Closed-Loop Output Impedance vs Frequency**

**www.ti.com** SBOS073C – SEPTEMBER 1997 – REVISED AUGUST 2016

##### Typical Characteristics (continued)

At TA= 25°C, VS= 5 V, and RL= 10 kΩ connected to VS/2, unless otherwise noted. 130 100 R L = 100k W AOL 90 110 R L = 10k W

100 R L = 2k W

, PSRR (dB) 90 CMRR (dB) A OL PSRR V S= 2.7V to 5V, VCM=-0.3V to (V+) 1.8V- V S= 5V, VCM=-0.3V to 5.3V V S= 2.7V, VCM=-0.3V to 3V

-75-50-25 0 25 50 75 100 125-75-50-25 0 25 50 75 100 125 m Temperature ( C) m Temperature ( C)

**Figure 7. Open-Loop Gain and Power-Supply Rejection vs Figure 8. Common-Mode Rejection vs Temperature**

**Temperature** 1000 800 Per Amplifier 2.0Per Amplifier 2.5 3.0 3.5 4.0 4.5 5.0 5.5 6.0 900

A) A) Quiescent Current ( Quiescent Current (

|-75|-50-25|0 25|50 75|100 125|||||||
|---|---|---|---|---|---|---|---|---|---|---|
||Temperature ( C)||||||Supply Voltage (V)||||
|Figure 9. Quiescent Current vs Temperature|||||Figure 10. Quiescent Current vs Supply Voltage||||||
|100|||||60||||||
|90-|I||||2.0|2.5 3.0|3.5|4.0 4.5|5.0 5.5|6.0|
|0-75|-50|-25 0|25 50|75 100|125|-I|||||

SC

SC

+ISC +ISC

Short-Circuit Current (mA) Short-Circuit Current (mA)

Temperature ( C) Supply Voltage (V)

**Figure 11. Short-Circuit Current vs Temperature Figure 12. Short-Circuit Current vs Supply Voltage**

Copyright © 1997–2016, Texas Instruments Incorporated *Submit Documentation Feedback* Product Folder Links: *OPA340 OPA2340 OPA4340*

SBOS073C – SEPTEMBER 1997 – REVISED AUGUST 2016 **www.ti.com**

##### Typical Characteristics (continued)

At TA= 25°C, VS= 5 V, and RL= 10 kΩ connected to VS/2, unless otherwise noted. 1k 1.0 0 -0.2 100 -0.4 -0.6 10-0.8 -1.0 -1 0 1 2 3 4 5 6 Input Bias Current (pA) 1 Input Bias Current (pA)

0.1
-75-50-25 0 25 50 75 100 125 Temperature ( C) Common-Mode Voltage (V)

**Figure 13. Input Bias Current vs Temperature Figure 14. Input Bias Current vs Input Common-Mode**

**Voltage** 5 6 0 VS= 5.5V Maximum output +125 C +25 C-55 C ) PP

VS= 2.7V

Output Voltage (V) Output Voltage (V

+125 C +25 C-55 C

–10 –20 –30 –40 –50 –60 –70 –80 –90 –100 100k 1M 10M Output Current (mA) Frequency (Hz)

**Figure 15. Output Voltage Swing vs Output Current Figure 16. Maximum Output Voltage vs Frequency**

18 25 Typical production Typical production 8 500 400 5 300 200 0 100 100 - 200 Percent of Amplifiers (%)- 300 Percent of Amplifiers (%) - 400 0 1 2 3 4 5 6 7 8 9 10 11 12 13 15 - 500 - Offset Voltage ( V) m Offset Voltage Drift ( V/ C) m

**Figure 17. Offset Voltage Production Distribution Figure 18. Offset Voltage Drift Magnitude Production**

**Distribution**

|10 Submit Documentation Feedback|Copyright © 1997–2016, Texas Instruments Incorporated|
|---|---|
||OPA2340 OPA4340|

Product Folder Links: *OPA340*

**www.ti.com** SBOS073C – SEPTEMBER 1997 – REVISED AUGUST 2016

##### Typical Characteristics (continued)

At TA= 25°C, VS= 5 V, and RL= 10 kΩ connected to VS/2, unless otherwise noted.

50mV/div 1V/div

1 s/div m 1 s/div m CL= 100 pF CL= 100 pF

**Figure 19. Small-Signal Step Response** m **Figure 20. Large-Signal Step Response**

60 100

G = 0 1-

0.01%
G = +1 s) 10

|Overshoot (%)||G = 5|-|1|0.1%|
|---|---|---|---|---|---|
|||||Settling Time (||
|G = +5||See text for reducing overshoot.||||
|||||0.1||
||100 1000||10k||1|
||Load Capacitance (pF)||||Closed-Loop Gain (V/V)|
|Figure 21. Small-Signal Overshoot vs Load Capacitance||||Figure 22. Settling Time vs Closed-Loop Gain||

10 100 1000

Copyright © 1997–2016, Texas Instruments Incorporated *Submit Documentation Feedback* Product Folder Links: *OPA340 OPA2340 OPA4340*

<u>SBOS073C – SEPTEMBER 1997 – REVISED AUGUST 2016 www.ti.com</u>

#### 7 Detailed Description

##### 7.1 Overview

The OPA340 series operational amplifiers are fabricated on a state-of-the-art, 0.6-micron CMOS process. These devices are unity-gain stable and suitable for a wide range of general-purpose applications. Rail-to-rail input and output make them ideal for driving sampling A/D converters. In addition, excellent AC performance makes them well-suited for audio applications. The class AB output stage is capable of driving 600-Ω loads series and extends 500 mV beyond the supply. Rail-to-rail input and output swing significantly increases dynamic range, especially in low-supply applications. Figure 23 shows the input and output waveforms for the OPA340 in unity- gain configuration. Operation is from a single 5-V supply with a 10-kΩ load connected to V/2. The input is a 5- VPPsinusoid. Output voltage is approximately 4.98 VPP. Power-supply pins must be bypassed with 0.01-µF ceramic capacitors.

V = +5, G = +1, R = 10kS LW

5 VIN

2V/div

5 VOUT

**Figure 23. Rail-to-Rail Input and Output**

##### 7.2 Functional Block Diagram

V+

Reference Current

V IN+ VIN-

V BIAS1 Class AB Control VO Circuitry V BIAS2

V- (Ground) Copyright © 2016, Texas Instruments Incorporated

|12 Submit Documentation Feedback|Copyright © 1997–2016, Texas Instruments Incorporated|
|---|---|
||OPA2340 OPA4340|

Product Folder Links: *OPA340*

<u>www.ti.com SBOS073C – SEPTEMBER 1997 – REVISED AUGUST 2016</u>

##### 7.3 Feature Description

##### 7.3.1 Operating Voltage

The OPA340 series operational amplifiers are fully specified from 2.7 V to 5 V. However, supply voltage may range from 2.5 V to 5.5 V. Parameters are ensured over the specified supply range—a unique feature of the OPA340 series. In addition, many specifications apply from –40°C to 85°C. Most behavior remains virtually unchanged throughout the full operating voltage range. Parameters which vary significantly with operating voltages or temperature are shown in the *Typical Characteristics*.

##### 7.3.2 Rail-to-Rail Input

The input common-mode voltage range of the OPA340 series extends 500 mV beyond the supply rails. This extended range is achieved with a complementary input stage—an N-channel input differential pair in parallel with a P-channel differential pair. The N-channel pair is active for input voltages close to the positive rail, typically (V+) – 1.3 V to 500 mV above the positive supply, while the P-channel pair is on for inputs from 500 mV below the negative supply to approximately (V+) – 1.3 V. There is a small transition region, typically (V+) – 1.5 V to (V+) – 1.1 V, in which both pairs are on. This 400-mV transition region can vary ±300 mV with process variation. Thus, the transition region (both stages on) can range from (V+) – 1.8 V to (V+) – 1.4 V on the low end, up to (V+) – 1.2 V to (V+) – 0.8 V on the high end.

OPA340 series operational amplifiers are laser-trimmed to the reduce offset voltage difference between the N- channel and P-channel input stages, resulting in improved common-mode rejection and a smooth transition between the N-channel pair and the P-channel pair. However, within the 400-mV transition region PSRR, CMRR, offset voltage, offset drift, and THD may be degraded compared to operation outside this region.

A double-folded cascode adds the signal from the two input pairs and presents a differential signal to the class AB output stage. Normally, input bias current is approximately 200 fA; however, input voltages exceeding the power supplies by more than 500 mV can cause excessive current to flow in or out of the input pins. Momentary voltages greater than 500 mV beyond the power supply can be tolerated if the current on the input pins is limited to 10 mA. This current limiting is easily accomplished with an input resistor, as shown in Figure 24. Many input signals are inherently current-limited to less than 10 mA; therefore, a limiting resistor is not required.

V+ I OVERLOAD 10mA max **OPAx340** VOUT IN V 5k W

Copyright © 2016, Texas Instruments Incorporated

**Figure 24. Input Current Protection for Voltages Exceeding the Supply Voltage**

##### 7.3.3 Rail-to-Rail Output

A class AB output stage with common-source transistors is used to achieve rail-to-rail output. For light resistive loads (> 50 kΩ), the output voltage is typically a few millivolts from the supply rails. With moderate resistive loads (2 kΩ to 50 kΩ), the output can swing to within a few tens of millivolts from the supply rails and maintain high open-loop gain (see Figure 15).

##### 7.3.4 Capacitive Load and Stability

OPA340 series operational amplifiers can drive a wide range of capacitive loads. However, all operational amplifiers under certain conditions can become unstable. operational amplifier configuration, gain, and load value are some of the factors to consider when determining stability. An operational amplifier in unity-gain configuration is most susceptible to the effects of capacitive load. The capacitive load reacts with the output resistance of the operational amplifier, along with any additional load resistance, to create a pole in the small-signal response that degrades the phase margin. In unity-gain configuration, the OPA340 series operational amplifiers perform well, with a pure capacitive load up to approximately 1000 pF. Increasing gain enhances the amplifier ability to drive more capacitance (see Figure 21).

Copyright © 1997–2016, Texas Instruments Incorporated *Submit Documentation Feedback* Product Folder Links: *OPA340 OPA2340 OPA4340*

<u>SBOS073C – SEPTEMBER 1997 – REVISED AUGUST 2016 www.ti.com</u>

##### Feature Description (continued)

One method of improving capacitive load drive in the unity-gain configuration is to insert a 10-Ω to 20-Ω resistor in series with the output, as shown in Figure 25. This resistor significantly reduces ringing with large capacitive loads. However, if there is a resistive load in parallel with the capacitive load, it creates a voltage divider introducing a DC error at the output and slightly reduces output swing. This error can be insignificant. For instance, with RL= 10 kΩ and RS= 20 Ω, there is only an approximate 0.2% error at the output.

When used with the miniature package options of the OPA340 series, the combination is ideal for space-limited and low-power applications. For further information, consult the ADS7816 data sheet, *12-Bit High Speed Micro* *Power Sampling Analog-To-Digital Converter* (SBAS061). With the OPA340 in a noninverting configuration, an RC network at the output of the amplifier can be used to filter high-frequency noise in the signal (see Figure 26). In the inverting configuration, filtering may be accomplished with a capacitor across the feedback resistor (see

Figure 27).

V+

RS **OPAx340** VOUT

||10 to W||
|---|---|---|
||20|W R|

IN V 10 to W C L L

Copyright © 2016, Texas Instruments Incorporated

**Figure 25. Series Resistor in Unity-Gain Configuration Improves Capacitive Load Drive**

##### 7.3.5 Driving A/D Converters

The OPA340 series operational amplifiers are optimized for driving medium-speed (up to 100 kHz) sampling A/D converters. However, they also offer excellent performance for higher speed converters. The OPA340 series provides an effective means of buffering the converter input capacitance and resulting charge injection while providing signal gain. Figure 26 and Figure 27 show the OPA340 driving an ADS7816. The ADS7816 is a 12-bit, micro-power sampling converter in the tiny 8-pin VSSOP package.

|+5V|||
|---|---|---|
|0.1 F|m|0.1 F m|

8 V+ REFV 1 7 500 W

|||500|W|+In ADS781612-Bit A/D||DCLOCK|Serial|
|---|---|---|---|---|---|---|---|
|V = 0V to 5V for 0V to 5V output.|V|RC network filters high-frequency noise.|3300pF|2 -In 3 GND 4 Copyright © 2016, Texas Instruments Incorporated|NOTE: A/D Input = 0 to V||D Interface|

+In DCLOCK Serial **OPA340** **ADS7816** 12-Bit A/DOUT INCS/SHDN

IN

REF

**Figure 26. OPA340 in Noninverting Configuration Driving ADS7816**

|14 Submit Documentation Feedback|Copyright © 1997–2016, Texas Instruments Incorporated|
|---|---|
||OPA2340 OPA4340|

Product Folder Links: *OPA340*

<u>www.ti.com SBOS073C – SEPTEMBER 1997 – REVISED AUGUST 2016</u>

##### Feature Description (continued)

+5V

330pF

0.1 F m 0.1 F m
5k W 5k W V INV 1 8 V+ REF 7 DCLOCK **OPA340** **ADS7816** 12-Bit A/DOUT D Interface +In Serial 2 -In CS/SHDN 3 GND 4

INV = 0V to 5V for 0V to 5V output.-NOTE: A/D Input = 0 to VREF Copyright © 2016, Texas Instruments Incorporated

**Figure 27. OPA340 in Inverting Configuration Driving ADS7816**

+5V Filters 160Hz to 2.4kHz

10M W

INV **1/2** 243k W 1.74M W

|10M OPA2340|W200pF||1/2||
|---|---|---|---|---|
||||OPA2340|47pF|
|||||R|
|||Copyright © 2016, Texas Instruments Incorporated|220pF||

10M **OPA2340** W200pF **1/2**

L

**Figure 28. Speech Bandpass Filter**

##### 7.4 Device Functional Modes

The OPAx340 has a single functional mode and is operational when the power-supply voltage is greater than

2.7 V (±1.35 V). The maximum power supply voltage for the OPAx340 is 5.5 V (±2.75 V).
Copyright © 1997–2016, Texas Instruments Incorporated *Submit Documentation Feedback* Product Folder Links: *OPA340 OPA2340 OPA4340*

SBOS073C – SEPTEMBER 1997 – REVISED AUGUST 2016 **www.ti.com**

#### 8 Application and Implementation

##### NOTE

Information in the following applications sections is not part of the TI component specification, and TI does not warrant its accuracy or completeness. TI’s customers are responsible for determining suitability of components for their purposes. Customers should validate and test their design implementation to confirm system functionality.

##### 8.1 Application Information

The OPAx340 amplifier is a single-supply, CMOS operational amplifier with 5.5-MHz unity-gain bandwidth and supply current of 950 µA. Its performance is optimized for low-voltage (2.7 V to 5.5 V), single-supply applications, with its input common-mode voltage linear range extending 300 mV beyond the rails and the output voltage swing within 5 mV of either rail. The OPAx340 series features wide bandwidth and unity-gain stability with rail-to- rail input and output for increased dynamic range. Power-supply pins must be bypassed with 0.01-µF ceramic capacitors.

##### 8.2 Typical Applications

##### 8.2.1 Single-Pole, Low-Pass Filter

Figure 29 shows the OPA340 in a typical noninverting application with the input signal bandwidth limited by the

input lowpass filter.

**Figure 29. Single-Pole, Low-Pass Filter**

Equation 1 through Equation 2 show calculations for corner frequency and gain:

(1)
(2)

|16 Submit Documentation Feedback|Copyright © 1997–2016, Texas Instruments Incorporated|
|---|---|
||OPA2340 OPA4340|

Product Folder Links: *OPA340*

<u>www.ti.com SBOS073C – SEPTEMBER 1997 – REVISED AUGUST 2016</u>

##### Typical Applications (continued)

##### 8.2.1.1 Design Requirements

When receiving low-level signals, limiting the bandwidth of the incoming signals into the system is often required. The simplest way to establish this limited bandwidth is to place an RC filter at the noninverting terminal of the amplifier, as shown in Figure 29. If a steeper attenuation level is required, a two-pole or higher-order filter may be used.

##### 8.2.1.2 Detailed Design Procedure

The design goals for this circuit include these parameters:

- A noninverting gain of 10 V/V (20 dB)
- Design a single-pole response circuit with –3-dB rolloff at 15.9 kHz and 159 Hz
- Modify the design to increase attenuation level to –40 dB/decade (Sallen-Key Filter) Use these design values:
- C₁ = 0 nF, 10 nF, 1 µF
- R₁ = 1 kΩ
- RG= 10 kΩ
- RF= 90 kΩ
Figure 30 shows how the output voltage of OPA340 changes over frequency depending on the value of C₁ with a
 constant R₁ of 1 kΩ. Without any filtering of the input signal (C₁ = 0), the –3-dB effective bandwidth is a function of the OPA340 unity-gain bandwidth and closed-loop gain, f(–3dB)= UGBW/ACL, where ACLis closed-loop gain and UGBW denotes unity-gain bandwidth. Thus, for a closed-loop gain = 10, f(–3dB)= 1 MHz/10 =100 kHz; see
Figure 30.
 To further limit the output bandwidth, an appropriate choice of C₁ must be made: for C₁ = 10 nF,
##### = 15.9 kHz.

To further limit the bandwidth, a larger C₁ must be used: choosing C₁ = 1 µF,

##### = 159 Hz (see Figure 30).

##### 8.2.1.3 Application Curve

IN

OUT 40

C = 01 0 (dB)

|/V|||C = 10 nF||
|---|---|---|---|---|
|-|20|C = 1 F|m||
|Gain = V|-40||||

/V C = 10 nF1

1 10 100 1 k 10 k 100 k 1 M Frequency (Hz)

**Figure 30. OPA340 Single-Pole AC Gain vs Frequency Response**

Copyright © 1997–2016, Texas Instruments Incorporated *Submit Documentation Feedback* Product Folder Links: *OPA340 OPA2340 OPA4340*

<u>SBOS073C – SEPTEMBER 1997 – REVISED AUGUST 2016 www.ti.com</u>

##### Typical Applications (continued)

##### 8.2.2 Two-Pole, Low-Pass Filter

If even more attenuation is required, a multiple pole filter is required. The Sallen-Key filter may be used for this task, as shown in Figure 31. For best results, the amplifier must have effective bandwidth that is at least 10 times higher than the filter cutoff frequency. Failure to follow this guideline results in a phase shift of the amplifier, which in turn leads to lower precision of the filter bandwidth. Additionally, to minimize the loading effect between multiple RC pairs on overall the filter cutoff frequency, choose R = 10 × R₁ and C₂ = C1/10; see Figure 32.

**Figure 31. Two-Pole, Lowpass Filter**

Equation 3 through Equation 5 show calculations for corner frequency and gain:

(3)
(4)
(5)
##### 8.2.2.1 Detailed Design Procedure

Use these design values:

- C₁ = 10 nF and C₂ = 1 nF
- R₁ = 1 kΩ and R₂= 10 kΩ
- RG= 10 kΩ
- RF= 90 kΩ
Figure 32 shows the Sallen-Key filter second-order response for different RC values: for R and C values above,

##### = 15.9 kHz.

To further limit the bandwidth, a larger RC value must be used: increasing C values 100 times, such as C₁ = 1 µF and C₂ = 0.1 µF, with unchanged resistors, results in the second-order rolloff at

##### = 159 Hz. See Figure 32.

|18 Submit Documentation Feedback|Copyright © 1997–2016, Texas Instruments Incorporated|
|---|---|
||OPA2340 OPA4340|

Product Folder Links: *OPA340*

**www.ti.com** SBOS073C – SEPTEMBER 1997 – REVISED AUGUST 2016

##### Typical Applications (continued)

##### 8.2.2.2 Application Curve

**Figure 32. OPA340 Two-Pole, Lowpass Sallen-Key AC Gain vs Frequency Response**

#### 9 Power Supply Recommendations

The OPAx340 is specified for operation from 2.7 V to 5.5 V (±1.35 V to ±2.75 V).

##### CAUTION

Supply voltages larger than 7 V can permanently damage the device (see the *Absolute* *Maximum Ratings*).

TI recommends placing 0.1-μF bypass capacitors close to the power-supply pins to reduce errors coupling in from noisy or high-impedance power supplies.

Copyright © 1997–2016, Texas Instruments Incorporated *Submit Documentation Feedback* Product Folder Links: *OPA340 OPA2340 OPA4340*

<u>SBOS073C – SEPTEMBER 1997 – REVISED AUGUST 2016 www.ti.com</u>

#### 10 Layout

##### 10.1 Layout Guidelines

Pay attention to good layout practices. Keep traces short and when possible, use a printed-circuit board (PCB) ground plane with surface-mount components placed as close to the device pins as possible. Place a 0.1-μF capacitor closely across the supply pins. Apply these guidelines throughout the analog circuit to improve performance and provide benefits, such as reducing the electromagnetic interference (EMI) susceptibility.

Operational amplifiers vary in susceptibility to radio frequency interference (RFI). RFI can generally be identified as a variation in offset voltage or DC signal levels with changes in the interfering RF signal. The OPA340 is specifically designed to minimize susceptibility to RFI and demonstrates remarkably low sensitivity compared to previous generation devices. Strong RF fields can still cause varying offset levels.

##### 10.2 Layout Example

Place components close to device and Run the input traces to eachother toreduce parasitic as far away from errors the supply lines VS+

||RF||
|---|---|---|
||N/C|N/C|
|RG|||
|GND|–IN|V+|
|VIN|+IN|OUTPUT|
||V–|N/C|

as possible

GND

Use low-ESR, ceramic bypass capacitor

GNDVS– Use low-ESR, VOUT ceramic bypass capacitor Copyright © 2016, Texas Instruments Incorporated

**Figure 33. Layout Recommendation**

VIN +± VOUT

RG RF

Copyright © 2016, Texas Instruments Incorporated

**Figure 34. Schematic Representation**

|20 Submit Documentation Feedback|Copyright © 1997–2016, Texas Instruments Incorporated|
|---|---|
||OPA2340 OPA4340|

Product Folder Links: *OPA340*

**www.ti.com** SBOS073C – SEPTEMBER 1997 – REVISED AUGUST 2016

#### 11 Device and Documentation Support

##### 11.1 Device Support

##### 11.1.1 Development Support

##### 11.1.1.1 TINA-TI™ (Free Software Download)

TINA™ is a simple, powerful, and easy-to-use circuit simulation program based on a SPICE engine. TINA-TI™ is a free, fully-functional version of the TINA software, preloaded with a library of macro models in addition to a range of both passive and active models. TINA-TI provides all the conventional DC, transient, and frequency domain analysis of SPICE, as well as additional design capabilities.

Available as a free download from the Analog eLab Design Center, TINA-TI offers extensive post-processing capability that allows users to format results in a variety of ways. Virtual instruments offer the ability to select input waveforms and probe circuit nodes, voltages, and waveforms, creating a dynamic quick-start tool.

##### NOTE

These files require that either the TINA software (from DesignSoft™) or TINA-TI software be installed. Download the free TINA-TI software from the TINA-TI folder.

##### 11.1.1.2 DIP Adapter EVM

The DIP Adapter EVM tool provides an easy, low-cost way to prototype small surface mount ICs. The evaluation tool these TI packages: D or U (SOIC-8), PW (TSSOP-8), DGK (MSOP-8), DBV (SOT23-6, SOT23-5 and SOT23-3), DCK (SC70-6 and SC70-5), and DRL (SOT563-6). The DIP Adapter EVM may also be used with terminal strips or may be wired directly to existing circuits.

##### 11.1.1.3 Universal Operational Amplifier EVM

The Universal Op Amp EVM is a series of general-purpose, blank circuit boards that simplify prototyping circuits for a variety of IC package types. The evaluation module board design allows many different circuits to be constructed easily and quickly. Five models are offered, with each model intended for a specific package type. PDIP, SOIC, MSOP, TSSOP and SOT23 packages are all supported.

##### NOTE

These boards are unpopulated, so users must provide their own ICs. TI recommends requesting several operational amplifier device samples when ordering the Universal Op Amp EVM.

##### 11.1.1.4 TI Precision Designs

TI Precision Designs are analog solutions created by TI’s precision analog applications experts and offer the theory of operation, component selection, simulation, complete PCB schematic and layout, bill of materials, and measured performance of many useful circuits. TI Precision Designs are available online at [http://www.ti.com/ww/en/analog/precision-designs/](http://www.ti.com/ww/en/analog/precision-designs/).

##### 11.1.1.5 WEBENCH

*®* ***Filter Designer***

WEBENCH® Filter Designer is a simple, powerful, and easy-to-use active filter design program. The WEBENCH Filter Designer lets you create optimized filter designs using a selection of TI operational amplifiers and passive components from TI's vendor partners.

Available as a web-based tool from the WEBENCH® Design Center, WEBENCH® Filter Designer allows you to design, optimize, and simulate complete multistage active filter solutions within minutes.

Copyright © 1997–2016, Texas Instruments Incorporated *Submit Documentation Feedback* Product Folder Links: *OPA340 OPA2340 OPA4340*

SBOS073C – SEPTEMBER 1997 – REVISED AUGUST 2016 **www.ti.com**

##### 11.2 Documentation Support

##### 11.2.1 Related Documentation

For related documentation, see the following application reports and publications (available for download from www.ti.com):

- *12-Bit High Speed Micro Power Sampling Analog-To-Digital Converter* (SBAS061)
- *A Dual-Polarity, Bidirectional Current-Shunt Monitor* (SLYT311)
- *OPA340, OPA2340, OPA4340 EMI Immunity Performance* (SBOZ010)
- *Getting the Full Potential from your ADC* (SBAA069)
- *Feedback Plots Define Op Amp AC Performance* (SBOA015)
- *Capacitive Load Drive Solution Using an Isolation Resistor* (TIPD128)
- *Circuit Board Layout Techniques* (SLOA089)
##### 11.3 Related Links

Table 1 lists quick access links. Categories include technical documents, support and community resources,

tools and software, and quick access to sample or buy.

**Table 1. Related Links**

|PARTS|PRODUCT FOLDER|SAMPLE & BUY|TECHNICAL|TOOLS &|SUPPORT &|
|---|---|---|---|---|---|
||||DOCUMENTS|SOFTWARE|COMMUNITY|
|OPA340|Click here|Click here|Click here|Click here|Click here|

OPA2340 Click here Click here Click here Click here Click here OPA4340 Click here Click here Click here Click here Click here

##### 11.4 Receiving Notification of Documentation Updates

To receive notification of documentation updates, navigate to the device product folder on ti.com. In the upper right corner, click on *Alert me* to register and receive a weekly digest of any product information that has changed. For change details, review the revision history included in any revised document.

##### 11.5 Community Resources

The following links connect to TI community resources. Linked contents are provided "AS IS" by the respective contributors. They do not constitute TI specifications and do not necessarily reflect TI's views; see TI's Terms of Use.

**TI E2E™ Online Community *TI's Engineer-to-Engineer (E2E) Community.*** Created to foster collaboration among engineers. At e2e.ti.com, you can ask questions, share knowledge, explore ideas and help solve problems with fellow engineers.

**Design Support *TI's Design Support*** Quickly find helpful E2E forums along with design support tools and contact information for technical support.

##### 11.6 Trademarks

MicroAmplifier, TINA-TI, E2E are trademarks of Texas Instruments. WEBENCH is a registered trademark of Texas Instruments. TINA, DesignSoft are trademarks of DesignSoft, Inc. All other trademarks are the property of their respective owners.

##### 11.7 Electrostatic Discharge Caution

These devices have limited built-in ESD protection. The leads should be shorted together or the device placed in conductive foam during storage or handling to prevent electrostatic damage to the MOS gates.

|22 Submit Documentation Feedback|Copyright © 1997–2016, Texas Instruments Incorporated|
|---|---|
||OPA2340 OPA4340|

Product Folder Links: *OPA340*

<u>www.ti.com SBOS073C – SEPTEMBER 1997 – REVISED AUGUST 2016</u>

##### 11.8 Glossary

SLYZ022 — *TI Glossary*. This glossary lists and explains terms, acronyms, and definitions.

#### 12 Mechanical, Packaging, and Orderable Information

The following pages include mechanical, packaging, and orderable information. This information is the most current data available for the designated devices. This data is subject to change without notice and revision of this document. For browser-based versions of this data sheet, refer to the left-hand navigation.

Copyright © 1997–2016, Texas Instruments Incorporated *Submit Documentation Feedback* Product Folder Links: *OPA340 OPA2340 OPA4340*

### PACKAGE OPTION ADDENDUM

www.ti.com 15-Jul-2026

##### PACKAGING INFORMATION

**Orderable part number**

|Status (1)|Material type (2)|Package | Pins|Package qty | Carrier||RoHS (3)|Lead finish/ Ball material (4)||MSL rating/ Peak reflow (5)|Op temp (°C)|Part marking (6)|
|---|---|---|---|---|---|---|---|---|---|---|
|Active|Production|VSSOP (DGK) | 8|250 | SMALL T&R||Yes|NIPDAU | SN | NIPDAUAG|Level-2-260C-1 YEAR||-|A40A|
|Active|Production|VSSOP (DGK) | 8|250 | SMALL T&R||Yes|NIPDAU|Level-2-260C-1 YEAR||-40 to 85|A40A|
|Last Time Buy|Production|VSSOP (DGK) | 8|250 | SMALL T&R||Yes|NIPDAU | NIPDAUAG|Level-2-260C-1 YEAR||-|A40A|
|Last Time Buy|Production|VSSOP (DGK) | 8|250 | SMALL T&R||Yes|NIPDAU|Level-2-260C-1 YEAR||-40 to 85|A40A|
|Active|Production|VSSOP (DGK) | 8|2500 | LARGE T&R||Yes|NIPDAU | SN | NIPDAUAG|Level-2-260C-1 YEAR||-|A40A|
|Active|Production|VSSOP (DGK) | 8|2500 | LARGE T&R||Yes|NIPDAU|Level-2-260C-1 YEAR||-40 to 85|A40A|
|Last Time Buy|Production|VSSOP (DGK) | 8|2500 | LARGE T&R||Yes|NIPDAU | NIPDAUAG|Level-2-260C-1 YEAR||-|A40A|
|Last Time Buy|Production|VSSOP (DGK) | 8|2500 | LARGE T&R||Yes|NIPDAU|Level-2-260C-1 YEAR||-40 to 85|A40A|
|Active|Production|SOIC (D) | 8||75 | TUBE|Yes|NIPDAU|Level-2-260C-1 YEAR||-40 to 85|OPA 2340UA|
|Active|Production|SOIC (D) | 8||75 | TUBE|Yes|NIPDAU|Level-2-260C-1 YEAR||-40 to 85|OPA 2340UA|
|Active|Production|SOIC (D) | 8|2500 | LARGE T&R||Yes|NIPDAU|Level-2-260C-1 YEAR||-|OPA 2340UA|
|Active|Production|SOIC (D) | 8|2500 | LARGE T&R||Yes|NIPDAU|Level-2-260C-1 YEAR||-40 to 85|OPA 2340UA|
|Active|Production|SOIC (D) | 8|2500 | LARGE T&R||Yes|NIPDAU|Level-2-260C-1 YEAR||See OPA2340UA/2K5|OPA 2340UA|
|Active|Production|SOT-23 (DBV) | 5|250 | SMALL T&R||Yes|NIPDAU|Level-2-260C-1 YEAR||-40 to 85|A40|
|Active|Production|SOT-23 (DBV) | 5|250 | SMALL T&R||Yes|NIPDAU|Level-2-260C-1 YEAR||-40 to 85|A40|
|Active|Production|SOT-23 (DBV) | 5|250 | SMALL T&R||Yes|NIPDAU|Level-2-260C-1 YEAR||-40 to 85|A40|
|Active|Production|SOT-23 (DBV) | 5|3000 | LARGE T&R||Yes|NIPDAU|Level-2-260C-1 YEAR||-40 to 85|A40|
|Active|Production|SOT-23 (DBV) | 5|3000 | LARGE T&R||Yes|NIPDAU|Level-2-260C-1 YEAR||-40 to 85|A40|
|Active|Production|SOT-23 (DBV) | 5|3000 | LARGE T&R||Yes|NIPDAU|Level-2-260C-1 YEAR||-40 to 85|A40|
|Active|Production|PDIP (P) | 8||50 | TUBE|Yes|NIPDAU|N/A for Pkg Type||-40 to 85|OPA340PA|
|Active|Production|PDIP (P) | 8||50 | TUBE|Yes|NIPDAU|N/A for Pkg Type||-40 to 85|OPA340PA|

OPA2340EA/250

OPA2340EA/250.B OPA2340EA/250G4

OPA2340EA/250G4.B

OPA2340EA/2K5

OPA2340EA/2K5.B OPA2340EA/2K5G4

OPA2340EA/2K5G4.B

OPA2340UA

OPA2340UA.B

OPA2340UA/2K5

OPA2340UA/2K5.B

OPA2340UA/2K5G4

OPA340NA/250 OPA340NA/250.B OPA340NA/250G4 OPA340NA/3K OPA340NA/3K.B OPA340NA/3KG4 OPA340PA OPA340PA.B

Addendum-Page

### PACKAGE OPTION ADDENDUM

www.ti.com 15-Jul-2026

**Orderable part number**

|Status (1)|Material type (2)|Package | Pins|Package qty | Carrier||RoHS (3)|Lead finish/ Ball material (4)|MSL rating/ Peak reflow (5)|Op temp (°C)|Part marking (6)|
|---|---|---|---|---|---|---|---|---|---|
|Active|Production|SOIC (D) | 8||75 | TUBE|Yes|NIPDAU|Level-2-260C-1 YEAR|-40 to 85|OPA 340UA|
|Active|Production|SOIC (D) | 8||75 | TUBE|Yes|NIPDAU|Level-2-260C-1 YEAR|-40 to 85|OPA 340UA|
|Active|Production|SOIC (D) | 8|2500 | LARGE T&R||Yes|NIPDAU|Level-2-260C-1 YEAR|-40 to 85|OPA 340UA|
|Active|Production|SOIC (D) | 8|2500 | LARGE T&R||Yes|NIPDAU|Level-2-260C-1 YEAR|-40 to 85|OPA 340UA|
|Active|Production|SOIC (D) | 8|2500 | LARGE T&R||Yes|NIPDAU|Level-2-260C-1 YEAR|-40 to 85|OPA 340UA|
|Active|Production|SSOP (DBQ) | 16|250 | SMALL T&R||Yes|NIPDAU|Level-2-260C-1 YEAR|-40 to 85|OPA 4340EA|
|Active|Production|SSOP (DBQ) | 16|250 | SMALL T&R||Yes|NIPDAU|Level-2-260C-1 YEAR|-40 to 85|OPA 4340EA|
|Active|Production|SSOP (DBQ) | 16|250 | SMALL T&R||Yes|NIPDAU|Level-2-260C-1 YEAR|-40 to 85|OPA 4340EA|
|Active|Production|SSOP (DBQ) | 16|2500 | LARGE T&R||Yes|NIPDAU|Level-2-260C-1 YEAR|-40 to 85|OPA 4340EA|
|Active|Production|SSOP (DBQ) | 16|2500 | LARGE T&R||Yes|NIPDAU|Level-2-260C-1 YEAR|-40 to 85|OPA 4340EA|
|Active|Production|SOIC (D) | 14||50 | TUBE|Yes|NIPDAU|Level-3-260C-168 HR|-40 to 85|OPA4340UA|
|Active|Production|SOIC (D) | 14||50 | TUBE|Yes|NIPDAU|Level-3-260C-168 HR|-40 to 85|OPA4340UA|
|Active|Production|SOIC (D) | 14|2500 | LARGE T&R||Yes|NIPDAU|Level-3-260C-168 HR|-40 to 85|OPA4340UA|
|Active|Production|SOIC (D) | 14|2500 | LARGE T&R||Yes|NIPDAU|Level-3-260C-168 HR|-40 to 85|OPA4340UA|
|Active|Production|SOIC (D) | 14|2500 | LARGE T&R||Yes|NIPDAU|Level-3-260C-168 HR|-40 to 85|OPA4340UA|
|Active|Production|SOIC (D) | 14||50 | TUBE|Yes|NIPDAU|Level-3-260C-168 HR|-40 to 85|OPA4340UA|

OPA340UA

OPA340UA.B

OPA340UA/2K5

OPA340UA/2K5.B

OPA340UA/2K5G4

OPA4340EA/250

OPA4340EA/250.B

OPA4340EA/250G4

OPA4340EA/2K5

OPA4340EA/2K5.B

OPA4340UA OPA4340UA.B OPA4340UA/2K5 OPA4340UA/2K5.B OPA4340UA/2K5G4 OPA4340UAG4

**(1)** **Status:** For more details on status, see our product life cycle.
**(2)** **Material type:** When designated, preproduction parts are prototypes/experimental devices, and are not yet approved or released for full production. Testing and final process, including without limitation quality assurance, reliability performance testing, and/or process qualification, may not yet be complete, and this item is subject to further changes or possible discontinuation. If available for ordering, purchases will be subject to an additional waiver at checkout, and are intended for early internal evaluation purposes only. These items are sold without warranties of any kind.
**(3)** **RoHS values:** Yes, No, RoHS Exempt. See the TI RoHS Statement for additional information and value definition.
Addendum-Page

### PACKAGE OPTION ADDENDUM

www.ti.com 15-Jul-2026

**(4)** **Lead finish/Ball material:** Parts may have multiple material finish options. Finish options are separated by a vertical ruled line. Lead finish/Ball material values may wrap to two lines if the finish value exceeds the maximum column width.
**(5)** **MSL rating/Peak reflow:** The moisture sensitivity level ratings and peak solder (reflow) temperatures. In the event that a part has multiple moisture sensitivity ratings, only the lowest level per JEDEC standards is shown. Refer to the shipping label for the actual reflow temperature that will be used to mount the part to the printed circuit board.
**(6)** **Part marking:** There may be an additional marking, which relates to the logo, the lot trace code information, or the environmental category of the part. Multiple part markings will be inside parentheses. Only one part marking contained in parentheses and separated by a "~" will appear on a part. If a line is indented then it is a continuation of the previous line and the two combined represent the entire part marking for that device. **Important Information and Disclaimer:** The information provided on this page represents TI's knowledge and belief as of the date that it is provided. TI bases its knowledge and belief on information provided by third parties, and makes no representation or warranty as to the accuracy of such information. Efforts are underway to better integrate information from third parties. TI has taken and continues to take reasonable steps to provide representative and accurate information but may not have conducted destructive testing or chemical analysis on incoming materials and chemicals. TI and TI suppliers consider certain information to be proprietary, and thus CAS numbers and other limited information may not be available for release. In no event shall TI's liability arising out of such information exceed the total purchase price of the TI part(s) at issue in this document sold by TI to Customer on an annual basis. **OTHER QUALIFIED VERSIONS OF OPA340 :** Enhanced Product : OPA340-EP • NOTE: Qualified Version Definitions: Enhanced Product-Supports Defense, Aerospace and Medical Applications •
Addendum-Page

### PACKAGE MATERIALS INFORMATION

www.ti.com 15-Jul-2026

##### TAPE AND REEL INFORMATION

**REEL DIMENSIONS TAPE DIMENSIONS** K0 P1

W B0 Reel Diameter Cavity A0

A0 Dimension designed to accommodate the component width B0 Dimension designed to accommodate the component length K0 Dimension designed to accommodate the component thickness W Overall width of the carrier tape P1 Pitch between successive cavity centers

Reel Width (W1) **QUADRANT ASSIGNMENTS FOR PIN 1 ORIENTATION IN TAPE**

Sprocket Holes

||Q1 Q2|Q1|Q2|||
|---|---|---|---|---|---|
||Q3 Q4|Q3|Q4|User Direction of Feed||

Pocket Quadrants

*All dimensions are nominal **Device Package Package Pins SPQ Reel Reel A0 B0 K0 P1 W Pin1** **Type Drawing Diameter Width (mm) (mm) (mm) (mm) (mm) Quadrant** **(mm) W1 (mm)**

|OPA2340EA/250|VSSOP|DGK|8 250|330.0|12.4|5.25|3.35|1.25|8.0 12.0|Q1|
|---|---|---|---|---|---|---|---|---|---|---|
|OPA2340EA/250|VSSOP|DGK|8 250|330.0|12.4|5.3|3.4|1.4|8.0 12.0|Q1|
|OPA2340EA/250|VSSOP|DGK|8 250|330.0|12.4|5.3|3.4|1.4|8.0 12.0|Q1|
|OPA2340EA/250G4|VSSOP|DGK|8 250|330.0|12.4|5.3|3.4|1.4|8.0 12.0|Q1|
|OPA2340EA/250G4|VSSOP|DGK|8 250|330.0|12.4|5.3|3.4|1.4|8.0 12.0|Q1|
|OPA2340EA/2K5|VSSOP|DGK|8 2500|330.0|12.4|5.25|3.35|1.25|8.0 12.0|Q1|
|OPA2340EA/2K5|VSSOP|DGK|8 2500|330.0|12.4|5.3|3.4|1.4|8.0 12.0|Q1|
|OPA2340EA/2K5|VSSOP|DGK|8 2500|330.0|12.4|5.3|3.4|1.4|8.0 12.0|Q1|
|OPA2340EA/2K5G4|VSSOP|DGK|8 2500|330.0|12.4|5.3|3.4|1.4|8.0 12.0|Q1|
|OPA2340EA/2K5G4|VSSOP|DGK|8 2500|330.0|12.4|5.3|3.4|1.4|8.0 12.0|Q1|
|OPA2340UA/2K5|SOIC|D|8 2500|330.0|12.4|6.4|5.2|2.1|8.0 12.0|Q1|
|OPA340NA/250|SOT-23|DBV|5 250|178.0|9.0|3.3|3.2|1.4|4.0 8.0|Q3|
|OPA340NA/250|SOT-23|DBV|5 250|179.0|8.4|3.2|3.2|1.4|4.0 8.0|Q3|
|OPA340NA/3K|SOT-23|DBV|5 3000|178.0|9.0|3.3|3.2|1.4|4.0 8.0|Q3|
|OPA340NA/3K|SOT-23|DBV|5 3000|179.0|8.4|3.2|3.2|1.4|4.0 8.0|Q3|
|OPA340UA/2K5|SOIC|D|8 2500|330.0|12.4|6.4|5.2|2.1|8.0 12.0|Q1|

OPA2340EA/250 VSSOP DGK 8 250 330.0 12.4 5.25 3.35 1.25 8.0 12.0 Q1

Pack Materials-Page

### PACKAGE MATERIALS INFORMATION

www.ti.com 15-Jul-2026

**Device Package Package Pins SPQ Reel Reel A0 B0 K0 P1 W Pin1** **Type Drawing Diameter Width (mm) (mm) (mm) (mm) (mm) Quadrant** **(mm) W1 (mm)** OPA4340EA/250 SSOP DBQ 16 250 180.0 12.4 6.4 5.2 2.1 8.0 12.0 Q1

|OPA4340EA/250|SSOP|DBQ|16|250|180.0|12.4|6.4 5.2|2.1 8.0|12.0|Q1|
|---|---|---|---|---|---|---|---|---|---|---|
|OPA4340EA/2K5|SSOP|DBQ|16|2500|330.0|12.4|6.4 5.2|2.1 8.0|12.0|Q1|
|OPA4340UA/2K5|SOIC|D|14|2500|330.0|16.4|6.5 9.0|2.1 8.0|16.0|Q1|

Pack Materials-Page

### PACKAGE MATERIALS INFORMATION

www.ti.com 15-Jul-2026

|TAPE AND REEL BOX DIMENSIONS *All dimensions are nominal|W||Width (mm) L||H||
|---|---|---|---|---|---|---|
||Device Package Type|Package Drawing|Pins||SPQ|Length (mm) Width (mm) Height (mm)|
|OPA2340EA/250|VSSOP||DGK 8||250|366.0 364.0 50.0|
|OPA2340EA/250|VSSOP||DGK 8||250|366.0 364.0 50.0|
|OPA2340EA/250|VSSOP||DGK 8||250|353.0 353.0 32.0|
|OPA2340EA/250G4|VSSOP||DGK 8||250|353.0 353.0 32.0|
|OPA2340EA/250G4|VSSOP||DGK 8||250|366.0 364.0 50.0|
|OPA2340EA/2K5|VSSOP||DGK 8||2500|366.0 364.0 50.0|
|OPA2340EA/2K5|VSSOP||DGK 8||2500|366.0 364.0 50.0|
|OPA2340EA/2K5|VSSOP||DGK 8||2500|353.0 353.0 32.0|
|OPA2340EA/2K5G4|VSSOP||DGK 8||2500|353.0 353.0 32.0|
|OPA2340EA/2K5G4|VSSOP||DGK 8||2500|366.0 364.0 50.0|
|OPA2340UA/2K5|SOIC||D 8||2500|353.0 353.0 32.0|
|OPA340NA/250|SOT-23||DBV 5||250|180.0 180.0 18.0|
|OPA340NA/250|SOT-23||DBV 5||250|213.0 191.0 35.0|
|OPA340NA/3K|SOT-23||DBV 5||3000|180.0 180.0 18.0|
|OPA340NA/3K|SOT-23||DBV 5||3000|213.0 191.0 35.0|
|OPA340UA/2K5|SOIC||D 8||2500|353.0 353.0 32.0|
|OPA4340EA/250|SSOP||DBQ 16||250|213.0 191.0 35.0|
|OPA4340EA/2K5|SSOP||DBQ 16||2500|353.0 353.0 32.0|

Pack Materials-Page

### PACKAGE MATERIALS INFORMATION

www.ti.com 15-Jul-2026

**Package Drawing**

|Device|Package Type|Pins|SPQ|Length (mm)|Width (mm)|Height (mm)||
|---|---|---|---|---|---|---|---|
|OPA4340UA/2K5|SOIC|14|2500|353.0|353.0|32.0||

D

Pack Materials-Page

### PACKAGE MATERIALS INFORMATION

www.ti.com 15-Jul-2026

##### TUBE

##### T-Tube height L-Tube length

##### W-Tube width

##### B-Alignment groove width

*All dimensions are nominal

|Device||Package Type|Pins|SPQ|L (mm)|W (mm)|T (µm)|B (mm)|
|---|---|---|---|---|---|---|---|---|
|OPA2340UA|D|SOIC|8|75|506.6|8|3940|4.32|
|OPA2340UA.B|D|SOIC|8|75|506.6|8|3940|4.32|
|OPA340PA|P|PDIP|8|50|506|13.97|11230|4.32|
|OPA340PA.B|P|PDIP|8|50|506|13.97|11230|4.32|
|OPA340UA|D|SOIC|8|75|506.6|8|3940|4.32|
|OPA340UA.B|D|SOIC|8|75|506.6|8|3940|4.32|
|OPA4340UA|D|SOIC|14|50|506.6|8|3940|4.32|
|OPA4340UA.B|D|SOIC|14|50|506.6|8|3940|4.32|
|OPA4340UAG4|D|SOIC|14|50|506.6|8|3940|4.32|

**Device Package Name Package Type Pins SPQ L (mm) W (mm) T (µm) B (mm)**

Pack Materials-Page

## PACKAGE OUTLINE

# D0008A <u>SOIC - 1.75 mm max height</u>

SCALE 2.800 SMALL OUTLINE INTEGRATED CIRCUIT

<u>C</u>

SEATING PLANE

.228-.244 TYP [5.80-6.19]

||[5.80-6.19]||.004 [0.1]|C|
|---|---|---|---|---|
|A|PIN 1 ID AREA|6X .050 [1.27]|||
|1||8|||

.004 [0.1] C
2X

.189-.197 [4.81-5.00].150 NOTE 3 [3.81]
4X (0 -15 )

4 5 8X .012-.020

B.150-.157 [0.31-0.51]

||B|.150-.157|[0.31-0.51]||.069 MAX|
|---|---|---|---|---|---|
|||[3.81-3.98] NOTE 4|.010 [0.25]|C A B|[1.75]|

.069 MAX
.005-.010 TYP [0.13-0.25]
4X (0 -15 )

SEE DETAIL A

.010 <u>[0.25]</u>
.004-.010
0 - 8 [0.11-0.25]

.016-.050 [0.41-1.27]DETAIL A
(.041) TYPICAL [1.04]

4214825/C 02/2019

NOTES:

1. Linear dimensions are in inches [millimeters]. Dimensions in parenthesis are for reference only. Controlling dimensions are in inches. Dimensioning and tolerancing per ASME Y14.5M.
2. This drawing is subject to change without notice.
3. This dimension does not include mold flash, protrusions, or gate burrs. Mold flash, protrusions, or gate burrs shall not exceed .006 [0.15] per side.
4. This dimension does not include interlead flash.
5. Reference JEDEC registration MS-012, variation AA.
www.ti.com

## EXAMPLE BOARD LAYOUT

# D0008A <u>SOIC - 1.75 mm max height</u>

|||||||SMALL OUTLINE INTEGRATED CIRCUIT|
|---|---|---|---|---|---|---|
||8X (.061|) [1.55] 1|||SYMM|SEE DETAILS|
|||||||8|
||8X (.024) [0.6]|4||||SYMM (R.002) TYP [0.05] 5|
|6X (.050|) [1.27]||||||
|METAL||||SOLDER MASK OPENING|(.213) [5.4] LAND PATTERN EXAMPLE EXPOSED METAL SHOWN SCALE:8X SOLDER MASK OPENING|METAL UNDER SOLDER MASK|
|EXPOSED|||||EXPOSED||
|METAL|[0.07] NON SOLDER MASK DEFINED|.0028 MAX ALL AROUND|||METAL SOLDER MASK DETAILS|.0028 MIN [0.07] ALL AROUND SOLDER MASK DEFINED 4214825/C 02/2019|

NOTES: (continued) 6. Publication IPC-7351 may have alternate designs. 7. Solder mask tolerances between and around signal pads can vary based on board fabrication site.

www.ti.com

## EXAMPLE STENCIL DESIGN

# D0008A <u>SOIC - 1.75 mm max height</u>

|||||SMALL OUTLINE INTEGRATED CIRCUIT|
|---|---|---|---|---|
|8X (.061 [1.55]|) 1||SYMM||
|||||8|
|8X (.024)|||||
|[0.6]|4|||SYMM (R.002) TYP [0.05] 5|
|6X (.050) [1.27]|||(.213) [5.4] SOLDER PASTE EXAMPLE BASED ON .005 INCH [0.125 MM] THICK STENCIL SCALE:8X|4214825/C 02/2019|

NOTES: (continued) design recommendations. 9. Board assembly site may have different recommendations for stencil design. 8. Laser cutting apertures with trapezoidal walls and rounded corners may offer better paste release. IPC-7525 may have alternate

www.ti.com

## PACKAGE OUTLINE

# DBQ0016A <u>SSOP - 1.75 mm max height</u>

SCALE 2.800 SHRINK SMALL-OUTLINE PACKAGE

C

SEATING PLANE

.228-.244 TYP [5.80-6.19].004 [0.1] C
<u>A</u> PIN 1 ID AREA 14X .0250 [0.635] 16 1

2X

.175
[.189 4.81-.197-5.00] [4.45] NOTE 3

<u>8</u> 9 16X .008-.012

|16X .008-.012|||
|---|---|---|
|[0.21-0.30]||.069 MAX|
|.007 [0.17]|C A B|[1.75]|

B.150-.157
[3.81-3.98] NOTE 4

.005-.010 TYP [0.13-0.25]
SEE DETAIL A

.010 <u>[0.25]</u>
GAGE PLANE

.004-.010
0 - 8 [0.11-0.25]

.016-.035 [0.41-0.88]
##### DETAIL A

(.041) TYPICAL [1.04]

4214846/A 03/2014

NOTES:

1. Linear dimensions are in inches [millimeters]. Dimensions in parenthesis are for reference only. Controlling dimensions are in inches. Dimensioning and tolerancing per ASME Y14.5M.
2. This drawing is subject to change without notice.
3. This dimension does not include mold flash, protrusions, or gate burrs. Mold flash, protrusions, or gate burrs shall not exceed .006 inch, per side.
4. This dimension does not include interlead flash.
5. Reference JEDEC registration MO-137, variation AB.
www.ti.com

## EXAMPLE BOARD LAYOUT

# DBQ0016A <u>SSOP - 1.75 mm max height</u>

SHRINK SMALL-OUTLINE PACKAGE

16X (.063) [1.6] SEE SYMM DETAILS <u>1</u> 16

16X (.016) [0.41]

14X (.0250) [0.635] 8 9

(.213) [5.4]

##### LAND PATTERN EXAMPLE

SCALE:8X

SOLDER MASK SOLDER MASK METAL METAL OPENING OPENING

.002 MAX.002 MIN [0.05] [0.05] ALL AROUND ALL AROUND
NON SOLDER MASK SOLDER MASK DEFINED DEFINED

##### SOLDER MASK DETAILS

4214846/A 03/2014

NOTES: (continued)

6. Publication IPC-7351 may have alternate designs.
7. Solder mask tolerances between and around signal pads can vary based on board fabrication site.
www.ti.com

## EXAMPLE STENCIL DESIGN

# DBQ0016A <u>SSOP - 1.75 mm max height</u>

SHRINK SMALL-OUTLINE PACKAGE

16X (.063) [1.6] SYMM <u>1</u> 16

16X (.016) [0.41] SYMM

14X (.0250) [0.635] 8 9

(.213) [5.4]

##### SOLDER PASTE EXAMPLE

BASED ON .005 INCH [0.127 MM] THICK STENCIL SCALE:8X

4214846/A 03/2014

NOTES: (continued)

8. Laser cutting apertures with trapezoidal walls and rounded corners may offer better paste release. IPC-7525 may have alternate design recommendations.
9. Board assembly site may have different recommendations for stencil design.
www.ti.com

## PACKAGE OUTLINE

# DBV0005A <u>SOT-23 - 1.45 mm max height</u>

SCALE 4.000 SMALL OUTLINE TRANSISTOR

3.0 C
2.6
<u>0.1 C</u>

|||1.75|||0.1 C|
|---|---|---|---|---|---|
|PIN 1 INDEX AREA||1.45|B|A||
||1||5|||
|2X 0.95|||(0.1)|||
|||||3.05||
|||||2.75||
|1.9|2||(0.15)|1.9||

1.75
4 3 5X 0.5

0.3
0.15 TYP
0.2 C A B NOTE 5 (1.1)

|0.2|C A B|NOTE 5|(1.1)|0.15 TYP 0.00|
|---|---|---|---|---|
||||1.45||
|||4X 4 -15|0.90||

4X 0 -15

0.25
GAGE PLANE 0.22 TYP

0.08
8

0.6 TYP
0 TYP

0.3 SEATING PLANE
4214839/K 08/2024

NOTES:

1. All linear dimensions are in millimeters. Any dimensions in parenthesis are for reference only. Dimensioning and tolerancing per ASME Y14.5M.
2. This drawing is subject to change without notice.
3. Refernce JEDEC MO-178.
4. Body dimensions do not include mold flash, protrusions, or gate burrs. Mold flash, protrusions, or gate burrs shall not exceed 0.25 mm per side.
5. Support pin may differ or may not be present.
www.ti.com

## EXAMPLE BOARD LAYOUT

# DBV0005A <u>SOT-23 - 1.45 mm max height</u>

|||||||||||SMALL OUTLINE TRANSISTOR|
|---|---|---|---|---|---|---|---|---|---|---|
||2X (0.95)|1 5X (0.6) 2|||5X (1.1)|PKG|||5 SYMM (1.9)||
|||3 (R0.05) TYP|||||||4||
|SOLDER MASK OPENING|||||METAL|(2.6) LAND PATTERN EXAMPLE EXPOSED METAL SHOWN SCALE:15X|METAL UNDER SOLDER MASK|||SOLDER MASK OPENING|
|EXPOSED METAL||0.07 MAX ARROUND NON SOLDER MASK DEFINED (PREFERRED)||||EXPOSED METAL SOLDER MASK DETAILS|||0.07 MIN ARROUND SOLDER MASK DEFINED|4214839/K 08/2024|

NOTES: (continued) 6. Publication IPC-7351 may have alternate designs. 7. Solder mask tolerances between and around signal pads can vary based on board fabrication site.

www.ti.com

## EXAMPLE STENCIL DESIGN

# DBV0005A <u>SOT-23 - 1.45 mm max height</u>

||||||SMALL OUTLINE TRANSISTOR|
|---|---|---|---|---|---|
|1|5X (1.1)|PKG||||
|5X (0.6)||||5||
|2||||SYMM (1.9)||
|2X(0.95)||||||
|3||||4||
|(R0.05) TYP||(2.6) SOLDER PASTE EXAMPLE BASED ON 0.125 mm THICK STENCIL SCALE:15X|||4214839/K 08/2024|

NOTES: (continued) design recommendations. 9. Board assembly site may have different recommendations for stencil design. 8. Laser cutting apertures with trapezoidal walls and rounded corners may offer better paste release. IPC-7525 may have alternate

www.ti.com

## PACKAGE OUTLINE

# DGK0008A VSSOP - 1.1 mm max height

SCALE 4.000 SMALL OUTLINE PACKAGE

<u>C</u>

5.05 TYP
A 4.75

<u>0.1 C</u>
PIN 1 INDEX AREA SEATING PLANE <u>6X 0.65</u> 8 1

2X

3.1
1.95
2.9
NOTE 3

4 5 8X 0.38

<u>0.25</u>
3.1 <u>0.13 C A B</u>
<u>B</u>

2.9
NOTE 4

0.23
0.13
SEE DETAIL A

<u>0.25</u> GAGE PLANE
1.1 MAX
0.15
0.7
0 -8 0.05

0.4
A 20 DETAIL A TYPICAL

4214862/A 04/2023 PowerPAD is a trademark of Texas Instruments. NOTES:

1. All linear dimensions are in millimeters. Any dimensions in parenthesis are for reference only. Dimensioning and tolerancing per ASME Y14.5M.
2. This drawing is subject to change without notice.
3. This dimension does not include mold flash, protrusions, or gate burrs. Mold flash, protrusions, or gate burrs shall not exceed 0.15 mm per side.
4. This dimension does not include interlead flash. Interlead flash shall not exceed 0.25 mm per side.
5. Reference JEDEC registration MO-187.
www.ti.com

## EXAMPLE BOARD LAYOUT

TM

# DGK0008A <u>VSSOP - 1.1 mm max height</u>

||||SMALL OUTLINE PACKAGE|
|---|---|---|---|
||8X (1.4)||SYMM (R0.05) TYP|
|8X (0.45) 1|||8|
||||SYMM|
|6X (0.65)||||
||||5|
|4|||SEE DETAILS|
|SOLDER MASK OPENING|||(4.4) LAND PATTERN EXAMPLE EXPOSED METAL SHOWN SCALE: 15X SOLDER MASK METAL UNDER METAL OPENING SOLDER MASK|
|EXPOSED METAL|||EXPOSED METAL|
||NON-SOLDER MASK DEFINED (PREFERRED)|0.05 MAX ALL AROUND|0.05 MIN ALL AROUND SOLDER MASK DEFINED 15.000 SOLDER MASK DETAILS 4214862/A 04/2023|

NOTES: (continued) 6. Publication IPC-7351 may have alternate designs. 9. Size of metal pad may vary due to creepage requirement. on this view. It is recommended that vias under paste be filled, plugged or tented. 7. Solder mask tolerances between and around signal pads can vary based on board fabrication site. 8. Vias are optional depending on application, refer to device data sheet. If any vias are implemented, refer to their locations shown

www.ti.com

## EXAMPLE STENCIL DESIGN

TM

# DGK0008A <u>VSSOP - 1.1 mm max height</u>

|||SMALL OUTLINE PACKAGE|
|---|---|---|
||8X (1.4)|SYMM (R0.05) TYP|
|1 8X (0.45)||8|
|||SYMM|
|6X (0.65)|||
|4||5 (4.4) SOLDER PASTE EXAMPLE SCALE: 15X 4214862/A 04/2023|

NOTES: (continued) design recommendations. 12. Board assembly site may have different recommendations for stencil design. 11. Laser cutting apertures with trapezoidal walls and rounded corners may offer better paste release. IPC-7525 may have alternate

www.ti.com

## PACKAGE OUTLINE

# D0014A <u>SOIC - 1.75 mm max height</u>

SCALE 1.800 SMALL OUTLINE INTEGRATED CIRCUIT

C

6.2
SEATING PLANE

5.8 TYP

|A|PIN 1 ID||0.1 C|
|---|---|---|---|
||AREA|12X 1.27||
|1||14||

8.75 2X
8.55 7.62
NOTE 3

7 8 14X 0.51

||4.0|14X 0.51 0.31||
|---|---|---|---|
|B|3.8 NOTE 4|0.25|C A B|

0.31
1.75 MAX
0.25
0.13 TYP
SEE DETAIL A

<u>0.25</u>
GAGE PLANE

0.25
1.27
0 - 8 0.10

0.40
##### DETAIL A

TYPICAL

4220718/A 09/2016

NOTES:

1. All linear dimensions are in millimeters. Dimensions in parenthesis are for reference only. Dimensioning and tolerancing per ASME Y14.5M.
2. This drawing is subject to change without notice.
3. This dimension does not include mold flash, protrusions, or gate burrs. Mold flash, protrusions, or gate burrs shall not exceed 0.15 mm, per side.
4. This dimension does not include interlead flash. Interlead flash shall not exceed 0.43 mm, per side.
5. Reference JEDEC registration MS-012, variation AB.
www.ti.com

## EXAMPLE BOARD LAYOUT

# D0014A <u>SOIC - 1.75 mm max height</u>

|||SMALL OUTLINE INTEGRATED CIRCUIT|
|---|---|---|
|14X (1.55) 1||SYMM|
|||14|
|14X (0.6)|||
|12X (1.27)||SYMM|
|7||8|
|(R0.05) TYP|||
|SOLDER MASK OPENING|METAL|(5.4) LAND PATTERN EXAMPLE SCALE:8X SOLDER MASK METAL UNDER OPENING SOLDER MASK|
|0.07 MAX ALL AROUND NON SOLDER MASK DEFINED||0.07 MIN ALL AROUND SOLDER MASK DEFINED SOLDER MASK DETAILS 4220718/A 09/2016|

NOTES: (continued) 6. Publication IPC-7351 may have alternate designs. 7. Solder mask tolerances between and around signal pads can vary based on board fabrication site.

www.ti.com

## EXAMPLE STENCIL DESIGN

# D0014A <u>SOIC - 1.75 mm max height</u>

|||SMALL OUTLINE INTEGRATED CIRCUIT|
|---|---|---|
|14X (1.55) 1||SYMM|
|||14|
|14X (0.6)|||
|12X (1.27)||SYMM|
|7||8 (5.4) SOLDER PASTE EXAMPLE BASED ON 0.125 mm THICK STENCIL SCALE:8X 4220718/A 09/2016|

NOTES: (continued) design recommendations. 9. Board assembly site may have different recommendations for stencil design. 8. Laser cutting apertures with trapezoidal walls and rounded corners may offer better paste release. IPC-7525 may have alternate

www.ti.com

#### IMPORTANT NOTICE AND DISCLAIMER

TI PROVIDES TECHNICAL AND RELIABILITY DATA (INCLUDING DATASHEETS), DESIGN RESOURCES (INCLUDING REFERENCE DESIGNS), APPLICATION OR OTHER DESIGN ADVICE, WEB TOOLS, SAFETY INFORMATION, AND OTHER RESOURCES “AS IS” AND WITH ALL FAULTS, AND DISCLAIMS ALL WARRANTIES, EXPRESS AND IMPLIED, INCLUDING WITHOUT LIMITATION ANY IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE OR NON-INFRINGEMENT OF THIRD PARTY INTELLECTUAL PROPERTY RIGHTS. These resources are intended for skilled developers designing with TI products. You are solely responsible for (1) selecting the appropriate TI products for your application, (2) designing, validating and testing your application, and (3) ensuring your application meets applicable standards, and any other safety, security, regulatory or other requirements. These resources are subject to change without notice. TI grants you permission to use these resources only for development of an application that uses the TI products described in the resource. Other reproduction and display of these resources is prohibited. No license is granted to any other TI intellectual property right or to any third party intellectual property right. TI disclaims responsibility for, and you fully indemnify TI and its representatives against any claims, damages, costs, losses, and liabilities arising out of your use of these resources. TI’s products are provided subject to TI’s Terms of Sale, TI’s General Quality Guidelines, or other applicable terms available either on ti.com or provided in conjunction with such TI products. TI’s provision of these resources does not expand or otherwise alter TI’s applicable warranties or warranty disclaimers for TI products. Unless TI explicitly designates a product as custom or customer-specified, TI products are standard, catalog, general purpose devices. TI objects to and rejects any additional or different terms you may propose. IMPORTANT NOTICE

Copyright © 2026, Texas Instruments Incorporated Last updated 10/2025
