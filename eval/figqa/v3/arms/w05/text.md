**LP5907** SNVS798Q – APRIL 2012 – REVISED JULY 2025

## LP5907 250mA, Low-Noise, Low-I

**Q** **LDO**

#### 1 Features 3 Description

- For a more updated portfolio device, see the The LP5907 is a low-noise LDO that can supply TPS7A20 up to 250mA output current. Designed to meet the
- Input voltage range: 2.2V to 5.5V
requirements of RF and analog circuits, the LP5907

- Output voltage range: 1.2V to 4.5V
provides low noise, high PSRR, low quiescent current,

- Stable with 1-µF ceramic input and output
and low line or load transient response figures. Using capacitors innovative design techniques, the LP5907 offers

- No noise bypass capacitor required
class-leading noise performance without a noise

- Remote output capacitor placement
bypass capacitor and the ability for remote output

- Thermal-overload and short-circuit protection capacitor placement.
- Operating junction temperature: –40°C to 125°C
The device is designed to work with a 1µF input and

- Low output voltage noise: < 6.5µVRMS
a 1µF output ceramic capacitor (no separate noise

- PSRR: 82dB at 1kHz
bypass capacitor is required).

- Output voltage tolerance: ±2%
- Very low IQ (enabled): 12μA This device is available with fixed output voltages
- Low dropout: 120mV (typical)
from 1.2V to 4.5V in 25mV steps. Contact Texas

- Create a custom design using the LP5907 with the Instruments Sales for specific voltage option needs. WEBENCH® Power Designer
##### Package Information

|PART NUMBER|PACKAGE|(1)PACKAGE SIZE|
|---|---|---|
||YKE, YKG, YKM,|0.685mm × 0.685mm|
||YCR (DSBGA, 4)||
|LP5907 Orderable Information. includes pins, where applicable.|DBV (SOT-23, 5) DQN (X2SON, 4)|2.9mm × 2.8mm 1mm × 1mm|

(1) For more information, see the Mechanical, Packaging, and
(2) The package size (length × width) is a nominal value and

#### 2 Applications

(2)
- Smartphones
- Tablets
- Communications equipment
- Digital still cameras
- Factory automation
##### INPUT IN OUT OUTPUT

1 F 1 F

##### LP5907

##### ENABLE EN

GND

GND

##### Simplified Schematic

An IMPORTANT NOTICE at the end of this data sheet addresses availability, warranty, changes, use in safety-critical applications, intellectual property matters and other important disclaimers. PRODUCTION DATA.

**LP5907** <u>www.ti.com</u> <u>SNVS798Q – APRIL 2012 – REVISED JULY 2025</u>

#### Table of Contents

**1 Features**............................................................................1
**2 Applications**..................................................................... 1
**3 Description**.......................................................................1
**4 Pin Configuration and Functions**................................... 3
**5 Specifications**.................................................................. 4

5.1 Absolute Maximum Ratings........................................ 4
5.2 ESD Ratings............................................................... 4
5.3 Recommended Operating Conditions.........................4
5.4 Thermal Information....................................................5
5.5 Electrical Characteristics.............................................5
5.6 Output and Input Capacitors....................................... 6
5.7 Typical Characteristics................................................ 7
**6 Detailed Description**...................................................... 11

6.1 Overview................................................................... 11
6.2 Functional Block Diagram......................................... 11
6.3 Feature Description................................................... 11
6.4 Device Functional Modes..........................................12
**7 Application and Implementation**.................................. 13

7.1 Application Information............................................. 13
7.2 Typical Application.................................................... 13
7.3 Power Supply Recommendations.............................16
7.4 Layout....................................................................... 17
**8 Device and Documentation Support**............................19

8.1 Documentation Support............................................ 19
8.2 Receiving Notification of Documentation Updates....19
8.3 Support Resources................................................... 19
8.4 Trademarks............................................................... 19
8.5 Electrostatic Discharge Caution................................19
8.6 Glossary....................................................................19
**9 Revision History**............................................................ 20
**10 Mechanical, Packaging, and Orderable**
**Information**.................................................................... 20

*Submit Document Feedback* Copyright © 2025 Texas Instruments Incorporated *LP5907* Product Folder Links:

**LP5907** **www.ti.com** SNVS798Q – APRIL 2012 – REVISED JULY 2025

#### 4 Pin Configuration and Functions

IN OUT OUT IN A1 A2 A2 A1

B1 B2 B2 B1 EN GND GND EN TOP VIEW BOTTOM VIEW

**Figure 4-1. YKE, YKG, YKM, and YCR Packages, 4-Pin DSBGA**

||Table 4-1. Pin Functions: DSBGA|
|---|---|
|PIN|TYPE DESCRIPTION|
|DSBGA NAME||

A1 IN I Input voltage supply. Connect a 1µF capacitor at this input. Regulated output voltage. Connect a minimum 1µF low-ESR capacitor to this pin. Connect A2 OUT O this output to the load circuit. An internal 230Ω (typical) pulldown resistor prevents a charge remaining on VOUT when the regulator is in the shutdown mode (VEN low). Enable input. A low voltage (< VIL) on this pin turns the regulator off and discharges the B1 EN I output pin to GND through an internal 230Ω pulldown resistor. A high voltage (> V pin enables the regulator output. This pin has an internal 1MΩ pulldown resistor to hold the IH) on this

regulator off by default. B2 GND — Common ground

5 OUT GND 21 IN1 OUT

5 GND 2

EN N/C 4 3 IN EN

**Figure 4-3. DBV Package, 5-Pin SOT-23**

**Figure 4-2. DQN Package, 4-Pin X2SON**

##### (Top View)

##### (Bottom View)

||Table 4-2. Pin Functions: X2SON, SOT-23|
|---|---|
|PIN|TYPE DESCRIPTION|
|NAME X2SON|SOT-23|

Enable input. A low voltage (< VIL) on this pin turns the regulator off and EN 3 3 I discharges the output pin to GND through an internal 230Ω pulldown resistor.

|EN|3|3|I discharges the output pin to GND through an internal 230Ω pulldown resistor. A high voltage (> V||IH) on this pin enables the regulator output. This pin has an|||
|---|---|---|---|---|---|---|---|
||||internal 1MΩ pulldown resistor to hold the regulator off by default.|||||
|GND|2|2|— Common ground.|||||
|IN|4|1|I Input voltage supply. Connect a 1µF capacitor at this input.|||||
|N/C|—|4|— No internal electrical connection. Regulated output voltage. Connect a minimum 1µF low-ESR capacitor to this|||||
|OUT|1|5|O pin. Connect this output to the load circuit. An internal 230Ω (typical) pulldown resistor prevents a charge remaining on V mode (V|ENlow).|||OUTwhen the regulator is in shutdown|
|Thermal Pad|5|—|— Thermal pad for the X2SON package, connect to GND or leave floating. Do not connect to any potential other than GND.|||||

Copyright © 2025 Texas Instruments Incorporated *Submit Document Feedback* Product Folder Links: *LP5907*

**LP5907** SNVS798Q – APRIL 2012 – REVISED JULY 2025 <u>www.ti.com</u>

#### 5 Specifications

##### 5.1 Absolute Maximum Ratings

over operating free-air temperature range (unless otherwise noted)

(1) (3)
**MIN MAX UNIT** VINInput voltage –0.3 6 V VOUTOutput voltage –0.3 See(2)V VENEnable input voltage –0.3 6 V Continuous power dissipation(4)<u>Internally limited</u> W T JMAXJunction temperature 150 °C T stgStorage temperature –65 150 °C

(1) Stresses beyond those listed under *Absolute Maximum Ratings* may cause permanent damage to the device. These are stress ratings only, and functional operation of the device at these or any other conditions beyond those indicated under the *Recommended* *Operating Conditions* is not implied. Exposure to absolute-maximum-rated conditions for extended periods may affect device reliability.
(2) Abs Max VOUT is the lessor of VIN + 0.3V, or 6V.
(3) All voltages are with respect to the GND pin.
(4) Internal thermal shutdown circuitry protects the device from permanent damage.
##### 5.2 ESD Ratings

|||VALUE|UNIT|
|---|---|---|---|
||Human-body model (HBM), per ANSI/ESDA/JEDEC JS-001|±2000||
|V(ESD)Electrostatic discharge|Charged-device model (CDM), per JEDEC specification JESD22-C101|(2)±1000|V|

(1) JEDEC document JEP155 states that 500V HBM allows safe manufacturing with a standard ESD control process.
(2) JEDEC document JEP157 states that 250V CDM allows safe manufacturing with a standard ESD control process.

(1)
##### 5.3 Recommended Operating Conditions

over operating free-air temperature range (unless otherwise noted)

(1) (2)
**MIN MAX UNIT** VINInput supply voltage 2.2 5.5 V VENEnable input voltage 0 5.5 V I OUTOutput current 0 250 mA T JJunction temperature –40 125 °C T AAmbient temperature

(3)–40 85 °C
(1) Stresses beyond those listed under *Absolute Maximum Ratings* may cause permanent damage to the device. These are stress ratings only, and functional operation of the device at these or any other conditions beyond those indicated under *Recommended Operating* *Conditions* is not implied. Exposure to absolute-maximum-rated conditions for extended periods may affect device reliability.
(2) All voltages are with respect to the GND pin.
(3) In applications where high power dissipation and poor package thermal resistance is present, the maximum ambient temperature can need to be derated. Maximum ambient temperature (TA-MAX) is dependent on the maximum operating junction temperature (TJ-MAX-OP = 125°C), the maximum power dissipation of the device in the application (PD-MAX), and the junction-to ambient thermal resistance of the device or package in the application (RθJA), as given by the following equation: TA-MAX = TJ-MAX-OP – (RθJA × PD-MAX). See the *Application and Implementation* section.
*Submit Document Feedback* Copyright © 2025 Texas Instruments Incorporated

**LP5907** <u>www.ti.com SNVS798Q – APRIL 2012 – REVISED JULY 2025</u>

##### 5.4 Thermal Information

||DBV (SOT-23)|DQN (X2SON)|YCR (DSBGA)|YKE (DSBGA)|YKG (DSBGA)|YKM (DSBGA)||
|---|---|---|---|---|---|---|---|
||5 PINS|4 PINS|4 PINS|4 PINS|4 PINS|4 PINS||

(1) THERMAL METRIC LP5907 UNIT

|RθJA|Junction-to-ambient thermal resistance|193.4|216.1|189.4|206.1|191.6|194.1|°C/W|
|---|---|---|---|---|---|---|---|---|
|RθJC(top)|Junction-to-case (top) thermal resistance|102.1|161.7|2.4|1.5|2.4|3.0|°C/W|
|RθJB|Junction-to-board thermal resistance|45.8|162.1|56.6|37.0|58.9|62.7|°C/W|
|ψJT|Junction-to-top characterization parameter|8.4|5.1|1.1|15.0|1.1|1.1|°C/W|
|ψJB|Junction-to-board characterization parameter|45.3|161.7|56.5|36.8|58.9|62.7|°C/W|
|RθJC(bot) note.|Junction-to-case (bottom) thermal resistance|n/a|123.0|n/a|n/a|n/a|n/a|°C/W|

(1) For more information about traditional and new thermal metrics, see the Semiconductor and IC Package Thermal Metrics application

##### 5.5 Electrical Characteristics

(1) (2) (3)
VIN = VOUT(NOM) + 1V, VEN = 1.2V, IOUT = 1mA, CIN = 1µF, and COUT = 1µF (unless otherwise noted) **PARAMETER TEST CONDITIONS MIN TYP MAX UNIT** VINInput voltage TA = 25°C 2.2 5.5 V VIN = (VOUT(NOM) + 1V) to 5.5V, –2 2 IOUT = 1mA to 250mA Output voltage tolerance VIN = (VOUT(NOM) + 1V) to 5.5V, %VOUT IOUT = 1mA to 250mA –3 3 ΔVOUT(VOUT < 1.8V, SOT-23, X2SON packages)

IN = (VOUT(NOM) + 1V) to 5.5V, Line regulation 0.02 %/V IVOUT = 1mA Load regulation IOUT = 1mA to 250mA 0.001 %/mA Load current See(4)0 250 mA ILOAD Maximum output current 250 mA VEN = 1.2V, IOUT = 0mA 12 25 I(5)VEN = 1.2V, IOUT = 250mA 250 425 μA QQuiescent current VEN = 0.3V (disabled) 0.2 1 I(6)VEN = 1.2V, IOUT = 0mA 14 μA GGround current IOUT = 100mA 50 VDODropout voltage(7)IOUT = 250mA (DSBGA package) 120 200 mV IOUT = 250mA (SOT-23, X2SON packages) 250 ISCShort-circuit current limit TA = 25°C(8)250 500 mA f = 100Hz, IOUT = 20mA 90 f = 1kHz, IOUT = 20mA 82 PSRR Power-supply rejection ratio(9)dB f = 10kHz, IOUT = 20mA 65 f = 100kHz, IOUT = 20mA 60 <u>IOUT = 1mA</u> 10 e(9)BW = 10Hz to 100kHz µVRMS NOutput noise voltage <u>IOUT = 250mA</u> 6.5 Output automatic discharge RADVEN < VIL (output disabled) 230 Ω pulldown resistance Thermal shutdown TJ rising 160 TSD°C Thermal hysteresis TJ falling from shutdown <u>LOGIC INPUT THRESHOLDS</u>

Copyright © 2025 Texas Instruments Incorporated *Submit Document Feedback*

**LP5907** <u>SNVS798Q – APRIL 2012 – REVISED JULY 2025 www.ti.com</u>

##### 5.5 Electrical Characteristics (continued)

(1) (2) (3)
VIN = VOUT(NOM) + 1V, VEN = 1.2V, IOUT = 1mA, CIN = 1µF, and COUT = 1µF (unless otherwise noted) **PARAMETER TEST CONDITIONS MIN TYP MAX UNIT** VIN = 2.2V to 5.5V, VILLow input threshold 0.4 V VEN falling until the output is disabled VIN = 2.2V to 5.5V VIHHigh input threshold 1.2 V VEN rising until the output is enabled VEN = 5.5V and VIN = 5.5V 5.5 I(10)μA ENInput current at EN pin VEN = 0V and VIN = 5.5V 0.001 <u>TRANSIENT CHARACTERISTICS</u> VIN = (VOUT(NOM) + 1V) to –1 (VOUT(NOM) + 1.6V) in 30µs Line transient(9) VIN = (VOUT(NOM) + 1.6V) to 1 mV (VOUT(NOM) + 1.6V) in 30µs IOUT = 1mA to 250mA in 10µs –40 Load transient(9) ΔVOUT I 40 OUT = 250mA to 1mA in 10µs Overshoot on start-up(9)Stated as a percentage of VOUT(NOM)5% Stated as a percentage of VOUT(NOM), VIN = VOUT + 1V to 5.5V, 0.7µF < COUT < 10µF, 0mA Overshoot on start-up with EN(9)1% < IOUT < 250mA, EN rising until the output is enabled From VEN > VIH to VOUT = 95% of VOUT(NOM), tONTurn-on time 80 150 µs TA = 25°C

(1) All voltages are with respect to the device GND terminal, unless otherwise stated.
(2) Minimum and maximum limits are specified through test, design, or statistical correlation over the junction temperature (TJ) range of –40°C to 125°C, unless otherwise stated. Typical values represent the most likely parametric norm at TA = 25°C, and are provided for reference purposes only.
(3) In applications where high power dissipation or poor package thermal resistance is present, the maximum ambient temperature can possibly have to be derated. Maximum ambient temperature (TA-MAX) is dependent on the maximum operating junction temperature (TJ-MAX-OP = 125°C), the maximum power dissipation of the device in the application (PD-MAX), and the junction-to ambient thermal resistance of the device or package in the application RθJA ), as given by the following equation: TA-MAX = TJ-MAX-OP – (RθJA × PD-MAX). See the *Application and Implementation* section.
(4) The device maintains a stable, regulated output voltage without a load current.
(5) Quiescent current is defined here as the difference in current between the input voltage source and the load at VOUT.
(6) Ground current is defined here as the total current flowing to ground as a result of all input voltages applied to the device.
(7) Dropout voltage is the voltage difference between the input and the output at which the output voltage drops to 100mV below the nominal value.
(8) Short-circuit current (ISC) for the LP5907 is equivalent to current limit. To minimize thermal effects during testing, ISC is measured with VOUT pulled to 100mV below the nominal voltage.
(9) This specification is verified by design. (10) There is a 1MΩ resistor between EN and ground on the device.
##### 5.6 Output and Input Capacitors

over operating free-air temperature range (unless otherwise noted)

(1)

||PARAMETER||TEST CONDITIONS|MIN(1)|TYP|MAX|UNIT|
|---|---|---|---|---|---|---|---|
|CIN|Input capacitance|(2)||0.7|1||µF|
|COUT|Output capacitance|(2)|Capacitance for stability|0.7|1|10|µF|
|ESR 30% or better over the full temperature range. The full range of operating conditions for the capacitor in the application must be considered during device selection to make sure this minimum capacitance specification is met. X7R capacitors are recommended, however capacitor types X5R, Y5V, and Z5U can be used with consideration of the application and conditions.|Output/input capacitance|(2)||5||500|mΩ|

(1) The minimum capacitance must be greater than 0.7µF over the full range of operating conditions. The capacitor tolerance must be
(2) This specification is verified by design.

*Submit Document Feedback* Copyright © 2025 Texas Instruments Incorporated

**LP5907** <u>www.ti.com SNVS798Q – APRIL 2012 – REVISED JULY 2025</u>

|5.7 Typical Characteristics V = 3.7V, V = 2.8V, I = 1mA, C = 1µF, C = 1µF, and T IN OUT OUT IN OUT|= 25°C (unless otherwise noted) A|
|---|---|
|16 14 12 A) 10 (8 Q I 6 4 2 0 2.3 2.8 3.3 3.8 4.3 4.8 5.3 5.8 V (V) IN SVA-30180569 Figure 5-1. Quiescent Current vs Input Voltage|1 0.9 0.8 VEN (V) 0.7 0.6 VIH Rising VIL Falling 0.5 2 2.5 3 3.5 4 4.5 5 5.5 6 VIN (V) D001 Figure 5-2. V Thresholds vs V EN IN|
|1.4 1.2 1 0.8 0.6 VOUT (V) 0.4 0.2 RLOAD = 1.2 k RLOAD = 4.8 : 0 0 0.5 1 1.5 2 2.5 VIN (V) D002 A) V = 1.2V, V = V OUT EN IN Figure 5-3. V vs V OUT IN|5 4.5 4 3.5 3 2.5 VOUT (V) 2 1.5 1 RLOAD = 4.5 k : 0.5 RLOAD = 18 : 0 0 1 2 3 4 5 6 VIN (V) D003 V = 4.5V, V = V OUT EN IN Figure 5-4. V vs V OUT IN|
|350 300 250 200 150 100 VIN = 3.0V GROUND CURRENT (VIN = 3.8V 50 VIN = 4.2V VIN = 5.5V 0 0 50 100 150 200 250 300 I OUT (mA) SVA-30180571 Figure 5-5. Ground Current vs Output Current|V = 3.6V IN (V) 2.800 OUT V 2.775 2.750 -40°C 90°C 2.725 25°C 2.700 0 50 100 150 200 250 LOAD (mA) SVA-30180567 Figure 5-6. Load Regulation|

:

2.900
2.875
2.850
2.825
Copyright © 2025 Texas Instruments Incorporated *Submit Document Feedback*

**LP5907** <u>SNVS798Q – APRIL 2012 – REVISED JULY 2025 www.ti.com</u>

|5.7 Typical Characteristics (continued) V = 3.7V, V = 2.8V, I = 1mA, C = 1µF, C = 1µF, and T IN OUT OUT IN OUT|= 25°C (unless otherwise noted) A|
|---|---|
|0.2 0.1 0 (%) -0.1 OUT V ' -0.2 -0.3 -0.4 -50 -25 0 25 50 75 100 125 D010 Junction Temperature (q C) Figure 5-7. ΔV vs Temperature OUT|Load = 10 mA (V) 2.800 OUT V 2.775 2.750 -40°C 90°C 2.725 25°C 2.700 3.0 3.5 4.0 4.5 5.0 5.5 V (V) IN SVA-30180568 Figure 5-8. Line Regulation|
|V OUT V V IN = EN I IN 2 ms/DIV SVA-30180509 Figure 5-9. Inrush Current|2V/DIV2V/DIV V OUT (AC Coupled) 1A/DIV V IN 10 s/DIV SVA-30180510 V = 3.2V ↔ 4.2V, load = 1mA IN Figure 5-10. Line Transient|
|V OUT (AC Coupled) V IN 10 s/DIV SVA-30180511 V = 3.2V ↔ 4.2V, load = 250mA IN Figure 5-11. Line Transient|10 mV/ V OUT DIV 1V/DIV LOAD 100 s/DIV SVA-30180512 Load = 0mA ↔ 250mA, –40°C Figure 5-12. Load Transient|

2.900
2.875
2.850
2.825
10 mV/ DIV

1V/DIV

100 mV/DIV

200 mA/DIV

*Submit Document Feedback* Copyright © 2025 Texas Instruments Incorporated

**LP5907** <u>www.ti.com SNVS798Q – APRIL 2012 – REVISED JULY 2025</u>

|5.7 Typical Characteristics (continued) V = 3.7V, V = 2.8V, I = 1mA, C = 1µF, C = 1µF, and T IN OUT OUT IN OUT|= 25°C (unless otherwise noted) A|
|---|---|
|V OUT LOAD 100 s/DIV SVA-30180513 Load = 0mA ↔ 250mA, 90°C Figure 5-13. Load Transient|100 mV/DIV V OUT 200 mA/DIV LOAD 100 s/DIV SVA-30180514 Load = 0mA ↔ 250mA, 25°C Figure 5-14. Load Transient|
|V OUT EN 20 s/DIV SVA-30180515 Load = 0mA Figure 5-15. Start-Up|1V/DIV V OUT 1V/DIV EN 20 s/DIV SVA-30180516 Load = 250mA Figure 5-16. Start-Up|
|Figure 5-17. Noise Density Test|140 120 100 80 60 40 Dropout Voltage DROPOUT VOLTAGE (mV) 20 0 0 50 100 150 200 250 LOAD CURRENT (mA) SVA-30180573 Figure 5-18. Dropout Voltage vs Load Current|

100 mV/DIV

200 mA/DIV

1V/DIV

1V/DIV

Copyright © 2025 Texas Instruments Incorporated *Submit Document Feedback*

**LP5907** <u>SNVS798Q – APRIL 2012 – REVISED JULY 2025 www.ti.com</u>

##### 5.7 Typical Characteristics (continued)

VIN = 3.7V, VOUT = 2.8V, IOUT = 1mA, CIN = 1µF, COUT = 1µF, and TA = 25°C (unless otherwise noted)

0 0 250 mA 200 mA -20 150 mA-20 100 mA -40 50 mA 20 mA-40 -60-60 PSRR (dB) PSRR (dB) 250 mA -80-80 200 mA 150 mA -100-100 100 mA 50 mA 20 mA -120-120

0.1 1 10 100 0.01 0.1 1 10 100 1000 10000
FREQUENCY (kHz)D004FREQUENCY (kHz)D005

**Figure 5-19. PSRR Loads Averaged 100Hz to 100kHz Figure 5-20. PSRR Loads Averaged 10Hz to 10MHz**

*Submit Document Feedback* Copyright © 2025 Texas Instruments Incorporated

**LP5907** <u>www.ti.com SNVS798Q – APRIL 2012 – REVISED JULY 2025</u>

#### 6 Detailed Description

##### 6.1 Overview

Designed to meet the needs of sensitive RF and analog circuits, the LP5907 provides low noise, high PSRR, low quiescent current, and low line and load transient response figures. Using innovative design techniques, the LP5907 offers class leading noise performance without the need for a separate noise filter capacitor.

The LP5907 is designed to perform with a single 1µF input capacitor and a single 1µF ceramic output capacitor. With a reasonable PCB layout, the single 1µF ceramic output capacitor can be placed up to 10cm away from the LP5907 device.

##### 6.2 Functional Block Diagram

IN OUT

EN POR

EN

+ RF CF +

VBG RAD

1.20V
EN EN+EN

1 M VIH GND

##### 6.3 Feature Description 6.3.1 Enable (EN)

The LP5907 EN pin is internally held low by a 1MΩ resistor to GND. The EN pin voltage must be higher than the VIHthreshold to make sure that the device is fully enabled under all operating conditions. The EN pin voltage must be lower than the VIL threshold to make sure that the device is fully disabled and the automatic output discharge is activated.

##### 6.3.2 Low Output Noise

Any internal noise at the LP5907 reference voltage is reduced by a first-order, low-pass RC filter before being passed to the output buffer stage. The low-pass RC filter has a –3-dB cut-off frequency of approximately 0.1Hz.

##### 6.3.3 Output Automatic Discharge

The LP5907 output employs an internal 230Ω (typical) pulldown resistance to discharge the output when the EN pin is low and the device is disabled.

Copyright © 2025 Texas Instruments Incorporated *Submit Document Feedback*

**LP5907** <u>SNVS798Q – APRIL 2012 – REVISED JULY 2025 www.ti.com</u>

##### 6.3.4 Remote Output Capacitor Placement

The LP5907 requires at least a 1µF capacitor at the OUT pin, but there are no strict requirements about the location of the capacitor in regards the OUT pin. In practical designs, the output capacitor can be located up to 10cm away from the LDO.

##### 6.3.5 Thermal Overload Protection (TSD)

Thermal shutdown disables the output when the junction temperature rises to approximately 160°C, which allows the device to cool. When the junction temperature cools to approximately 145°C, the output circuitry enables. Based on power dissipation, thermal resistance, and ambient temperature, the thermal protection circuit can cycle on and off. This thermal cycling limits the dissipation of the regulator, and protects the regulator from damage as a result of overheating.

The thermal shutdown circuitry of the LP5907 is designed to protect against temporary thermal overload conditions. The TSD circuitry is not intended to replace proper heat-sinking. Continuously running the LP5907 into thermal shutdown can degrade device reliability.

##### 6.4 Device Functional Modes 6.4.1 Enable (EN)

The LP5907 enable (EN) pin is internally held low by a 1MΩ resistor to GND. The EN pin voltage must be higher than the VIH threshold to make sure that the device is fully enabled under all operating conditions.

When the EN pin is pulled low, and the output is disabled, the output automatic discharge circuitry is activated. Any charge on the OUT pin is discharged to GND through the internal 230Ω (typical) pulldown resistance.

##### 6.4.2 Minimum Operating Input Voltage (VIN)

The LP5907 does not include any dedicated UVLO circuitry. The LP5907 internal circuitry is not fully functional until VIN is at least 2.2V. The output voltage is not regulated until VIN has reached at least the greater of 2.2V or (VOUT + VDO).

*Submit Document Feedback* Copyright © 2025 Texas Instruments Incorporated

**LP5907** <u>www.ti.com</u> SNVS798Q – APRIL 2012 – REVISED JULY 2025

|7 Application and Implementation|||
|---|---|---|
|Note Information in the following applications sections is not part of the TI component specification, and TI does not warrant its accuracy or completeness. TI’s customers are responsible for determining suitability of components for their purposes, as well as validating and testing their design implementation to confirm system functionality.|||
|7.1 Application Information The LP5907 is designed to meet the requirements of RF and analog circuits, by providing low noise, high PSRR, low quiescent current, and low line or load transient response figures. The device offers excellent noise performance without the need for a noise bypass capacitor and is stable with input and output capacitors with a value of 1µF. The LP5907 delivers this performance in industry standard packages such as DSBGA, X2SON, and SOT-23 which, for this device, are specified with an operating junction temperature (T 7.2 Typical Application Figure 7-1 shows the typical application circuit for the LP5907. Input and output capacitances can be increased, if needed, above the 1µF minimum for some applications. INPUT IN 1 F ENABLE EN GND GND Figure 7-1. LP5907 Typical Application 7.2.1 Design Requirements Table 7-1 summarizes the design requirements for Figure 7-1. Table 7-1. Design Parameters|) of –40°C to 125°C. J OUT OUTPUT 1 F LP5907||
|DESIGN PARAMETER|EXAMPLE VALUE||
|Input voltage range|2.2V to 5.5V||
|Output voltage|1.8V||
|Output current|200mA||
|Output capacitor range|0.7µF to 10µF||
|Input/output capacitor ESR range|5mΩ to 500mΩ||

Copyright © 2025 Texas Instruments Incorporated *Submit Document Feedback*

**LP5907** <u>SNVS798Q – APRIL 2012 – REVISED JULY 2025 www.ti.com</u>

##### 7.2.2 Detailed Design Procedure

**7.2.2.1 Custom Design With WEBENCH® Tools** Click here to create a custom design using the LP5907 device with the WEBENCH® Power Designer.
1. Start by entering the input voltage (VIN), output voltage (VOUT), and output current (IOUT) requirements.
2. Optimize the design for key parameters such as efficiency, footprint, and cost using the optimizer dial.
3. Compare the generated design with other possible solutions from Texas Instruments. The WEBENCH Power Designer provides a customized schematic along with a list of materials with real-time pricing and component availability. In most cases, these actions are available:
- Run electrical simulations to see important waveforms and circuit performance
- Run thermal simulations to understand board thermal performance
- Export customized schematic and layout into popular CAD formats
- Print PDF reports for the design, and share the design with colleagues Get more information about WEBENCH tools at www.ti.com/WEBENCH.
**7.2.2.2 Power Dissipation and Device Operation** The permissible power dissipation for any package is a measure of the capability of the device to pass heat from the power source, the junctions of the device, to the ultimate heat sink, the ambient environment. Thus, the power dissipation is dependent on the ambient temperature and the thermal resistance across the various interfaces between the die junction and ambient air. The maximum allowable power dissipation for the device in a given package can be calculated using Equation 1: PD-MAX = ((TJ-MAX – TA) / RθJA) (1) The actual power being dissipated in the device can be represented by Equation 2: PD = (VIN – VOUT) × IOUT(2) These two equations establish the relationship between the maximum power dissipation allowed in regards to thermal consideration, the voltage drop across the device, and the continuous current capability of the device. Use these two equations to determine the optimum operating conditions for the device in the application. In applications where lower power dissipation (PD) or excellent package thermal resistance (RθJA) is present, the maximum ambient temperature (TA-MAX) can be increased. In applications where high power dissipation or poor package thermal resistance is present, the maximum ambient temperature (TA-MAX) can be derated. TA-MAX is dependent on the maximum operating junction temperature (TJ-MAX-OP = 125°C), the maximum allowable power dissipation in the device package in the application (PD-MAX), and the junction-to ambient thermal resistance of the device or package in the application (RθJA), as given by Equation 3:
(3)

|TA-MAX|= (TJ-MAX-OP|– (RθJA× P|D-MAX))|||
|---|---|---|---|---|---|
|7.2.2.3 External Capacitors|A-MAX IN|IN OUT||D|OUT|

Alternately, if T cannot be derated, the P value must be reduced. This reduction can be accomplished by reducing V in the *V –V* term as long as the minimum VIN is met, or by reducing the I term, or by some combination of the two.

Like most low-dropout regulators, the LP5907 requires external capacitors for regulator stability. The device is specifically designed for portable applications requiring minimum board space and smallest components. These capacitors must be correctly selected for good performance.

*Submit Document Feedback* Copyright © 2025 Texas Instruments Incorporated

**LP5907** <u>www.ti.com</u> SNVS798Q – APRIL 2012 – REVISED JULY 2025

**7.2.2.4 Input Capacitor** An input capacitor is required for stability. The input capacitor must be at least equal to, or greater than, the output capacitor for good load transient performance. Connect at least a 1µF capacitor between the LP5907 input pin and ground for stable operation over the full load current range. Basically, having more output capacitance than input is acceptable, as long as the input is at least 1µF. The input capacitor must be located a distance of not more than 1cm from the input pin and returned to a clean analog ground. Any good quality ceramic, tantalum, or film capacitor can be used at the input.
##### Note

To provide stable operation, good PCB practices must be used to minimize ground impedance and to keep input inductance low. If these conditions cannot be met, or if long leads are used to connect the battery or other power source to the LP5907, increase the input capacitor to at least 10µF. Also, tantalum capacitors can suffer catastrophic failures resulting from surge current when connected to a low-impedance source of power (such as a battery or a very large capacitor). If a tantalum capacitor is used at the input, verify by the manufacturer that the capacitor has a surge current rating sufficient for the application. The initial tolerance, applied voltage derating, and temperature coefficient must all be considered when selecting the input capacitor to make sure that the actual capacitance is never less than 0.7µF over the entire operating range.

**7.2.2.5 Output Capacitor** The LP5907 is designed specifically to work with a very small ceramic output capacitor, typically 1µF. A ceramic capacitor (dielectric types X5R or X7R) in the 1µF to 10µF range, and with ESR between 5mΩ to 500mΩ, is suitable in the LP5907 application circuit. For this device, connect the output capacitor between the OUT pin with a good connection back to the GND pin. Tantalum or film capacitors can also be used at the device output, VOUT, but these are not as attractive for reasons of size and cost (see the *Capacitor Characteristics* section). The output capacitor must meet the requirement for the minimum value of capacitance and have an ESR value that is within the range of 5mΩ to 500mΩ for stability. Like the input capacitor, the initial tolerance, applied voltage derating, and temperature coefficient must all be considered when selecting the input capacitor to make sure that the actual capacitance is never less than 0.7µF over the entire operating range.
**7.2.2.6 Capacitor Characteristics** The LP5907 is designed to work with ceramic capacitors on the input and output to take advantage of the benefits these components offer. For capacitance values in the range of 1µF to 10µF, ceramic capacitors are the smallest, least expensive and have the lowest ESR values, thus making them best for eliminating high-frequency noise. The ESR of a typical 1µF ceramic capacitor is in the range of 20mΩ to 40mΩ, which easily meets the ESR requirement for stability for the LP5907. A better choice for temperature coefficient in a ceramic capacitor is X7R. This type of capacitor is the most stable and holds the capacitance within ±15% over the temperature range. Tantalum capacitors are less desirable than ceramic for use as output capacitors because they are more expensive when comparing equivalent capacitance and voltage ratings in the 1µF to 10µF range. Another important consideration is that tantalum capacitors have higher ESR values than equivalent size ceramics. Which means that although a tantalum capacitor can possibly be found with an ESR value within the stable range, the capacitor must be larger in capacitance (which means bigger and more costly) than a ceramic capacitor with the same ESR value. The ESR of a typical tantalum increases by approximately 2:1 when the temperature goes from 25°C down to –40°C, so some guard band must be allowed.
Copyright © 2025 Texas Instruments Incorporated *Submit Document Feedback*

**LP5907** <u>SNVS798Q – APRIL 2012 – REVISED JULY 2025 www.ti.com</u>

**7.2.2.7 Remote Capacitor Operation** The LP5907 requires at least a 1µF capacitor at the OUT pin, but there are no strict requirements about the location of the capacitor in regards to the pin. In practical designs the output capacitor can be located up to 10cm away from the LDO. Which means that there is no need to have a special capacitor close to the output pin if there is already respective capacitors in the system (such as a capacitor at the input of supplied device). The remote capacitor feature helps minimize the number of capacitors in the system. In general, keep the wiring parasitic inductance at a minimum, which means use traces as wide as possible from the LDO output to the capacitors, thus keeping the LDO output trace layer as close to ground layer as possible and avoiding vias on the path. If vias must be used, use as many vias as possible between the connection layers. Keep parasitic wiring inductance less than 35nH. For applications with fast load transients, use an input capacitor equal to or larger to the sum of the capacitance at the output node for best load transient performance.
**7.2.2.8 No-Load Stability** The LP5907 remains stable, and in regulation, with no external load.
**7.2.2.9 Enable Control** The LP5907 can be switched on or off by a logic input at the EN pin. A voltage on this pin greater than VIH turns the device on, and a voltage less than VIL turns the device off. When the EN pin is low, the regulator output is off and the device typically consumes less than 1μA. Additionally, an output pulldown circuit is activated that makes sure any charge stored on COUT is discharged to ground. If the application does not require the shutdown feature, the EN pin can be tied directly to the IN pin to keep the regulator output permanently on. An internal 1MΩ pulldown resistor ties the EN input to ground, making sure the device remains off if the EN pin is left open circuit. To provide proper operation, the signal source used to drive the EN pin must be able to swing above and below the specified turn-on or turn-off voltage thresholds listed in the *Electrical Characteristics* under VIL and VIH.
##### 7.2.3 Application Curves

1V/DIV V OUT 100 mV/DIV

V OUT

1V/DIV LOAD 200 mA/DIV EN

20 s/DIV 100 s/DIV SVA-30180515 SVA-30180514

**Figure 7-2. Start-Up Figure 7-3. Load Transient Response**

##### 7.3 Power Supply Recommendations

This device is designed to operate from an input supply voltage range of 2.2V to 5.5V. The input supply must be well regulated and free of spurious noise. To make sure that the LP5907 output voltage is well regulated and dynamic performance is optimum, the input supply must be at least VOUT + 1V. A minimum capacitor value of 1µF is required to be within 1cm of the IN pin.

*Submit Document Feedback* Copyright © 2025 Texas Instruments Incorporated

**LP5907** <u>www.ti.com SNVS798Q – APRIL 2012 – REVISED JULY 2025</u>

##### 7.4 Layout 7.4.1 Layout Guidelines

The dynamic performance of the LP5907 is dependent on the layout of the PCB. PCB layout practices that are adequate for typical LDOs can degrade the PSRR, noise, or transient performance of the LP5907.

Best performance is achieved by placing CIN and COUT on the same side of the PCB as the LP5907, and as close to the package as practical. The ground connections for CIN and COUT must route back to the LP5907 ground pin using as wide and short of a copper trace as practical.

Connections using long trace lengths, narrow trace widths, and connections through vias must be avoided. These connections add parasitic inductances and resistance that results in inferior performance, especially during transient conditions.

**7.4.1.1 X2SON Mounting** The X2SON package thermal pad must be soldered to the printed circuit board for proper thermal and mechanical performance. For more information, see the *QFN/SON PCB Attachment* application note.
**7.4.1.2 DSBGA Mounting**
VOUT The DSBGA package requires specific mounting techniques, which are detailed in *AN-1112 DSBGA Wafer Level* *Chip Scale Package* application note. For best results during assembly, alignment ordinals on the PC board can be used to facilitate placement of the DSBGA device. VIN GND

**7.4.1.3 DSBGA Light Sensitivity**
5 Exposing the DSBGA device to direct light can cause incorrect operation of the device. Light sources such as halogen lamps can affect electrical performance if these sources are situated in proximity to the device.GNDEnable Light with wavelengths in the red and infrared part of the spectrum have the most detrimental effect; thus, the fluorescent lighting used inside most buildings has very little effect on performance.

##### 7.4.2 Layout Examples

CINOUT 1 C4 OUT

INGND

EN N/C

**Figure 7-4. SOT-23 Typical Layout**

Copyright © 2025 Texas Instruments Incorporated *Submit Document Feedback*

**LP5907** <u>SNVS798Q – APRIL 2012 – REVISED JULY 2025 www.ti.com</u>

VOUTVINLP5907SN

|1|4|
|---|---|
||OUT|
|2|3|

##### C CIN

Power Ground VEN

**Figure 7-5. X2SON Typical Layout**

VIN VOUT LP5907UV

A1 A2 CINCOUT B1 B2

Power Ground VEN

**Figure 7-6. DSBGA Typical Layout**

*Submit Document Feedback* Copyright © 2025 Texas Instruments Incorporated

**LP5907** <u>www.ti.com SNVS798Q – APRIL 2012 – REVISED JULY 2025</u>

#### 8 Device and Documentation Support

##### 8.1 Documentation Support 8.1.1 Custom Design With WEBENCH® Tools

Click here to create a custom design using the LP5907 device with the WEBENCH® Power Designer.

1. Start by entering the input voltage (VIN), output voltage (VOUT), and output current (IOUT) requirements.
2. Optimize the design for key parameters such as efficiency, footprint, and cost using the optimizer dial.
3. Compare the generated design with other possible solutions from Texas Instruments. The WEBENCH Power Designer provides a customized schematic along with a list of materials with real-time pricing and component availability. In most cases, these actions are available:
- Run electrical simulations to see important waveforms and circuit performance
- Run thermal simulations to understand board thermal performance
- Export customized schematic and layout into popular CAD formats
- Print PDF reports for the design, and share the design with colleagues Get more information about WEBENCH tools at www.ti.com/WEBENCH.
##### 8.1.2 Related Documentation

##### For related documentation, see the following:

- Texas Instruments, *AN-1112 DSBGA Wafer Level Chip Scale Package* application note
- Texas Instruments, *QFN/SON PCB Attachment* application note
##### 8.2 Receiving Notification of Documentation Updates

To receive notification of documentation updates, navigate to the device product folder on ti.com. Click on *Notifications* to register and receive a weekly digest of any product information that has changed. For change details, review the revision history included in any revised document.

##### 8.3 Support Resources

TI E2E™ support forums are an engineer's go-to source for fast, verified answers and design help — straight from the experts. Search existing answers or ask your own question to get the quick design help you need.

Linked content is provided "AS IS" by the respective contributors. They do not constitute TI specifications and do not necessarily reflect TI's views; see TI's Terms of Use.

##### 8.4 Trademarks

TI E2E™ is a trademark of Texas Instruments. WEBENCH® is a registered trademark of Texas Instruments. All trademarks are the property of their respective owners.

##### 8.5 Electrostatic Discharge Caution

This integrated circuit can be damaged by ESD. Texas Instruments recommends that all integrated circuits be handled with appropriate precautions. Failure to observe proper handling and installation procedures can cause damage. ESD damage can range from subtle performance degradation to complete device failure. Precision integrated circuits may be more susceptible to damage because very small parametric changes could cause the device not to meet its published specifications.

##### 8.6 Glossary

TI Glossary This glossary lists and explains terms, acronyms, and definitions.

Copyright © 2025 Texas Instruments Incorporated *Submit Document Feedback*

**LP5907** SNVS798Q – APRIL 2012 – REVISED JULY 2025 <u>www.ti.com</u>

||9 Revision History NOTE: Page numbers for previous revisions may differ from page numbers in the current version. Changes from Revision P (January 2024) to Revision Q (July 2025) Page|
|---|---|
|•|Changed 0.5µF to 0.7µF in footnote 1 of Output and Input Capacitors table.....................................................6 Changes from Revision O (June 2020) to Revision P (January 2024) Page|
|• • •|Updated the numbering format for tables, figures, and cross-references throughout the document................. 1 Added YCR to pinout caption of Pin Configuration and Functions section.........................................................3 Added YCR column to Thermal Information table.............................................................................................. 5 10 Mechanical, Packaging, and Orderable Information The following pages include mechanical, packaging, and orderable information. This information is the most current data available for the designated devices. This data is subject to change without notice and revision of this document. For browser-based versions of this data sheet, refer to the left-hand navigation.|

*Submit Document Feedback* Copyright © 2025 Texas Instruments Incorporated

### PACKAGE OPTION ADDENDUM

www.ti.com 7-Nov-2025

##### PACKAGING INFORMATION

**Orderable part number**

|Status (1)|Material type (2)|Package | Pins|Package qty | Carrier|RoHS (3)|Lead finish/ Ball material (4)|MSL rating/ Peak reflow (5)|Op temp (°C)|Part marking (6)|
|---|---|---|---|---|---|---|---|---|
|Active|Production|DSBGA (YKM) | 4|3000 | LARGE T&R|Yes|SNAGCU|Level-1-260C-UNLIM|-40 to 125|Q|
|Active|Production|DSBGA (YKM) | 4|3000 | LARGE T&R|Yes|SNAGCU|Level-1-260C-UNLIM|-40 to 125|Q|
|Active|Production|DSBGA (YKM) | 4|3000 | LARGE T&R|Yes|SNAGCU|Level-1-260C-UNLIM|-40 to 125|N|
|Active|Production|DSBGA (YKM) | 4|3000 | LARGE T&R|Yes|SNAGCU|Level-1-260C-UNLIM|-40 to 125|N|
|Active|Production|SOT-23 (DBV) | 5|3000 | LARGE T&R|Yes|NIPDAU | SN|Level-1-260C-UNLIM|-40 to 125|LLTB|
|Active|Production|SOT-23 (DBV) | 5|3000 | LARGE T&R|Yes|NIPDAU|Level-1-260C-UNLIM|-40 to 125|LLTB|
|Active|Production|SOT-23 (DBV) | 5|3000 | LARGE T&R|Yes|NIPDAU|Level-1-260C-UNLIM|-40 to 125|LLTB|
|Active|Production|SOT-23 (DBV) | 5|3000 | LARGE T&R|Yes|NIPDAU | SN|Level-1-260C-UNLIM|-40 to 125|LN8B|
|Active|Production|SOT-23 (DBV) | 5|3000 | LARGE T&R|Yes|NIPDAU|Level-1-260C-UNLIM|-40 to 125|LN8B|
|Active|Production|SOT-23 (DBV) | 5|3000 | LARGE T&R|Yes|NIPDAU|Level-1-260C-UNLIM|-40 to 125|LN8B|
|Active|Production|SOT-23 (DBV) | 5|3000 | LARGE T&R|Yes|NIPDAU | SN|Level-1-260C-UNLIM|-40 to 125|LLUB|
|Active|Production|SOT-23 (DBV) | 5|3000 | LARGE T&R|Yes|NIPDAU|Level-1-260C-UNLIM|-40 to 125|LLUB|
|Active|Production|SOT-23 (DBV) | 5|3000 | LARGE T&R|Yes|NIPDAU|Level-1-260C-UNLIM|-40 to 125|LLUB|
|Active|Production|SOT-23 (DBV) | 5|3000 | LARGE T&R|Yes|NIPDAU | SN|Level-1-260C-UNLIM|-40 to 125|LN7B|
|Active|Production|SOT-23 (DBV) | 5|3000 | LARGE T&R|Yes|NIPDAU|Level-1-260C-UNLIM|-40 to 125|LN7B|
|Active|Production|SOT-23 (DBV) | 5|3000 | LARGE T&R|Yes|NIPDAU|Level-1-260C-UNLIM|-40 to 125|LN7B|
|Active|Production|SOT-23 (DBV) | 5|3000 | LARGE T&R|Yes|NIPDAU | SN|Level-1-260C-UNLIM|-40 to 125|LLYB|
|Active|Production|SOT-23 (DBV) | 5|3000 | LARGE T&R|Yes|NIPDAU|Level-1-260C-UNLIM|-40 to 125|LLYB|
|Active|Production|SOT-23 (DBV) | 5|3000 | LARGE T&R|Yes|NIPDAU|Level-1-260C-UNLIM|-40 to 125|LLYB|
|Active|Production|SOT-23 (DBV) | 5|3000 | LARGE T&R|Yes|NIPDAU|Level-1-260C-UNLIM|-40 to 125|LN4B|
|Active|Production|SOT-23 (DBV) | 5|3000 | LARGE T&R|Yes|NIPDAU | SN|Level-1-260C-UNLIM|-40 to 125|LN4B|
|Active|Production|SOT-23 (DBV) | 5|3000 | LARGE T&R|Yes|NIPDAU | SN|Level-1-260C-UNLIM|-40 to 125|1E5X|
|Active|Production|SOT-23 (DBV) | 5|3000 | LARGE T&R|Yes|NIPDAU|Level-1-260C-UNLIM|-40 to 125|1E5X|
|Active|Production|SOT-23 (DBV) | 5|3000 | LARGE T&R|Yes|NIPDAU|Level-1-260C-UNLIM|-40 to 125|1E5X|
|Active|Production|SOT-23 (DBV) | 5|3000 | LARGE T&R|Yes|NIPDAU | SN|Level-1-260C-UNLIM|-40 to 125|LLZB|
|Active|Production|SOT-23 (DBV) | 5|3000 | LARGE T&R|Yes|NIPDAU|Level-1-260C-UNLIM|-40 to 125|LLZB|
|Active|Production|SOT-23 (DBV) | 5|3000 | LARGE T&R|Yes|NIPDAU|Level-1-260C-UNLIM|-40 to 125|LLZB|
|Active|Production|SOT-23 (DBV) | 5|3000 | LARGE T&R|Yes|NIPDAU | SN|Level-1-260C-UNLIM|-40 to 125|LN5B|
|Active|Production|SOT-23 (DBV) | 5|3000 | LARGE T&R|Yes|NIPDAU|Level-1-260C-UNLIM|-40 to 125|LN5B|

LP5907A28YKMR LP5907A28YKMR.B LP5907A33YKMR LP5907A33YKMR.B LP5907MFX-1.2/NOPB LP5907MFX-1.2/NOPB.A LP5907MFX-1.2/NOPB.B LP5907MFX-1.5/NOPB LP5907MFX-1.5/NOPB.A LP5907MFX-1.5/NOPB.B LP5907MFX-1.8/NOPB LP5907MFX-1.8/NOPB.A LP5907MFX-1.8/NOPB.B LP5907MFX-2.5/NOPB LP5907MFX-2.5/NOPB.A LP5907MFX-2.5/NOPB.B LP5907MFX-2.8/NOPB LP5907MFX-2.8/NOPB.A LP5907MFX-2.8/NOPB.B LP5907MFX-2.85/NO.A LP5907MFX-2.85/NOPB LP5907MFX-2.9/NOPB LP5907MFX-2.9/NOPB.A LP5907MFX-2.9/NOPB.B LP5907MFX-3.0/NOPB LP5907MFX-3.0/NOPB.A LP5907MFX-3.0/NOPB.B LP5907MFX-3.1/NOPB LP5907MFX-3.1/NOPB.A

Addendum-Page

### PACKAGE OPTION ADDENDUM

www.ti.com 7-Nov-2025

**Orderable part number**

|Status (1)|Material type (2)|Package | Pins|Package qty | Carrier|RoHS (3)|Lead finish/ Ball material (4)|MSL rating/ Peak reflow|(5)|Op temp (°C)|Part marking (6)|
|---|---|---|---|---|---|---|---|---|---|
|Active|Production|SOT-23 (DBV) | 5|3000 | LARGE T&R|Yes|NIPDAU|Level-1-260C-UNLIM||-40 to 125|LN5B|
|Active|Production|SOT-23 (DBV) | 5|3000 | LARGE T&R|Yes|NIPDAU | SN|Level-1-260C-UNLIM||-40 to 125|LN6B|
|Active|Production|SOT-23 (DBV) | 5|3000 | LARGE T&R|Yes|NIPDAU|Level-1-260C-UNLIM||-40 to 125|LN6B|
|Active|Production|SOT-23 (DBV) | 5|3000 | LARGE T&R|Yes|NIPDAU|Level-1-260C-UNLIM||-40 to 125|LN6B|
|Active|Production|SOT-23 (DBV) | 5|3000 | LARGE T&R|Yes|NIPDAU | SN|Level-1-260C-UNLIM||-40 to 125|LLVB|
|Active|Production|SOT-23 (DBV) | 5|3000 | LARGE T&R|Yes|NIPDAU|Level-1-260C-UNLIM||-40 to 125|LLVB|
|Active|Production|SOT-23 (DBV) | 5|3000 | LARGE T&R|Yes|NIPDAU|Level-1-260C-UNLIM||-40 to 125|LLVB|
|Active|Production|SOT-23 (DBV) | 5|3000 | LARGE T&R|Yes|NIPDAU | SN|Level-1-260C-UNLIM||-40 to 125|LLXB|
|Active|Production|SOT-23 (DBV) | 5|3000 | LARGE T&R|Yes|NIPDAU|Level-1-260C-UNLIM||-40 to 125|LLXB|
|Active|Production|SOT-23 (DBV) | 5|3000 | LARGE T&R|Yes|NIPDAU|Level-1-260C-UNLIM||-40 to 125|LLXB|
|Active|Production|SOT-23 (DBV) | 5|3000 | LARGE T&R|-|Call TI||Call TI|-40 to 125||
|Active|Production|SOT-23 (DBV) | 5|3000 | LARGE T&R|-|Call TI||Call TI|-40 to 125||
|Active|Production|SOT-23 (DBV) | 5|3000 | LARGE T&R|-|Call TI||Call TI|-40 to 125||
|Active|Production|SOT-23 (DBV) | 5|3000 | LARGE T&R|-|Call TI||Call TI|-40 to 125||
|Active|Production|SOT-23 (DBV) | 5|3000 | LARGE T&R|-|Call TI||Call TI|-40 to 125||
|Active|Production|SOT-23 (DBV) | 5|3000 | LARGE T&R|-|Call TI||Call TI|-40 to 125||
|Active|Production|SOT-23 (DBV) | 5|3000 | LARGE T&R|-|Call TI||Call TI|-40 to 125||
|Active|Production|SOT-23 (DBV) | 5|3000 | LARGE T&R|-|Call TI||Call TI|-40 to 125||
|Active|Production|SOT-23 (DBV) | 5|3000 | LARGE T&R|-|Call TI||Call TI|-40 to 125||
|Active|Production|SOT-23 (DBV) | 5|3000 | LARGE T&R|-|Call TI||Call TI|-40 to 125||
|Active|Production|SOT-23 (DBV) | 5|3000 | LARGE T&R|-|Call TI||Call TI|-40 to 125||
|Active|Production|SOT-23 (DBV) | 5|3000 | LARGE T&R|-|Call TI||Call TI|-40 to 125||
|Active|Production|SOT-23 (DBV) | 5|3000 | LARGE T&R|-|Call TI||Call TI|-40 to 125||
|Active|Production|SOT-23 (DBV) | 5|3000 | LARGE T&R|-|Call TI||Call TI|-40 to 125||
|Active|Production|SOT-23 (DBV) | 5|3000 | LARGE T&R|-|Call TI||Call TI|-40 to 125||
|Active|Production|SOT-23 (DBV) | 5|3000 | LARGE T&R|-|Call TI||Call TI|-40 to 125||
|Active|Production|SOT-23 (DBV) | 5|3000 | LARGE T&R|-|Call TI||Call TI|-40 to 125||
|Active|Production|SOT-23 (DBV) | 5|3000 | LARGE T&R|-|Call TI||Call TI|-40 to 125||
|Active|Production|X2SON (DQN) | 4|3000 | LARGE T&R|Yes|NIPDAU|Level-1-260C-UNLIM||-40 to 125|CF|
|Active|Production|X2SON (DQN) | 4|3000 | LARGE T&R|Yes|NIPDAU|Level-1-260C-UNLIM||-40 to 125|CF|
|Active|Production|X2SON (DQN) | 4|3000 | LARGE T&R|Yes|NIPDAU|Level-1-260C-UNLIM||-40 to 125|CF|

LP5907MFX-3.1/NOPB.B LP5907MFX-3.2/NOPB LP5907MFX-3.2/NOPB.A LP5907MFX-3.2/NOPB.B LP5907MFX-3.3/NOPB LP5907MFX-3.3/NOPB.A LP5907MFX-3.3/NOPB.B LP5907MFX-4.5/NOPB LP5907MFX-4.5/NOPB.A LP5907MFX-4.5/NOPB.B LP5907MFX1.2NOPBG4.A LP5907MFX1.2NOPBG4.B LP5907MFX1.8NOPBG4.A LP5907MFX1.8NOPBG4.B LP5907MFX2.5NOPBG4.A LP5907MFX2.5NOPBG4.B LP5907MFX2.8NOPBG4.A LP5907MFX2.8NOPBG4.B LP5907MFX3.0NOPBG4.A LP5907MFX3.0NOPBG4.B LP5907MFX3.1NOPBG4.A LP5907MFX3.1NOPBG4.B LP5907MFX3.2NOPBG4.A LP5907MFX3.2NOPBG4.B LP5907MFX3.3NOPBG4.A LP5907MFX3.3NOPBG4.B LP5907MFX4.5NOPBG4.A LP5907MFX4.5NOPBG4.B LP5907SNX-1.2/NOPB LP5907SNX-1.2/NOPB.A LP5907SNX-1.2/NOPB.B

Addendum-Page

### PACKAGE OPTION ADDENDUM

www.ti.com 7-Nov-2025

**Orderable part number**

|Status (1)|Material type (2)|Package | Pins|Package qty | Carrier|RoHS (3)|Lead finish/ Ball material (4)|MSL rating/ Peak reflow (5)|Op temp (°C)|Part marking (6)|
|---|---|---|---|---|---|---|---|---|
|Active|Production|X2SON (DQN) | 4|3000 | LARGE T&R|Yes|NIPDAU|Level-1-260C-UNLIM|-40 to 125|CG|
|Active|Production|X2SON (DQN) | 4|3000 | LARGE T&R|Yes|NIPDAU|Level-1-260C-UNLIM|-40 to 125|CG|
|Active|Production|X2SON (DQN) | 4|3000 | LARGE T&R|Yes|NIPDAU|Level-1-260C-UNLIM|-40 to 125|CG|
|Active|Production|X2SON (DQN) | 4|3000 | LARGE T&R|Yes|NIPDAU|Level-1-260C-UNLIM|-40 to 125|3Z|
|Active|Production|X2SON (DQN) | 4|3000 | LARGE T&R|Yes|NIPDAU|Level-1-260C-UNLIM|-40 to 125|3Z|
|Active|Production|X2SON (DQN) | 4|3000 | LARGE T&R|Yes|NIPDAU|Level-1-260C-UNLIM|-40 to 125|3Z|
|Active|Production|X2SON (DQN) | 4|3000 | LARGE T&R|Yes|NIPDAU|Level-1-260C-UNLIM|-40 to 125|EP|
|Active|Production|X2SON (DQN) | 4|3000 | LARGE T&R|Yes|NIPDAU|Level-1-260C-UNLIM|-40 to 125|EP|
|Active|Production|X2SON (DQN) | 4|3000 | LARGE T&R|Yes|NIPDAU|Level-1-260C-UNLIM|-40 to 125|EP|
|Active|Production|X2SON (DQN) | 4|3000 | LARGE T&R|Yes|NIPDAU|Level-1-260C-UNLIM|-40 to 125|F9|
|Active|Production|X2SON (DQN) | 4|3000 | LARGE T&R|Yes|NIPDAU|Level-1-260C-UNLIM|-40 to 125|F9|
|Active|Production|X2SON (DQN) | 4|3000 | LARGE T&R|Yes|NIPDAU|Level-1-260C-UNLIM|-40 to 125|F9|
|Active|Production|X2SON (DQN) | 4|3000 | LARGE T&R|Yes|NIPDAU|Level-1-260C-UNLIM|-40 to 125|CH|
|Active|Production|X2SON (DQN) | 4|3000 | LARGE T&R|Yes|NIPDAU|Level-1-260C-UNLIM|-40 to 125|CH|
|Active|Production|X2SON (DQN) | 4|3000 | LARGE T&R|Yes|NIPDAU|Level-1-260C-UNLIM|-40 to 125|CH|
|Active|Production|X2SON (DQN) | 4|3000 | LARGE T&R|Yes|NIPDAU|Level-1-260C-UNLIM|-40 to 125|HI|
|Active|Production|X2SON (DQN) | 4|3000 | LARGE T&R|Yes|NIPDAU|Level-1-260C-UNLIM|-40 to 125|HI|
|Active|Production|X2SON (DQN) | 4|3000 | LARGE T&R|Yes|NIPDAU|Level-1-260C-UNLIM|-40 to 125|HI|
|Active|Production|X2SON (DQN) | 4|3000 | LARGE T&R|Yes|NIPDAU|Level-1-260C-UNLIM|-40 to 125|CI|
|Active|Production|X2SON (DQN) | 4|3000 | LARGE T&R|Yes|NIPDAU|Level-1-260C-UNLIM|-40 to 125|CI|
|Active|Production|X2SON (DQN) | 4|3000 | LARGE T&R|Yes|NIPDAU|Level-1-260C-UNLIM|-40 to 125|CI|
|Active|Production|X2SON (DQN) | 4|3000 | LARGE T&R|Yes|NIPDAU|Level-1-260C-UNLIM|-40 to 125|CJ|
|Active|Production|X2SON (DQN) | 4|3000 | LARGE T&R|Yes|NIPDAU|Level-1-260C-UNLIM|-40 to 125|CJ|
|Active|Production|X2SON (DQN) | 4|3000 | LARGE T&R|Yes|NIPDAU|Level-1-260C-UNLIM|-40 to 125|CJ|
|Active|Production|X2SON (DQN) | 4|3000 | LARGE T&R|Yes|NIPDAU|Level-1-260C-UNLIM|-40 to 125|CJ|
|Active|Production|X2SON (DQN) | 4|3000 | LARGE T&R|Yes|NIPDAU|Level-1-260C-UNLIM|-40 to 125|CJ|
|Active|Production|X2SON (DQN) | 4|3000 | LARGE T&R|Yes|NIPDAU|Level-1-260C-UNLIM|-40 to 125|GV|
|Active|Production|X2SON (DQN) | 4|3000 | LARGE T&R|Yes|NIPDAU|Level-1-260C-UNLIM|-40 to 125|GV|
|Active|Production|X2SON (DQN) | 4|3000 | LARGE T&R|Yes|NIPDAU|Level-1-260C-UNLIM|-40 to 125|GV|
|Active|Production|X2SON (DQN) | 4|3000 | LARGE T&R|Yes|NIPDAU|Level-1-260C-UNLIM|-40 to 125|CK|
|Active|Production|X2SON (DQN) | 4|3000 | LARGE T&R|Yes|NIPDAU|Level-1-260C-UNLIM|-40 to 125|CK|

LP5907SNX-1.8/NOPB LP5907SNX-1.8/NOPB.A LP5907SNX-1.8/NOPB.B LP5907SNX-1.9 LP5907SNX-1.9.A LP5907SNX-1.9.B LP5907SNX-2.2/NOPB LP5907SNX-2.2/NOPB.A LP5907SNX-2.2/NOPB.B LP5907SNX-2.5/NOPB LP5907SNX-2.5/NOPB.A LP5907SNX-2.5/NOPB.B LP5907SNX-2.7/NOPB LP5907SNX-2.7/NOPB.A LP5907SNX-2.7/NOPB.B LP5907SNX-2.75 LP5907SNX-2.75.A LP5907SNX-2.75.B LP5907SNX-2.8/NOPB LP5907SNX-2.8/NOPB.A LP5907SNX-2.8/NOPB.B LP5907SNX-2.85/G4 LP5907SNX-2.85/G4.A LP5907SNX-2.85/G4.B LP5907SNX-2.85/NO.A LP5907SNX-2.85/NOPB LP5907SNX-2.9/NOPB LP5907SNX-2.9/NOPB.A LP5907SNX-2.9/NOPB.B LP5907SNX-3.0/NOPB LP5907SNX-3.0/NOPB.A

Addendum-Page

### PACKAGE OPTION ADDENDUM

www.ti.com 7-Nov-2025

**Orderable part number**

|Status (1)|Material type (2)|Package | Pins|Package qty | Carrier|RoHS (3)|Lead finish/ Ball material (4)|MSL rating/ Peak reflow (5)|Op temp (°C)|Part marking (6)|
|---|---|---|---|---|---|---|---|---|
|Active|Production|X2SON (DQN) | 4|3000 | LARGE T&R|Yes|NIPDAU|Level-1-260C-UNLIM|-40 to 125|CK|
|Active|Production|X2SON (DQN) | 4|3000 | LARGE T&R|Yes|NIPDAU|Level-1-260C-UNLIM|-40 to 125|CL|
|Active|Production|X2SON (DQN) | 4|3000 | LARGE T&R|Yes|NIPDAU|Level-1-260C-UNLIM|-40 to 125|CL|
|Active|Production|X2SON (DQN) | 4|3000 | LARGE T&R|Yes|NIPDAU|Level-1-260C-UNLIM|-40 to 125|CL|
|Active|Production|X2SON (DQN) | 4|3000 | LARGE T&R|Yes|NIPDAU|Level-1-260C-UNLIM|-40 to 125|CM|
|Active|Production|X2SON (DQN) | 4|3000 | LARGE T&R|Yes|NIPDAU|Level-1-260C-UNLIM|-40 to 125|CM|
|Active|Production|X2SON (DQN) | 4|3000 | LARGE T&R|Yes|NIPDAU|Level-1-260C-UNLIM|-40 to 125|CM|
|Active|Production|X2SON (DQN) | 4|3000 | LARGE T&R|Yes|NIPDAU|Level-1-260C-UNLIM|-40 to 125|CN|
|Active|Production|X2SON (DQN) | 4|3000 | LARGE T&R|Yes|NIPDAU|Level-1-260C-UNLIM|-40 to 125|CN|
|Active|Production|X2SON (DQN) | 4|3000 | LARGE T&R|Yes|NIPDAU|Level-1-260C-UNLIM|-40 to 125|CN|
|Active|Production|X2SON (DQN) | 4|3000 | LARGE T&R|Yes|NIPDAU|Level-1-260C-UNLIM|-40 to 125|GU|
|Active|Production|X2SON (DQN) | 4|3000 | LARGE T&R|Yes|NIPDAU|Level-1-260C-UNLIM|-40 to 125|GU|
|Active|Production|X2SON (DQN) | 4|3000 | LARGE T&R|Yes|NIPDAU|Level-1-260C-UNLIM|-40 to 125|GU|
|Active|Production|X2SON (DQN) | 4|3000 | LARGE T&R|Yes|NIPDAU|Level-1-260C-UNLIM|-40 to 125|CO|
|Active|Production|X2SON (DQN) | 4|3000 | LARGE T&R|Yes|NIPDAU|Level-1-260C-UNLIM|-40 to 125|CO|
|Active|Production|X2SON (DQN) | 4|3000 | LARGE T&R|Yes|NIPDAU|Level-1-260C-UNLIM|-40 to 125|CO|
|Active|Production|X2SON (DQN) | 4|3000 | LARGE T&R|Yes|NIPDAU|Level-1-260C-UNLIM|-40 to 125|CF|
|Active|Production|X2SON (DQN) | 4|3000 | LARGE T&R|Yes|NIPDAU|Level-1-260C-UNLIM|-40 to 125|CF|
|Active|Production|X2SON (DQN) | 4|3000 | LARGE T&R|Yes|NIPDAU|Level-1-260C-UNLIM|-40 to 125|CF|
|Active|Production|X2SON (DQN) | 4|3000 | LARGE T&R|Yes|NIPDAU|Level-1-260C-UNLIM|-40 to 125|CG|
|Active|Production|X2SON (DQN) | 4|3000 | LARGE T&R|Yes|NIPDAU|Level-1-260C-UNLIM|-40 to 125|CG|
|Active|Production|X2SON (DQN) | 4|3000 | LARGE T&R|Yes|NIPDAU|Level-1-260C-UNLIM|-40 to 125|CG|
|Active|Production|X2SON (DQN) | 4|3000 | LARGE T&R|Yes|NIPDAU|Level-1-260C-UNLIM|-40 to 125|EP|
|Active|Production|X2SON (DQN) | 4|3000 | LARGE T&R|Yes|NIPDAU|Level-1-260C-UNLIM|-40 to 125|EP|
|Active|Production|X2SON (DQN) | 4|3000 | LARGE T&R|Yes|NIPDAU|Level-1-260C-UNLIM|-40 to 125|EP|
|Active|Production|X2SON (DQN) | 4|3000 | LARGE T&R|Yes|NIPDAU|Level-1-260C-UNLIM|-40 to 125|F9|
|Active|Production|X2SON (DQN) | 4|3000 | LARGE T&R|Yes|NIPDAU|Level-1-260C-UNLIM|-40 to 125|F9|
|Active|Production|X2SON (DQN) | 4|3000 | LARGE T&R|Yes|NIPDAU|Level-1-260C-UNLIM|-40 to 125|F9|
|Active|Production|X2SON (DQN) | 4|3000 | LARGE T&R|Yes|NIPDAU|Level-1-260C-UNLIM|-40 to 125|CH|
|Active|Production|X2SON (DQN) | 4|3000 | LARGE T&R|Yes|NIPDAU|Level-1-260C-UNLIM|-40 to 125|CH|
|Active|Production|X2SON (DQN) | 4|3000 | LARGE T&R|Yes|NIPDAU|Level-1-260C-UNLIM|-40 to 125|CH|

LP5907SNX-3.0/NOPB.B LP5907SNX-3.1/NOPB LP5907SNX-3.1/NOPB.A LP5907SNX-3.1/NOPB.B LP5907SNX-3.2/NOPB LP5907SNX-3.2/NOPB.A LP5907SNX-3.2/NOPB.B LP5907SNX-3.3/NOPB LP5907SNX-3.3/NOPB.A LP5907SNX-3.3/NOPB.B LP5907SNX-4.0/NOPB LP5907SNX-4.0/NOPB.A LP5907SNX-4.0/NOPB.B LP5907SNX-4.5/NOPB LP5907SNX-4.5/NOPB.A LP5907SNX-4.5/NOPB.B LP5907SNX1.2NOPBG4 LP5907SNX1.2NOPBG4.A LP5907SNX1.2NOPBG4.B LP5907SNX1.8NOPBG4 LP5907SNX1.8NOPBG4.A LP5907SNX1.8NOPBG4.B LP5907SNX2.2NOPBG4 LP5907SNX2.2NOPBG4.A LP5907SNX2.2NOPBG4.B LP5907SNX2.5NOPBG4 LP5907SNX2.5NOPBG4.A LP5907SNX2.5NOPBG4.B LP5907SNX2.7NOPBG4 LP5907SNX2.7NOPBG4.A LP5907SNX2.7NOPBG4.B

Addendum-Page

### PACKAGE OPTION ADDENDUM

www.ti.com 7-Nov-2025

**Orderable part number**

|Status (1)|Material type (2)|Package | Pins|Package qty | Carrier|RoHS (3)|Lead finish/ Ball material (4)|MSL rating/ Peak reflow (5)|Op temp (°C)|Part marking (6)|
|---|---|---|---|---|---|---|---|---|
|Active|Production|X2SON (DQN) | 4|3000 | LARGE T&R|Yes|NIPDAU|Level-1-260C-UNLIM|-40 to 125|CI|
|Active|Production|X2SON (DQN) | 4|3000 | LARGE T&R|Yes|NIPDAU|Level-1-260C-UNLIM|-40 to 125|CI|
|Active|Production|X2SON (DQN) | 4|3000 | LARGE T&R|Yes|NIPDAU|Level-1-260C-UNLIM|-40 to 125|CI|
|Active|Production|X2SON (DQN) | 4|3000 | LARGE T&R|Yes|NIPDAU|Level-1-260C-UNLIM|-40 to 125|GV|
|Active|Production|X2SON (DQN) | 4|3000 | LARGE T&R|Yes|NIPDAU|Level-1-260C-UNLIM|-40 to 125|GV|
|Active|Production|X2SON (DQN) | 4|3000 | LARGE T&R|Yes|NIPDAU|Level-1-260C-UNLIM|-40 to 125|GV|
|Active|Production|X2SON (DQN) | 4|3000 | LARGE T&R|Yes|NIPDAU|Level-1-260C-UNLIM|-40 to 125|CK|
|Active|Production|X2SON (DQN) | 4|3000 | LARGE T&R|Yes|NIPDAU|Level-1-260C-UNLIM|-40 to 125|CK|
|Active|Production|X2SON (DQN) | 4|3000 | LARGE T&R|Yes|NIPDAU|Level-1-260C-UNLIM|-40 to 125|CK|
|Active|Production|X2SON (DQN) | 4|3000 | LARGE T&R|Yes|NIPDAU|Level-1-260C-UNLIM|-40 to 125|CL|
|Active|Production|X2SON (DQN) | 4|3000 | LARGE T&R|Yes|NIPDAU|Level-1-260C-UNLIM|-40 to 125|CL|
|Active|Production|X2SON (DQN) | 4|3000 | LARGE T&R|Yes|NIPDAU|Level-1-260C-UNLIM|-40 to 125|CL|
|Active|Production|X2SON (DQN) | 4|3000 | LARGE T&R|Yes|NIPDAU|Level-1-260C-UNLIM|-40 to 125|CM|
|Active|Production|X2SON (DQN) | 4|3000 | LARGE T&R|Yes|NIPDAU|Level-1-260C-UNLIM|-40 to 125|CM|
|Active|Production|X2SON (DQN) | 4|3000 | LARGE T&R|Yes|NIPDAU|Level-1-260C-UNLIM|-40 to 125|CM|
|Active|Production|X2SON (DQN) | 4|3000 | LARGE T&R|Yes|NIPDAU|Level-1-260C-UNLIM|-40 to 125|CN|
|Active|Production|X2SON (DQN) | 4|3000 | LARGE T&R|Yes|NIPDAU|Level-1-260C-UNLIM|-40 to 125|CN|
|Active|Production|X2SON (DQN) | 4|3000 | LARGE T&R|Yes|NIPDAU|Level-1-260C-UNLIM|-40 to 125|CN|
|Active|Production|X2SON (DQN) | 4|3000 | LARGE T&R|Yes|NIPDAU|Level-1-260C-UNLIM|-40 to 125|GU|
|Active|Production|X2SON (DQN) | 4|3000 | LARGE T&R|Yes|NIPDAU|Level-1-260C-UNLIM|-40 to 125|GU|
|Active|Production|X2SON (DQN) | 4|3000 | LARGE T&R|Yes|NIPDAU|Level-1-260C-UNLIM|-40 to 125|GU|
|Active|Production|X2SON (DQN) | 4|3000 | LARGE T&R|Yes|NIPDAU|Level-1-260C-UNLIM|-40 to 125|CO|
|Active|Production|X2SON (DQN) | 4|3000 | LARGE T&R|Yes|NIPDAU|Level-1-260C-UNLIM|-40 to 125|CO|
|Active|Production|X2SON (DQN) | 4|3000 | LARGE T&R|Yes|NIPDAU|Level-1-260C-UNLIM|-40 to 125|CO|
|Active|Production|DSBGA (YKE) | 4|250 | SMALL T&R|Yes|SNAGCU|Level-1-260C-UNLIM|-40 to 125|R|
|Active|Production|DSBGA (YKE) | 4|250 | SMALL T&R|Yes|SNAGCU|Level-1-260C-UNLIM|-40 to 125|R|
|Active|Production|DSBGA (YKE) | 4|250 | SMALL T&R|Yes|SNAGCU|Level-1-260C-UNLIM|-40 to 125|R|
|Active|Production|DSBGA (YKE) | 4|250 | SMALL T&R|Yes|SNAGCU|Level-1-260C-UNLIM|-40 to 125|S|
|Active|Production|DSBGA (YKE) | 4|250 | SMALL T&R|Yes|SNAGCU|Level-1-260C-UNLIM|-40 to 125|S|
|Active|Production|DSBGA (YKE) | 4|250 | SMALL T&R|Yes|SNAGCU|Level-1-260C-UNLIM|-40 to 125|S|
|Active|Production|DSBGA (YKE) | 4|250 | SMALL T&R|Yes|SNAGCU|Level-1-260C-UNLIM|-40 to 125|U|

LP5907SNX2.8NOPBG4 LP5907SNX2.8NOPBG4.A LP5907SNX2.8NOPBG4.B LP5907SNX2.9NOPBG4 LP5907SNX2.9NOPBG4.A LP5907SNX2.9NOPBG4.B LP5907SNX3.0NOPBG4 LP5907SNX3.0NOPBG4.A LP5907SNX3.0NOPBG4.B LP5907SNX3.1NOPBG4 LP5907SNX3.1NOPBG4.A LP5907SNX3.1NOPBG4.B LP5907SNX3.2NOPBG4 LP5907SNX3.2NOPBG4.A LP5907SNX3.2NOPBG4.B LP5907SNX3.3NOPBG4 LP5907SNX3.3NOPBG4.A LP5907SNX3.3NOPBG4.B LP5907SNX4.0NOPBG4 LP5907SNX4.0NOPBG4.A LP5907SNX4.0NOPBG4.B LP5907SNX4.5NOPBG4 LP5907SNX4.5NOPBG4.A LP5907SNX4.5NOPBG4.B LP5907UVE-1.2/NOPB LP5907UVE-1.2/NOPB.A LP5907UVE-1.2/NOPB.B LP5907UVE-1.8/NOPB LP5907UVE-1.8/NOPB.A LP5907UVE-1.8/NOPB.B LP5907UVE-2.8/NOPB

Addendum-Page

### PACKAGE OPTION ADDENDUM

www.ti.com 7-Nov-2025

**Orderable part number**

|Status (1)|Material type (2)|Package | Pins|Package qty | Carrier|RoHS (3)|Lead finish/ Ball material (4)|MSL rating/ Peak reflow (5)|Op temp (°C)|Part marking (6)|
|---|---|---|---|---|---|---|---|---|
|Active|Production|DSBGA (YKE) | 4|250 | SMALL T&R|Yes|SNAGCU|Level-1-260C-UNLIM|-40 to 125|U|
|Active|Production|DSBGA (YKE) | 4|250 | SMALL T&R|Yes|SNAGCU|Level-1-260C-UNLIM|-40 to 125|U|
|Active|Production|DSBGA (YKE) | 4|250 | SMALL T&R|Yes|SNAGCU|Level-1-260C-UNLIM|-40 to 125|V|
|Active|Production|DSBGA (YKE) | 4|250 | SMALL T&R|Yes|SNAGCU|Level-1-260C-UNLIM|-40 to 125|V|
|Active|Production|DSBGA (YKE) | 4|250 | SMALL T&R|Yes|SNAGCU|Level-1-260C-UNLIM|-40 to 125|B|
|Active|Production|DSBGA (YKE) | 4|250 | SMALL T&R|Yes|SNAGCU|Level-1-260C-UNLIM|-40 to 125|B|
|Active|Production|DSBGA (YKE) | 4|250 | SMALL T&R|Yes|SNAGCU|Level-1-260C-UNLIM|-40 to 125|B|
|Active|Production|DSBGA (YKE) | 4|250 | SMALL T&R|Yes|SNAGCU|Level-1-260C-UNLIM|-40 to 125|X|
|Active|Production|DSBGA (YKE) | 4|250 | SMALL T&R|Yes|SNAGCU|Level-1-260C-UNLIM|-40 to 125|X|
|Active|Production|DSBGA (YKE) | 4|250 | SMALL T&R|Yes|SNAGCU|Level-1-260C-UNLIM|-40 to 125|C|
|Active|Production|DSBGA (YKE) | 4|250 | SMALL T&R|Yes|SNAGCU|Level-1-260C-UNLIM|-40 to 125|C|
|Active|Production|DSBGA (YKE) | 4|250 | SMALL T&R|Yes|SNAGCU|Level-1-260C-UNLIM|-40 to 125|C|
|Active|Production|DSBGA (YKE) | 4|250 | SMALL T&R|Yes|SNAGCU|Level-1-260C-UNLIM|-40 to 125|D|
|Active|Production|DSBGA (YKE) | 4|250 | SMALL T&R|Yes|SNAGCU|Level-1-260C-UNLIM|-40 to 125|D|
|Active|Production|DSBGA (YKE) | 4|250 | SMALL T&R|Yes|SNAGCU|Level-1-260C-UNLIM|-40 to 125|D|
|Active|Production|DSBGA (YKE) | 4|250 | SMALL T&R|Yes|SNAGCU|Level-1-260C-UNLIM|-40 to 125|Z|
|Active|Production|DSBGA (YKE) | 4|250 | SMALL T&R|Yes|SNAGCU|Level-1-260C-UNLIM|-40 to 125|Z|
|Active|Production|DSBGA (YKE) | 4|3000 | LARGE T&R|Yes|SNAGCU|Level-1-260C-UNLIM|-40 to 125|R|
|Active|Production|DSBGA (YKE) | 4|3000 | LARGE T&R|Yes|SNAGCU|Level-1-260C-UNLIM|-40 to 125|R|
|Active|Production|DSBGA (YKE) | 4|3000 | LARGE T&R|Yes|SNAGCU|Level-1-260C-UNLIM|-40 to 125|R|
|Active|Production|DSBGA (YKE) | 4|3000 | LARGE T&R|Yes|SNAGCU|Level-1-260C-UNLIM|-40 to 125|S|
|Active|Production|DSBGA (YKE) | 4|3000 | LARGE T&R|Yes|SNAGCU|Level-1-260C-UNLIM|-40 to 125|S|
|Active|Production|DSBGA (YKE) | 4|3000 | LARGE T&R|Yes|SNAGCU|Level-1-260C-UNLIM|-40 to 125|S|
|Active|Production|DSBGA (YKE) | 4|3000 | LARGE T&R|Yes|SNAGCU|Level-1-260C-UNLIM|-40 to 125|E|
|Active|Production|DSBGA (YKE) | 4|3000 | LARGE T&R|Yes|SNAGCU|Level-1-260C-UNLIM|-40 to 125|E|
|Active|Production|DSBGA (YKE) | 4|3000 | LARGE T&R|Yes|SNAGCU|Level-1-260C-UNLIM|-40 to 125|E|
|Active|Production|DSBGA (YKE) | 4|3000 | LARGE T&R|Yes|SNAGCU|Level-1-260C-UNLIM|-40 to 125|U|
|Active|Production|DSBGA (YKE) | 4|3000 | LARGE T&R|Yes|SNAGCU|Level-1-260C-UNLIM|-40 to 125|U|
|Active|Production|DSBGA (YKE) | 4|3000 | LARGE T&R|Yes|SNAGCU|Level-1-260C-UNLIM|-40 to 125|U|
|Active|Production|DSBGA (YKE) | 4|3000 | LARGE T&R|Yes|SNAGCU|Level-1-260C-UNLIM|-40 to 125|V|
|Active|Production|DSBGA (YKE) | 4|3000 | LARGE T&R|Yes|SNAGCU|Level-1-260C-UNLIM|-40 to 125|V|

LP5907UVE-2.8/NOPB.A LP5907UVE-2.8/NOPB.B LP5907UVE-2.85/NO.A LP5907UVE-2.85/NOPB LP5907UVE-3.0/NOPB LP5907UVE-3.0/NOPB.A LP5907UVE-3.0/NOPB.B LP5907UVE-3.1/NOPB LP5907UVE-3.1/NOPB.A LP5907UVE-3.2/NOPB LP5907UVE-3.2/NOPB.A LP5907UVE-3.2/NOPB.B LP5907UVE-3.3/NOPB LP5907UVE-3.3/NOPB.A LP5907UVE-3.3/NOPB.B LP5907UVE-4.5/NOPB LP5907UVE-4.5/NOPB.A LP5907UVX-1.2/NOPB LP5907UVX-1.2/NOPB.A LP5907UVX-1.2/NOPB.B LP5907UVX-1.8/NOPB LP5907UVX-1.8/NOPB.A LP5907UVX-1.8/NOPB.B LP5907UVX-2.5/NOPB LP5907UVX-2.5/NOPB.A LP5907UVX-2.5/NOPB.B LP5907UVX-2.8/NOPB LP5907UVX-2.8/NOPB.A LP5907UVX-2.8/NOPB.B LP5907UVX-2.85/NO.A LP5907UVX-2.85/NOPB

Addendum-Page

### PACKAGE OPTION ADDENDUM

www.ti.com 7-Nov-2025

**Orderable part number**

|Status (1)|Material type (2)|Package | Pins|Package qty | Carrier|RoHS (3)|Lead finish/ Ball material (4)|MSL rating/ Peak reflow (5)|Op temp (°C)|Part marking (6)|
|---|---|---|---|---|---|---|---|---|
|Active|Production|DSBGA (YKE) | 4|3000 | LARGE T&R|Yes|SNAGCU|Level-1-260C-UNLIM|-40 to 125|B|
|Active|Production|DSBGA (YKE) | 4|3000 | LARGE T&R|Yes|SNAGCU|Level-1-260C-UNLIM|-40 to 125|B|
|Active|Production|DSBGA (YKE) | 4|3000 | LARGE T&R|Yes|SNAGCU|Level-1-260C-UNLIM|-40 to 125|B|
|Active|Production|DSBGA (YKE) | 4|3000 | LARGE T&R|Yes|SNAGCU|Level-1-260C-UNLIM|-40 to 125|X|
|Active|Production|DSBGA (YKE) | 4|3000 | LARGE T&R|Yes|SNAGCU|Level-1-260C-UNLIM|-40 to 125|X|
|Active|Production|DSBGA (YKE) | 4|3000 | LARGE T&R|Yes|SNAGCU|Level-1-260C-UNLIM|-40 to 125|C|
|Active|Production|DSBGA (YKE) | 4|3000 | LARGE T&R|Yes|SNAGCU|Level-1-260C-UNLIM|-40 to 125|C|
|Active|Production|DSBGA (YKE) | 4|3000 | LARGE T&R|Yes|SNAGCU|Level-1-260C-UNLIM|-40 to 125|C|
|Active|Production|DSBGA (YKE) | 4|3000 | LARGE T&R|Yes|SNAGCU|Level-1-260C-UNLIM|-40 to 125|D|
|Active|Production|DSBGA (YKE) | 4|3000 | LARGE T&R|Yes|SNAGCU|Level-1-260C-UNLIM|-40 to 125|D|
|Active|Production|DSBGA (YKE) | 4|3000 | LARGE T&R|Yes|SNAGCU|Level-1-260C-UNLIM|-40 to 125|D|
|Active|Production|DSBGA (YKE) | 4|3000 | LARGE T&R|Yes|SNAGCU|Level-1-260C-UNLIM|-40 to 125|Z|
|Active|Production|DSBGA (YKE) | 4|3000 | LARGE T&R|Yes|SNAGCU|Level-1-260C-UNLIM|-40 to 125|Z|
|Active|Production|DSBGA (YKE) | 4|3000 | LARGE T&R|Yes|SNAGCU|Level-1-260C-UNLIM|-40 to 125|8|
|Active|Production|DSBGA (YKE) | 4|3000 | LARGE T&R|Yes|SNAGCU|Level-1-260C-UNLIM|-40 to 125|8|
|Active|Production|DSBGA (YKE) | 4|3000 | LARGE T&R|Yes|SNAGCU|Level-1-260C-UNLIM|-40 to 125|8|
|Active|Production|DSBGA (YKE) | 4|3000 | LARGE T&R|Yes|SNAGCU|Level-1-260C-UNLIM|-40 to 125|9|
|Active|Production|DSBGA (YKE) | 4|3000 | LARGE T&R|Yes|SNAGCU|Level-1-260C-UNLIM|-40 to 125|9|
|Active|Production|DSBGA (YKG) | 4|3000 | LARGE T&R|Yes|SNAGCU|Level-1-260C-UNLIM|-40 to 125|3|
|Active|Production|DSBGA (YKG) | 4|3000 | LARGE T&R|Yes|SNAGCU|Level-1-260C-UNLIM|-40 to 125|3|
|Active|Production|DSBGA (YKG) | 4|3000 | LARGE T&R|Yes|SNAGCU|Level-1-260C-UNLIM|-40 to 125|5|
|Active|Production|DSBGA (YKG) | 4|3000 | LARGE T&R|Yes|SNAGCU|Level-1-260C-UNLIM|-40 to 125|5|
|Active|Production|DSBGA (YKG) | 4|3000 | LARGE T&R|Yes|SNAGCU|Level-1-260C-UNLIM|-40 to 125|P|
|Active|Production|DSBGA (YKG) | 4|3000 | LARGE T&R|Yes|SNAGCU|Level-1-260C-UNLIM|-40 to 125|P|

LP5907UVX-3.0/NOPB LP5907UVX-3.0/NOPB.A LP5907UVX-3.0/NOPB.B LP5907UVX-3.1/NOPB LP5907UVX-3.1/NOPB.A LP5907UVX-3.2/NOPB LP5907UVX-3.2/NOPB.A LP5907UVX-3.2/NOPB.B LP5907UVX-3.3/NOPB LP5907UVX-3.3/NOPB.A LP5907UVX-3.3/NOPB.B LP5907UVX-4.5/NOPB LP5907UVX-4.5/NOPB.A LP5907UVX19/NOPB LP5907UVX19/NOPB.A LP5907UVX19/NOPB.B LP5907UVX37/NOPB LP5907UVX37/NOPB.A LP5907YKGR-2.8 LP5907YKGR-2.8.B LP5907YKGR-2.825 LP5907YKGR-2.825.B LP5907YKGR-2.85 LP5907YKGR-2.85.B

**(1)** **Status:** For more details on status, see our product life cycle.
**(2)** **Material type:** When designated, preproduction parts are prototypes/experimental devices, and are not yet approved or released for full production. Testing and final process, including without limitation quality assurance, reliability performance testing, and/or process qualification, may not yet be complete, and this item is subject to further changes or possible discontinuation. If available for ordering, purchases will be subject to an additional waiver at checkout, and are intended for early internal evaluation purposes only. These items are sold without warranties of any kind.
**(3)** **RoHS values:** Yes, No, RoHS Exempt. See the TI RoHS Statement for additional information and value definition.
Addendum-Page

### PACKAGE OPTION ADDENDUM

www.ti.com 7-Nov-2025

**(4)** **Lead finish/Ball material:**
Parts may have multiple material finish options. Finish options are separated by a vertical ruled line. Lead finish/Ball material values may wrap to two lines if the finish value exceeds the maximum column width.

**(5)** **MSL rating/Peak reflow:**
The moisture sensitivity level ratings and peak solder (reflow) temperatures. In the event that a part has multiple moisture sensitivity ratings, only the lowest level per JEDEC standards is shown. Refer to the shipping label for the actual reflow temperature that will be used to mount the part to the printed circuit board.

**(6)** **Part marking:**
There may be an additional marking, which relates to the logo, the lot trace code information, or the environmental category of the part.

Multiple part markings will be inside parentheses. Only one part marking contained in parentheses and separated by a "~" will appear on a part. If a line is indented then it is a continuation of the previous line and the two combined represent the entire part marking for that device.

**Important Information and Disclaimer:** The information provided on this page represents TI's knowledge and belief as of the date that it is provided. TI bases its knowledge and belief on information provided by third parties, and makes no representation or warranty as to the accuracy of such information. Efforts are underway to better integrate information from third parties. TI has taken and continues to take reasonable steps to provide representative and accurate information but may not have conducted destructive testing or chemical analysis on incoming materials and chemicals. TI and TI suppliers consider certain information to be proprietary, and thus CAS numbers and other limited information may not be available for release.

In no event shall TI's liability arising out of such information exceed the total purchase price of the TI part(s) at issue in this document sold by TI to Customer on an annual basis.

**OTHER QUALIFIED VERSIONS OF LP5907 :**

• Automotive : LP5907-Q1

NOTE: Qualified Version Definitions:

• Automotive-Q100 devices qualified for high-reliability automotive applications targeting zero defects

Addendum-Page

### PACKAGE MATERIALS INFORMATION

www.ti.com 15-Jul-2026

##### TAPE AND REEL INFORMATION

**REEL DIMENSIONS TAPE DIMENSIONS** K0 P1

W B0 Reel Diameter Cavity A0 A0 Dimension designed to accommodate the component width B0 Dimension designed to accommodate the component length K0 Dimension designed to accommodate the component thickness W Overall width of the carrier tape P1 Pitch between successive cavity centers

Reel Width (W1) **QUADRANT ASSIGNMENTS FOR PIN 1 ORIENTATION IN TAPE** Sprocket Holes

||Q1 Q2|Q1|Q2|||
|---|---|---|---|---|---|
||Q3 Q4|Q3|Q4|User Direction of Feed||

Pocket Quadrants

*All dimensions are nominal **Device Package Package Pins SPQ Reel Reel A0 B0 K0 P1 W Pin1** **Type Drawing Diameter Width (mm) (mm) (mm) (mm) (mm) Quadrant** **(mm) W1 (mm)**

|LP5907A28YKMR|DSBGA|YKM|4 3000|178.0|8.4|0.74|0.74|0.54|4.0|8.0|Q1|
|---|---|---|---|---|---|---|---|---|---|---|---|
|LP5907A33YKMR|DSBGA|YKM|4 3000|178.0|8.4|0.74|0.74|0.54|4.0|8.0|Q1|
|LP5907MFX-1.2/NOPB|SOT-23|DBV|5 3000|180.0|8.4|3.2|3.2|1.4|4.0|8.0|Q3|
|LP5907MFX-1.2/NOPB|SOT-23|DBV|5 3000|180.0|8.4|3.2|3.2|1.4|4.0|8.0|Q3|
|LP5907MFX-1.2/NOPB|SOT-23|DBV|5 3000|178.0|8.4|3.2|3.2|1.4|4.0|8.0|Q3|
|LP5907MFX-1.5/NOPB|SOT-23|DBV|5 3000|178.0|8.4|3.2|3.2|1.4|4.0|8.0|Q3|
|LP5907MFX-1.5/NOPB|SOT-23|DBV|5 3000|180.0|8.4|3.2|3.2|1.4|4.0|8.0|Q3|
|LP5907MFX-1.5/NOPB|SOT-23|DBV|5 3000|180.0|8.4|3.2|3.2|1.4|4.0|8.0|Q3|
|LP5907MFX-1.8/NOPB|SOT-23|DBV|5 3000|180.0|8.4|3.2|3.2|1.4|4.0|8.0|Q3|
|LP5907MFX-1.8/NOPB|SOT-23|DBV|5 3000|178.0|8.4|3.2|3.2|1.4|4.0|8.0|Q3|
|LP5907MFX-1.8/NOPB|SOT-23|DBV|5 3000|180.0|8.4|3.2|3.2|1.4|4.0|8.0|Q3|
|LP5907MFX-2.5/NOPB|SOT-23|DBV|5 3000|180.0|8.4|3.2|3.2|1.4|4.0|8.0|Q3|
|LP5907MFX-2.5/NOPB|SOT-23|DBV|5 3000|178.0|8.4|3.2|3.2|1.4|4.0|8.0|Q3|
|LP5907MFX-2.5/NOPB|SOT-23|DBV|5 3000|180.0|8.4|3.2|3.2|1.4|4.0|8.0|Q3|
|LP5907MFX-2.8/NOPB|SOT-23|DBV|5 3000|178.0|8.4|3.2|3.2|1.4|4.0|8.0|Q3|
|LP5907MFX-2.8/NOPB|SOT-23|DBV|5 3000|180.0|8.4|3.2|3.2|1.4|4.0|8.0|Q3|

LP5907A28YKMR DSBGA YKM 4 3000 178.0 8.4 0.74 0.74 0.54 4.0 8.0 Q1

Pack Materials-Page

### PACKAGE MATERIALS INFORMATION

www.ti.com 15-Jul-2026

|Device|Package Type|Package Drawing|Pins|SPQ Diameter|Reel (mm) W1 (mm)|Reel Width|A0 (mm)|B0 (mm)|K0 (mm)|P1 (mm)|W (mm) Quadrant|Pin1|
|---|---|---|---|---|---|---|---|---|---|---|---|---|
|LP5907MFX-2.8/NOPB|SOT-23|DBV|5|3000|180.0|8.4|3.2|3.2|1.4|4.0|8.0|Q3|
|LP5907MFX-2.85/NOPB|SOT-23|DBV|5|3000|178.0|8.4|3.2|3.2|1.4|4.0|8.0|Q3|
|LP5907MFX-2.85/NOPB|SOT-23|DBV|5|3000|180.0|8.4|3.2|3.2|1.4|4.0|8.0|Q3|
|LP5907MFX-2.85/NOPB|SOT-23|DBV|5|3000|180.0|8.4|3.2|3.2|1.4|4.0|8.0|Q3|
|LP5907MFX-2.9/NOPB|SOT-23|DBV|5|3000|178.0|8.4|3.2|3.2|1.4|4.0|8.0|Q3|
|LP5907MFX-2.9/NOPB|SOT-23|DBV|5|3000|180.0|8.4|3.2|3.2|1.4|4.0|8.0|Q3|
|LP5907MFX-2.9/NOPB|SOT-23|DBV|5|3000|180.0|8.4|3.2|3.2|1.4|4.0|8.0|Q3|
|LP5907MFX-3.0/NOPB|SOT-23|DBV|5|3000|180.0|8.4|3.2|3.2|1.4|4.0|8.0|Q3|
|LP5907MFX-3.0/NOPB|SOT-23|DBV|5|3000|180.0|8.4|3.2|3.2|1.4|4.0|8.0|Q3|
|LP5907MFX-3.0/NOPB|SOT-23|DBV|5|3000|178.0|8.4|3.2|3.2|1.4|4.0|8.0|Q3|
|LP5907MFX-3.1/NOPB|SOT-23|DBV|5|3000|180.0|8.4|3.2|3.2|1.4|4.0|8.0|Q3|
|LP5907MFX-3.1/NOPB|SOT-23|DBV|5|3000|180.0|8.4|3.2|3.2|1.4|4.0|8.0|Q3|
|LP5907MFX-3.1/NOPB|SOT-23|DBV|5|3000|178.0|8.4|3.2|3.2|1.4|4.0|8.0|Q3|
|LP5907MFX-3.2/NOPB|SOT-23|DBV|5|3000|180.0|8.4|3.2|3.2|1.4|4.0|8.0|Q3|
|LP5907MFX-3.2/NOPB|SOT-23|DBV|5|3000|180.0|8.4|3.2|3.2|1.4|4.0|8.0|Q3|
|LP5907MFX-3.2/NOPB|SOT-23|DBV|5|3000|178.0|8.4|3.2|3.2|1.4|4.0|8.0|Q3|
|LP5907MFX-3.3/NOPB|SOT-23|DBV|5|3000|180.0|8.4|3.2|3.2|1.4|4.0|8.0|Q3|
|LP5907MFX-3.3/NOPB|SOT-23|DBV|5|3000|178.0|8.4|3.2|3.2|1.4|4.0|8.0|Q3|
|LP5907MFX-3.3/NOPB|SOT-23|DBV|5|3000|180.0|8.4|3.2|3.2|1.4|4.0|8.0|Q3|
|LP5907MFX-4.5/NOPB|SOT-23|DBV|5|3000|180.0|8.4|3.2|3.2|1.4|4.0|8.0|Q3|
|LP5907MFX-4.5/NOPB|SOT-23|DBV|5|3000|178.0|8.4|3.2|3.2|1.4|4.0|8.0|Q3|
|LP5907SNX-1.2/NOPB|X2SON|DQN|4|3000|180.0|9.5|1.16|1.16|0.63|4.0|8.0|Q2|
|LP5907SNX-1.2/NOPB|X2SON|DQN|4|3000|180.0|8.4|1.16|1.16|0.5|4.0|8.0|Q2|
|LP5907SNX-1.8/NOPB|X2SON|DQN|4|3000|180.0|9.5|1.16|1.16|0.63|4.0|8.0|Q2|
|LP5907SNX-1.8/NOPB|X2SON|DQN|4|3000|180.0|8.4|1.16|1.16|0.5|4.0|8.0|Q2|
|LP5907SNX-1.9|X2SON|DQN|4|3000|180.0|8.4|1.16|1.16|0.5|4.0|8.0|Q2|
|LP5907SNX-1.9|X2SON|DQN|4|3000|180.0|9.5|1.16|1.16|0.63|4.0|8.0|Q2|
|LP5907SNX-2.2/NOPB|X2SON|DQN|4|3000|180.0|8.4|1.16|1.16|0.5|4.0|8.0|Q2|
|LP5907SNX-2.2/NOPB|X2SON|DQN|4|3000|180.0|9.5|1.16|1.16|0.63|4.0|8.0|Q2|
|LP5907SNX-2.5/NOPB|X2SON|DQN|4|3000|180.0|9.5|1.16|1.16|0.63|4.0|8.0|Q2|
|LP5907SNX-2.5/NOPB|X2SON|DQN|4|3000|180.0|8.4|1.16|1.16|0.5|4.0|8.0|Q2|
|LP5907SNX-2.7/NOPB|X2SON|DQN|4|3000|180.0|8.4|1.16|1.16|0.5|4.0|8.0|Q2|
|LP5907SNX-2.7/NOPB|X2SON|DQN|4|3000|180.0|9.5|1.16|1.16|0.63|4.0|8.0|Q2|
|LP5907SNX-2.75|X2SON|DQN|4|3000|180.0|9.5|1.16|1.16|0.63|4.0|8.0|Q2|
|LP5907SNX-2.75|X2SON|DQN|4|3000|180.0|8.4|1.16|1.16|0.5|4.0|8.0|Q2|
|LP5907SNX-2.8/NOPB|X2SON|DQN|4|3000|180.0|9.5|1.16|1.16|0.63|4.0|8.0|Q2|
|LP5907SNX-2.8/NOPB|X2SON|DQN|4|3000|180.0|8.4|1.16|1.16|0.5|4.0|8.0|Q2|
|LP5907SNX-2.85/G4|X2SON|DQN|4|3000|180.0|8.4|1.16|1.16|0.5|4.0|8.0|Q2|
|LP5907SNX-2.85/NOPB|X2SON|DQN|4|3000|180.0|8.4|1.16|1.16|0.5|4.0|8.0|Q2|
|LP5907SNX-2.85/NOPB|X2SON|DQN|4|3000|180.0|9.5|1.16|1.16|0.63|4.0|8.0|Q2|
|LP5907SNX-2.9/NOPB|X2SON|DQN|4|3000|180.0|9.5|1.16|1.16|0.63|4.0|8.0|Q2|

Pack Materials-Page

### PACKAGE MATERIALS INFORMATION

www.ti.com 15-Jul-2026

|Device|Package Type|Package Drawing|Pins|SPQ Diameter|Reel (mm) W1 (mm)|Reel Width|A0 (mm)|B0 (mm)|K0 (mm)|P1 (mm)|W (mm) Quadrant|Pin1|
|---|---|---|---|---|---|---|---|---|---|---|---|---|
|LP5907SNX-2.9/NOPB|X2SON|DQN|4|3000|180.0|8.4|1.16|1.16|0.5|4.0|8.0|Q2|
|LP5907SNX-3.0/NOPB|X2SON|DQN|4|3000|180.0|8.4|1.16|1.16|0.5|4.0|8.0|Q2|
|LP5907SNX-3.0/NOPB|X2SON|DQN|4|3000|180.0|9.5|1.16|1.16|0.63|4.0|8.0|Q2|
|LP5907SNX-3.1/NOPB|X2SON|DQN|4|3000|180.0|9.5|1.16|1.16|0.63|4.0|8.0|Q2|
|LP5907SNX-3.1/NOPB|X2SON|DQN|4|3000|180.0|8.4|1.16|1.16|0.5|4.0|8.0|Q2|
|LP5907SNX-3.2/NOPB|X2SON|DQN|4|3000|180.0|8.4|1.16|1.16|0.5|4.0|8.0|Q2|
|LP5907SNX-3.2/NOPB|X2SON|DQN|4|3000|180.0|9.5|1.16|1.16|0.63|4.0|8.0|Q2|
|LP5907SNX-3.3/NOPB|X2SON|DQN|4|3000|180.0|9.5|1.16|1.16|0.63|4.0|8.0|Q2|
|LP5907SNX-3.3/NOPB|X2SON|DQN|4|3000|180.0|8.4|1.16|1.16|0.5|4.0|8.0|Q2|
|LP5907SNX-4.0/NOPB|X2SON|DQN|4|3000|180.0|9.5|1.16|1.16|0.63|4.0|8.0|Q2|
|LP5907SNX-4.0/NOPB|X2SON|DQN|4|3000|180.0|8.4|1.16|1.16|0.5|4.0|8.0|Q2|
|LP5907SNX-4.5/NOPB|X2SON|DQN|4|3000|180.0|9.5|1.16|1.16|0.63|4.0|8.0|Q2|
|LP5907SNX-4.5/NOPB|X2SON|DQN|4|3000|180.0|8.4|1.16|1.16|0.5|4.0|8.0|Q2|
|LP5907SNX1.2NOPBG4|X2SON|DQN|4|3000|180.0|8.4|1.16|1.16|0.5|4.0|8.0|Q2|
|LP5907SNX1.8NOPBG4|X2SON|DQN|4|3000|180.0|8.4|1.16|1.16|0.5|4.0|8.0|Q2|
|LP5907SNX2.2NOPBG4|X2SON|DQN|4|3000|180.0|8.4|1.16|1.16|0.5|4.0|8.0|Q2|
|LP5907SNX2.5NOPBG4|X2SON|DQN|4|3000|180.0|8.4|1.16|1.16|0.5|4.0|8.0|Q2|
|LP5907SNX2.7NOPBG4|X2SON|DQN|4|3000|180.0|8.4|1.16|1.16|0.5|4.0|8.0|Q2|
|LP5907SNX2.8NOPBG4|X2SON|DQN|4|3000|180.0|8.4|1.16|1.16|0.5|4.0|8.0|Q2|
|LP5907SNX2.9NOPBG4|X2SON|DQN|4|3000|180.0|8.4|1.16|1.16|0.5|4.0|8.0|Q2|
|LP5907SNX3.0NOPBG4|X2SON|DQN|4|3000|180.0|9.5|1.16|1.16|0.63|4.0|8.0|Q2|
|LP5907SNX3.1NOPBG4|X2SON|DQN|4|3000|180.0|8.4|1.16|1.16|0.5|4.0|8.0|Q2|
|LP5907SNX3.2NOPBG4|X2SON|DQN|4|3000|180.0|8.4|1.16|1.16|0.5|4.0|8.0|Q2|
|LP5907SNX3.3NOPBG4|X2SON|DQN|4|3000|180.0|8.4|1.16|1.16|0.5|4.0|8.0|Q2|
|LP5907SNX4.0NOPBG4|X2SON|DQN|4|3000|180.0|8.4|1.16|1.16|0.5|4.0|8.0|Q2|
|LP5907SNX4.5NOPBG4|X2SON|DQN|4|3000|180.0|8.4|1.16|1.16|0.5|4.0|8.0|Q2|
|LP5907UVE-1.2/NOPB|DSBGA|YKE|4|250|178.0|8.4|0.71|0.71|0.51|2.0|8.0|Q1|
|LP5907UVE-1.8/NOPB|DSBGA|YKE|4|250|178.0|8.4|0.71|0.71|0.51|2.0|8.0|Q1|
|LP5907UVE-2.8/NOPB|DSBGA|YKE|4|250|178.0|8.4|0.71|0.71|0.51|2.0|8.0|Q1|
|LP5907UVE-2.85/NOPB|DSBGA|YKE|4|250|178.0|8.4|0.71|0.71|0.51|2.0|8.0|Q1|
|LP5907UVE-3.0/NOPB|DSBGA|YKE|4|250|178.0|8.4|0.71|0.71|0.51|2.0|8.0|Q1|
|LP5907UVE-3.1/NOPB|DSBGA|YKE|4|250|178.0|8.4|0.71|0.71|0.51|2.0|8.0|Q1|
|LP5907UVE-3.2/NOPB|DSBGA|YKE|4|250|178.0|8.4|0.71|0.71|0.51|2.0|8.0|Q1|
|LP5907UVE-3.3/NOPB|DSBGA|YKE|4|250|178.0|8.4|0.71|0.71|0.51|2.0|8.0|Q1|
|LP5907UVE-4.5/NOPB|DSBGA|YKE|4|250|178.0|8.4|0.71|0.71|0.51|2.0|8.0|Q1|
|LP5907UVX-1.2/NOPB|DSBGA|YKE|4|3000|178.0|8.4|0.71|0.71|0.51|2.0|8.0|Q1|
|LP5907UVX-1.8/NOPB|DSBGA|YKE|4|3000|178.0|8.4|0.71|0.71|0.51|2.0|8.0|Q1|
|LP5907UVX-2.5/NOPB|DSBGA|YKE|4|3000|178.0|8.4|0.71|0.71|0.51|2.0|8.0|Q1|
|LP5907UVX-2.8/NOPB|DSBGA|YKE|4|3000|178.0|8.4|0.71|0.71|0.51|2.0|8.0|Q1|
|LP5907UVX-2.85/NOPB|DSBGA|YKE|4|3000|178.0|8.4|0.71|0.71|0.51|2.0|8.0|Q1|
|LP5907UVX-3.0/NOPB|DSBGA|YKE|4|3000|178.0|8.4|0.71|0.71|0.51|2.0|8.0|Q1|

Pack Materials-Page

### PACKAGE MATERIALS INFORMATION

www.ti.com 15-Jul-2026

**Device Package Package Pins SPQ Reel Reel A0 B0 K0 P1 W Pin1** **Type Drawing Diameter Width (mm) (mm) (mm) (mm) (mm) Quadrant** **(mm) W1 (mm)** LP5907UVX-3.1/NOPB DSBGA YKE 4 3000 178.0 8.4 0.71 0.71 0.51 2.0 8.0 Q1

|LP5907UVX-3.1/NOPB||DSBGA|YKE|4 3000|178.0|8.4|0.71|0.71|0.51|2.0|8.0|Q1|
|---|---|---|---|---|---|---|---|---|---|---|---|---|
|LP5907UVX-3.2/NOPB||DSBGA|YKE|4 3000|178.0|8.4|0.71|0.71|0.51|2.0|8.0|Q1|
|LP5907UVX-3.3/NOPB||DSBGA|YKE|4 3000|178.0|8.4|0.71|0.71|0.51|2.0|8.0|Q1|
|LP5907UVX-4.5/NOPB||DSBGA|YKE|4 3000|178.0|8.4|0.71|0.71|0.51|2.0|8.0|Q1|
|LP5907UVX19/NOPB||DSBGA|YKE|4 3000|178.0|8.4|0.71|0.71|0.51|2.0|8.0|Q1|
|LP5907UVX37/NOPB||DSBGA|YKE|4 3000|178.0|8.4|0.71|0.71|0.51|2.0|8.0|Q1|
|LP5907YKGR-2.8||DSBGA|YKG|4 3000|178.0|9.2|0.72|0.72|0.39|4.0|8.0|Q1|
|LP5907YKGR-2.825||DSBGA|YKG|4 3000|178.0|9.2|0.72|0.72|0.39|4.0|8.0|Q1|
|LP5907YKGR-2.85||DSBGA|YKG|4 3000|178.0|9.2|0.72|0.72|0.39|4.0|8.0|Q1|

Pack Materials-Page

### PACKAGE MATERIALS INFORMATION

www.ti.com 15-Jul-2026

|TAPE AND REEL BOX DIMENSIONS *All dimensions are nominal|W||Width (mm) L||H||
|---|---|---|---|---|---|---|
||Device Package Type|Package Drawing|Pins||SPQ|Length (mm) Width (mm) Height (mm)|
|LP5907A28YKMR|DSBGA||YKM 4||3000|220.0 220.0 35.0|
|LP5907A33YKMR|DSBGA||YKM 4||3000|220.0 220.0 35.0|
|LP5907MFX-1.2/NOPB|SOT-23||DBV 5||3000|210.0 185.0 35.0|
|LP5907MFX-1.2/NOPB|SOT-23||DBV 5||3000|210.0 185.0 35.0|
|LP5907MFX-1.2/NOPB|SOT-23||DBV 5||3000|208.0 191.0 35.0|
|LP5907MFX-1.5/NOPB|SOT-23||DBV 5||3000|208.0 191.0 35.0|
|LP5907MFX-1.5/NOPB|SOT-23||DBV 5||3000|210.0 185.0 35.0|
|LP5907MFX-1.5/NOPB|SOT-23||DBV 5||3000|210.0 185.0 35.0|
|LP5907MFX-1.8/NOPB|SOT-23||DBV 5||3000|210.0 185.0 35.0|
|LP5907MFX-1.8/NOPB|SOT-23||DBV 5||3000|208.0 191.0 35.0|
|LP5907MFX-1.8/NOPB|SOT-23||DBV 5||3000|210.0 185.0 35.0|
|LP5907MFX-2.5/NOPB|SOT-23||DBV 5||3000|210.0 185.0 35.0|
|LP5907MFX-2.5/NOPB|SOT-23||DBV 5||3000|208.0 191.0 35.0|
|LP5907MFX-2.5/NOPB|SOT-23||DBV 5||3000|210.0 185.0 35.0|
|LP5907MFX-2.8/NOPB|SOT-23||DBV 5||3000|208.0 191.0 35.0|
|LP5907MFX-2.8/NOPB|SOT-23||DBV 5||3000|210.0 185.0 35.0|
|LP5907MFX-2.8/NOPB|SOT-23||DBV 5||3000|210.0 185.0 35.0|
|LP5907MFX-2.85/NOPB|SOT-23||DBV 5||3000|208.0 191.0 35.0|

Pack Materials-Page

### PACKAGE MATERIALS INFORMATION

www.ti.com 15-Jul-2026

**Device**

||Package Type|Package Drawing|Pins|SPQ|Length (mm)|Width (mm)|Height (mm)|
|---|---|---|---|---|---|---|---|
|LP5907MFX-2.85/NOPB|SOT-23|DBV|5|3000|210.0|185.0|35.0|
|LP5907MFX-2.85/NOPB|SOT-23|DBV|5|3000|210.0|185.0|35.0|
|LP5907MFX-2.9/NOPB|SOT-23|DBV|5|3000|208.0|191.0|35.0|
|LP5907MFX-2.9/NOPB|SOT-23|DBV|5|3000|210.0|185.0|35.0|
|LP5907MFX-2.9/NOPB|SOT-23|DBV|5|3000|210.0|185.0|35.0|
|LP5907MFX-3.0/NOPB|SOT-23|DBV|5|3000|210.0|185.0|35.0|
|LP5907MFX-3.0/NOPB|SOT-23|DBV|5|3000|210.0|185.0|35.0|
|LP5907MFX-3.0/NOPB|SOT-23|DBV|5|3000|208.0|191.0|35.0|
|LP5907MFX-3.1/NOPB|SOT-23|DBV|5|3000|210.0|185.0|35.0|
|LP5907MFX-3.1/NOPB|SOT-23|DBV|5|3000|210.0|185.0|35.0|
|LP5907MFX-3.1/NOPB|SOT-23|DBV|5|3000|208.0|191.0|35.0|
|LP5907MFX-3.2/NOPB|SOT-23|DBV|5|3000|210.0|185.0|35.0|
|LP5907MFX-3.2/NOPB|SOT-23|DBV|5|3000|210.0|185.0|35.0|
|LP5907MFX-3.2/NOPB|SOT-23|DBV|5|3000|208.0|191.0|35.0|
|LP5907MFX-3.3/NOPB|SOT-23|DBV|5|3000|210.0|185.0|35.0|
|LP5907MFX-3.3/NOPB|SOT-23|DBV|5|3000|208.0|191.0|35.0|
|LP5907MFX-3.3/NOPB|SOT-23|DBV|5|3000|210.0|185.0|35.0|
|LP5907MFX-4.5/NOPB|SOT-23|DBV|5|3000|210.0|185.0|35.0|
|LP5907MFX-4.5/NOPB|SOT-23|DBV|5|3000|208.0|191.0|35.0|
|LP5907SNX-1.2/NOPB|X2SON|DQN|4|3000|184.0|184.0|19.0|
|LP5907SNX-1.2/NOPB|X2SON|DQN|4|3000|210.0|185.0|35.0|
|LP5907SNX-1.8/NOPB|X2SON|DQN|4|3000|184.0|184.0|19.0|
|LP5907SNX-1.8/NOPB|X2SON|DQN|4|3000|210.0|185.0|35.0|
|LP5907SNX-1.9|X2SON|DQN|4|3000|210.0|185.0|35.0|
|LP5907SNX-1.9|X2SON|DQN|4|3000|184.0|184.0|19.0|
|LP5907SNX-2.2/NOPB|X2SON|DQN|4|3000|210.0|185.0|35.0|
|LP5907SNX-2.2/NOPB|X2SON|DQN|4|3000|184.0|184.0|19.0|
|LP5907SNX-2.5/NOPB|X2SON|DQN|4|3000|184.0|184.0|19.0|
|LP5907SNX-2.5/NOPB|X2SON|DQN|4|3000|210.0|185.0|35.0|
|LP5907SNX-2.7/NOPB|X2SON|DQN|4|3000|210.0|185.0|35.0|
|LP5907SNX-2.7/NOPB|X2SON|DQN|4|3000|184.0|184.0|19.0|
|LP5907SNX-2.75|X2SON|DQN|4|3000|184.0|184.0|19.0|
|LP5907SNX-2.75|X2SON|DQN|4|3000|210.0|185.0|35.0|
|LP5907SNX-2.8/NOPB|X2SON|DQN|4|3000|184.0|184.0|19.0|
|LP5907SNX-2.8/NOPB|X2SON|DQN|4|3000|210.0|185.0|35.0|
|LP5907SNX-2.85/G4|X2SON|DQN|4|3000|210.0|185.0|35.0|
|LP5907SNX-2.85/NOPB|X2SON|DQN|4|3000|210.0|185.0|35.0|
|LP5907SNX-2.85/NOPB|X2SON|DQN|4|3000|184.0|184.0|19.0|
|LP5907SNX-2.9/NOPB|X2SON|DQN|4|3000|184.0|184.0|19.0|
|LP5907SNX-2.9/NOPB|X2SON|DQN|4|3000|210.0|185.0|35.0|
|LP5907SNX-3.0/NOPB|X2SON|DQN|4|3000|210.0|185.0|35.0|
|LP5907SNX-3.0/NOPB|X2SON|DQN|4|3000|184.0|184.0|19.0|
|LP5907SNX-3.1/NOPB|X2SON|DQN|4|3000|184.0|184.0|19.0|

Pack Materials-Page

### PACKAGE MATERIALS INFORMATION

www.ti.com 15-Jul-2026

**Device**

||Package Type|Package Drawing|Pins|SPQ|Length (mm)|Width (mm)|Height (mm)|
|---|---|---|---|---|---|---|---|
|LP5907SNX-3.1/NOPB|X2SON|DQN|4|3000|210.0|185.0|35.0|
|LP5907SNX-3.2/NOPB|X2SON|DQN|4|3000|210.0|185.0|35.0|
|LP5907SNX-3.2/NOPB|X2SON|DQN|4|3000|184.0|184.0|19.0|
|LP5907SNX-3.3/NOPB|X2SON|DQN|4|3000|184.0|184.0|19.0|
|LP5907SNX-3.3/NOPB|X2SON|DQN|4|3000|210.0|185.0|35.0|
|LP5907SNX-4.0/NOPB|X2SON|DQN|4|3000|184.0|184.0|19.0|
|LP5907SNX-4.0/NOPB|X2SON|DQN|4|3000|210.0|185.0|35.0|
|LP5907SNX-4.5/NOPB|X2SON|DQN|4|3000|184.0|184.0|19.0|
|LP5907SNX-4.5/NOPB|X2SON|DQN|4|3000|210.0|185.0|35.0|
|LP5907SNX1.2NOPBG4|X2SON|DQN|4|3000|210.0|185.0|35.0|
|LP5907SNX1.8NOPBG4|X2SON|DQN|4|3000|210.0|185.0|35.0|
|LP5907SNX2.2NOPBG4|X2SON|DQN|4|3000|210.0|185.0|35.0|
|LP5907SNX2.5NOPBG4|X2SON|DQN|4|3000|210.0|185.0|35.0|
|LP5907SNX2.7NOPBG4|X2SON|DQN|4|3000|210.0|185.0|35.0|
|LP5907SNX2.8NOPBG4|X2SON|DQN|4|3000|210.0|185.0|35.0|
|LP5907SNX2.9NOPBG4|X2SON|DQN|4|3000|210.0|185.0|35.0|
|LP5907SNX3.0NOPBG4|X2SON|DQN|4|3000|184.0|184.0|19.0|
|LP5907SNX3.1NOPBG4|X2SON|DQN|4|3000|210.0|185.0|35.0|
|LP5907SNX3.2NOPBG4|X2SON|DQN|4|3000|210.0|185.0|35.0|
|LP5907SNX3.3NOPBG4|X2SON|DQN|4|3000|210.0|185.0|35.0|
|LP5907SNX4.0NOPBG4|X2SON|DQN|4|3000|210.0|185.0|35.0|
|LP5907SNX4.5NOPBG4|X2SON|DQN|4|3000|210.0|185.0|35.0|
|LP5907UVE-1.2/NOPB|DSBGA|YKE|4|250|208.0|191.0|35.0|
|LP5907UVE-1.8/NOPB|DSBGA|YKE|4|250|208.0|191.0|35.0|
|LP5907UVE-2.8/NOPB|DSBGA|YKE|4|250|208.0|191.0|35.0|
|LP5907UVE-2.85/NOPB|DSBGA|YKE|4|250|208.0|191.0|35.0|
|LP5907UVE-3.0/NOPB|DSBGA|YKE|4|250|208.0|191.0|35.0|
|LP5907UVE-3.1/NOPB|DSBGA|YKE|4|250|208.0|191.0|35.0|
|LP5907UVE-3.2/NOPB|DSBGA|YKE|4|250|208.0|191.0|35.0|
|LP5907UVE-3.3/NOPB|DSBGA|YKE|4|250|208.0|191.0|35.0|
|LP5907UVE-4.5/NOPB|DSBGA|YKE|4|250|208.0|191.0|35.0|
|LP5907UVX-1.2/NOPB|DSBGA|YKE|4|3000|208.0|191.0|35.0|
|LP5907UVX-1.8/NOPB|DSBGA|YKE|4|3000|208.0|191.0|35.0|
|LP5907UVX-2.5/NOPB|DSBGA|YKE|4|3000|208.0|191.0|35.0|
|LP5907UVX-2.8/NOPB|DSBGA|YKE|4|3000|208.0|191.0|35.0|
|LP5907UVX-2.85/NOPB|DSBGA|YKE|4|3000|208.0|191.0|35.0|
|LP5907UVX-3.0/NOPB|DSBGA|YKE|4|3000|208.0|191.0|35.0|
|LP5907UVX-3.1/NOPB|DSBGA|YKE|4|3000|208.0|191.0|35.0|
|LP5907UVX-3.2/NOPB|DSBGA|YKE|4|3000|208.0|191.0|35.0|
|LP5907UVX-3.3/NOPB|DSBGA|YKE|4|3000|208.0|191.0|35.0|
|LP5907UVX-4.5/NOPB|DSBGA|YKE|4|3000|208.0|191.0|35.0|
|LP5907UVX19/NOPB|DSBGA|YKE|4|3000|208.0|191.0|35.0|
|LP5907UVX37/NOPB|DSBGA|YKE|4|3000|208.0|191.0|35.0|

Pack Materials-Page

### PACKAGE MATERIALS INFORMATION

www.ti.com 15-Jul-2026

||Device|Package Type|Package Drawing|Pins|SPQ|Length (mm)|Width (mm)|Height (mm)|
|---|---|---|---|---|---|---|---|---|
|LP5907YKGR-2.8||DSBGA|YKG|4|3000|220.0|220.0|35.0|
|LP5907YKGR-2.825||DSBGA|YKG|4|3000|220.0|220.0|35.0|
|LP5907YKGR-2.85||DSBGA|YKG|4|3000|220.0|220.0|35.0|

Pack Materials-Page

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
4214839/K 08/2024 NOTES:

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

# YKG0004 <u>DSBGA - 0.33mm MAX HEIGHT</u>

||||SCALE 15.000||DIE SIZE BALL GRID ARRAY|
|---|---|---|---|---|---|
|||||A||
|B||E||||
|BUMP A1 CORNER||||D||
|0.33 MAX|||||C SEATING PLANE|
|0.12 0.09|||BUMP||0.05 C|
||B||0.175||D: Max = 0.675 mm, Min = 0.615 mm|
||||||0.175|
|0.35|||||E: Max = 0.675 mm, Min = 0.615 mm|
||A|||||
|0.20 4X 0.16||1|2|||
|0.015 C A B||0.35|||4218366/E 05/2020|

NOTES: ASME Y14.5M. 2. This drawing is subject to change without notice. 1. All linear dimensions are in millimeters. Dimensions in parenthesis are for reference only. Dimensioning and tolerancing per

www.ti.com

## EXAMPLE BOARD LAYOUT

# YKG0004 <u>DSBGA - 0.33mm MAX HEIGHT</u>

|||||||||DIE SIZE BALL GRID ARRAY|
|---|---|---|---|---|---|---|---|---|
|||4X ((0.175) (0.35)|0.18)|SYMM 1 A B|2|||SYMM|
|0.0375 MAX EXPOSED METAL||NON SOLDERMASK DEFINED|(|(0.35) LAND PATTERN EXAMPLE EXPOSED METAL SHOWN SCALE:60X 0.18) METAL SOLDERMASK OPENING SOLDERMASK DETAILS NOT TO SCALE|0.0375 MIN EXPOSED METAL||(0.175)|(0.18) SOLDERMASK OPENING METAL UNDER SOLDER MASK SOLDERMASK DEFINED (PREFERRED) 4218366/E 05/2020|

NOTES: (continued) Refer to Texas Instruments Literature No. SNVA009 (www.ti.com/lit/snva009). 3. Final dimensions may vary due to manufacturing tolerance considerations and also routing constraints.

www.ti.com

## EXAMPLE STENCIL DESIGN

# YKG0004 <u>DSBGA - 0.33mm MAX HEIGHT</u>

||||||||DIE SIZE BALL GRID ARRAY|
|---|---|---|---|---|---|---|---|
||METAL TYP A (0.175)|1||SYMM|2||(R0.05) TYP 4X 0.21) (|
|(0.35)|||||||SYMM|
||B|||(0.35) SOLDERPASTE EXAMPLE BASED ON 0.075 mm THICK STENCIL SCALE:80X|(0.175)||4218366/E 05/2020|

NOTES: (continued) 4. Laser cutting apertures with trapezoidal walls and rounded corners may offer better paste release.

www.ti.com

## PACKAGE OUTLINE

# YKM0004 <u>DSBGA - 0.495 mm max height</u>

|SCALE 12.000||
|---|---|
||A|
|E||
||D BACK COATING|
||C|
|BALL TYP||
|0.35||
|TYP||
||B A|
|1 2||

DIE SIZE BALL GRID ARRAY

B

BALL A1 CORNER

0.495 MAX
SEATING PLANE

0.18
0.14
0.35 TYPD: Max = 0.675 mm, Min = 0.615 mm
E: Max = 0.675 mm, Min = 0.615 mm

0.225
4X

0.195
0.015 C A B
4223494/A 11/2014

NOTES:

1. All linear dimensions are in millimeters. Any dimensions in parenthesis are for reference only. Dimensioning and tolerancing per ASME Y14.5M.
2. This drawing is subject to change without notice.
www.ti.com

## EXAMPLE BOARD LAYOUT

# YKM0004 <u>DSBGA - 0.495 mm max height</u>

|||||DIE SIZE BALL GRID ARRAY|
|---|---|---|---|---|
|4X (||(0.35) TYP 0.18) A SYMM|||
|(0.18) METAL SOLDER MASK OPENING NON-SOLDER MASK DEFINED||(0.35) TYP B 1 2 SYMM LAND PATTERN EXAMPLE EXPOSED METAL SHOWN SCALE:40X 0.04 MAX 0.04 MIN EXPOSED EXPOSED METAL METAL SOLDER MASK DETAILS NOT TO SCALE||METAL UNDER SOLDER MASK (0.18) SOLDER MASK OPENING SOLDER MASK DEFINED (PREFERRED) 4223494/A 11/2014|

NOTES: (continued) Refer to Texas Instruments Literature No. SNVA009 (www.ti.com/lit/snva009). 3. Final dimensions may vary due to manufacturing tolerance considerations and also routing constraints.

www.ti.com

## EXAMPLE STENCIL DESIGN

# YKM0004 <u>DSBGA - 0.495 mm max height</u>

|||DIE SIZE BALL GRID ARRAY|
|---|---|---|
|||(0.35) TYP|
|4X (0.21) A (0.35) TYP B METAL TYP|1|(R0.05) TYP SYMM 2 SYMM SOLDER PASTE EXAMPLE BASED ON 0.075 - 0.1mm THICK STENCIL SCALE:40X 4223494/A 11/2014|

NOTES: (continued) 4. Laser cutting apertures with trapezoidal walls and rounded corners may offer better paste release.

www.ti.com

## PACKAGE OUTLINE

# YKE0004 <u>DSBGA - 0.445mm max height</u>

SCALE 12.000 DIE SIZE BALL GRID ARRAY

B E A

BALL A1 CORNER D

0.445 MAX
C

SEATING PLANE

0.18 BALL TYP
0.14
0.35 TYP B
0.35 TYPD: Max = 0.675 mm, Min = 0.615 mm
A E: Max = 0.675 mm, Min = 0.615 mm

0.225 1 2
4X

0.195
0.005 C A B
4220102/A 11/2014

NOTES:

1. All linear dimensions are in millimeters. Any dimensions in parenthesis are for reference only. Dimensioning and tolerancing per ASME Y14.5M.
2. This drawing is subject to change without notice.
www.ti.com

## EXAMPLE BOARD LAYOUT

# YKE0004 <u>DSBGA - 0.445mm max height</u>

||||||||DIE SIZE BALL GRID ARRAY|
|---|---|---|---|---|---|---|---|
|4X 0.18||0.02 A (0.35) TYP|||(0.35) TYP SYMM|||
|(0.18) METAL SOLDER MASK OPENING NON-SOLDER MASK DEFINED (PREFERRED)||B 1 0.04 MAX|SYMM LAND PATTERN EXAMPLE SCALE:40X|2 SOLDER MASK DETAILS NOT TO SCALE|0.04 MIN||METAL UNDER SOLDER MASK (0.18) SOLDER MASK OPENING SOLDER MASK DEFINED 4220102/A 11/2014|

NOTES: (continued) Refer to Texas Instruments Literature No. SNVA009 (www.ti.com/lit/snva009). 3. Final dimensions may vary due to manufacturing tolerance considerations and also routing constraints.

www.ti.com

## EXAMPLE STENCIL DESIGN

# YKE0004 <u>DSBGA - 0.445mm max height</u>

||||||DIE SIZE BALL GRID ARRAY|
|---|---|---|---|---|---|
||||||(0.35) TYP|
|4X (0.21) A|||||(R) TYP0.05|
|(0.35)|||||SYMM|
|TYP B||||||
|METAL TYP|1||SYMM SOLDER PASTE EXAMPLE BASED ON 0.075 - 0.1mm THICK STENCIL SCALE:40X|2|4220102/A 11/2014|

NOTES: (continued) 4. Laser cutting apertures with trapezoidal walls and rounded corners may offer better paste release.

www.ti.com

### PACKAGE OUTLINE DQN0004A X2SON - 0.4 mm max height

PLASTIC SMALL OUTLINE-NO LEAD

||||1.05||A|||||
|---|---|---|---|---|---|---|---|---|---|
||B||0.95|||||||
|PIN 1 INDEX AREA|1||||1.05 0.95|||||
||0.4 MAX|NOTE 6 (0.05) TYP|||0.48+0.12 -0.1|C SEATING PLANE 0.08 0.05 0.00||||
|2X 0.65|2||5||3 (0.07) TYP|EXPOSED THERMAL PAD NOTE 5|||NOTE 6|
||1||||4|||||
|PIN 1 ID (OPTIONAL)||||||4X 0.28 0.15||(0.11)||
|NOTE 4|||0.3 0.2 3X 0.30 0.15|||0.1 C A B 0.05 C|||4215302/E 12/2016|

NOTES:

1. All linear dimensions are in millimeters. Any dimensions in parenthesis are for reference only. Dimensioning and tolerancing per ASME Y14.5M.
2. This drawing is subject to change without notice.
3. The package thermal pad must be soldered to the printed circuit board for optimal thermal and mechanical performance.
4. Features may not exist. Recommend use of pin 1 marking on top of package for orientation purposes.
5. Shape of exposed side leads may differ.
6. Number and location of exposed tie bars may vary.
**www.ti.com**

### EXAMPLE BOARD LAYOUT DQN0004A X2SON - 0.4 mm max height

PLASTIC SMALL OUTLINE-NO LEAD

(0.86)

SYMM

4X (0.36) 4X SEE DETAIL (0.03)

4 4X (0.21) 1

SYMM 5 (0.65)

4X (0.18)

( 0.48) (0.22) TYP EXPOSED METAL CLEARANCE

##### LAND PATTERN EXAMPLE

SCALE: 40X

0.05 MIN
ALL AROUND SOLDER MASK EXPOSED METAL OPENING

METAL UNDER SOLDER MASK

SOLDER MASK DEFINED

##### SOLDER MASK DETAIL

4215302/E 12/2016

NOTES: (continued)

7. This package is designed to be soldered to a thermal pad on the board. For more information, see Texas Instruments literature number SLUA271 (www.ti.com/lit/slua271).
8. If any vias are implemented, it is recommended that vias under paste be filled, plugged or tented.
**www.ti.com**

### EXAMPLE STENCIL DESIGN DQN0004A X2SON - 0.4 mm max height

PLASTIC SMALL OUTLINE-NO LEAD

(0.9)

SYMM

4X (0.4) 4X (0.03)

4 1 4X (0.21)

5 SYMM (0.65)

SOLDER MASK 4X (0.22) EDGE

2 3

( 0.45) 4X (0.235)

##### SOLDER PASTE EXAMPLE

BASED ON 0.075 - 0.1mm THICK STENCIL

EXPOSED PAD 88% PRINTED SOLDER COVERAGE BY AREA SCALE: 60X

4215302/E 12/2016

NOTES: (continued)

9. Laser cutting apertures with trapezoidal walls and rounded corners may offer better paste release. IPC-7525 may have alternate design recommendations.
**www.ti.com**

#### IMPORTANT NOTICE AND DISCLAIMER

TI PROVIDES TECHNICAL AND RELIABILITY DATA (INCLUDING DATASHEETS), DESIGN RESOURCES (INCLUDING REFERENCE DESIGNS), APPLICATION OR OTHER DESIGN ADVICE, WEB TOOLS, SAFETY INFORMATION, AND OTHER RESOURCES “AS IS” AND WITH ALL FAULTS, AND DISCLAIMS ALL WARRANTIES, EXPRESS AND IMPLIED, INCLUDING WITHOUT LIMITATION ANY IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE OR NON-INFRINGEMENT OF THIRD PARTY INTELLECTUAL PROPERTY RIGHTS. These resources are intended for skilled developers designing with TI products. You are solely responsible for (1) selecting the appropriate TI products for your application, (2) designing, validating and testing your application, and (3) ensuring your application meets applicable standards, and any other safety, security, regulatory or other requirements. These resources are subject to change without notice. TI grants you permission to use these resources only for development of an application that uses the TI products described in the resource. Other reproduction and display of these resources is prohibited. No license is granted to any other TI intellectual property right or to any third party intellectual property right. TI disclaims responsibility for, and you fully indemnify TI and its representatives against any claims, damages, costs, losses, and liabilities arising out of your use of these resources. TI’s products are provided subject to TI’s Terms of Sale, TI’s General Quality Guidelines, or other applicable terms available either on ti.com or provided in conjunction with such TI products. TI’s provision of these resources does not expand or otherwise alter TI’s applicable warranties or warranty disclaimers for TI products. Unless TI explicitly designates a product as custom or customer-specified, TI products are standard, catalog, general purpose devices. TI objects to and rejects any additional or different terms you may propose. IMPORTANT NOTICE

Copyright © 2026, Texas Instruments Incorporated Last updated 10/2025
