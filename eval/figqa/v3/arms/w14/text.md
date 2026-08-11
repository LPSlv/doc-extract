**LM386** SNAS545D – MAY 2004 – REVISED AUGUST 2023

|3 Description designed for the gain to any value from 20 to 200.|The LM386M-1 and LM386MX-1 are power amplifiers use in low applications. The gain is internally set to 20 to keep external part count low, but the addition of an external resistor and capacitor between pins 1 and 8 increases The inputs are ground referenced while the output automatically biases to one-half the supply voltage. The quiescent power drain is only 24 mW when operating from a 6-V supply, making the LM386M-1 and LM386MX-1 prefered for battery operation. Device Information|voltage consumer (1)|
|---|---|---|
|PART NUMBER|PACKAGE|BODY SIZE (NOM)|
|LM386N-1|PDIP (8)|9.60 mm × 6.35 mm|
|LM386N-3|PDIP (8)|9.60 mm × 6.35 mm|
|LM386N-4|PDIP (8)|9.60 mm × 6.35 mm|
|LM386M-1|SOIC (8)|4.90 mm × 3.90 mm|
|LM386MX-1|SOIC (8)|4.90 mm × 3.90 mm|
|LM386MMX-1|VSSOP (8)|3.00 mm × 3.00 mm|

(1) the end of the data sheet. 1 1.35 k 2 - INPUT For all available packages, see the orderable addendum at 7 BYPASS 15 k 3 50 k 50 k + INPUT

## LM386 Low Voltage Audio Power Amplifier

#### 1 Features

- Battery Operation
- Minimum External Parts
- Wide Supply Voltage Range: 4 V–12 V or 5 V–18 V
- Low Quiescent Current Drain: 4 mA
- Voltage Gains from 20 to 200
- Ground-Referenced Input
- Self-Centering Output Quiescent Voltage
- Low Distortion: 0.2% (AV = 20, VS = 6 V, RL = 8 Ω, PO = 125 mW, f = 1 kHz)
- Available in 8-Pin MSOP Package
#### 2 Applications

- AM-FM Radio Amplifiers
- Portable Tape Player Amplifiers
- Intercoms
- TV Sound Systems
- Line Drivers
- Ultrasonic Drivers
- Small Servo Drivers
- Power Converters
6 V S

5 V OUT

4 GND

15 k

GAIN 15 k GAIN 8

##### Schematic

intellectual property matters and other important disclaimers. PRODUCTION DATA. An IMPORTANT NOTICE at the end of this data sheet addresses availability, warranty, changes, use in safety-critical applications,

**LM386** SNAS545D – MAY 2004 – REVISED AUGUST 2023 <u>www.ti.com</u>

||Table of Contents 1 Features ............................................................................1 8.3 Feature Description.....................................................9 2 Applications ..................................................................... 1 8.4 Device Functional Modes............................................9 3 Description .......................................................................1 9 Application and Implementation .................................. 10 4 Revision History .............................................................. 2 9.1 Application Information............................................. 10 5 Pin Configuration and Functions ................................... 3 9.2 Typical Application.................................................... 10 6 Specifications .................................................................. 4 10 Power Supply Recommendations ..............................17 6.1 Absolute Maximum Ratings........................................ 4 11 Layout ........................................................................... 18 6.2 ESD Ratings............................................................... 4 11.1 Layout Guidelines................................................... 18 6.3 Recommended Operating Conditions.........................4 11.2 Layout Examples.....................................................18 6.4 Thermal Information....................................................4 12 Device and Documentation Support ..........................20 6.5 Electrical Characteristics.............................................5 12.1 Device Support....................................................... 20 6.6 Typical Characteristics................................................ 6 12.2 Documentation Support.......................................... 20 7 Parameter Measurement Information ............................ 8 12.3 Receiving Notification of Documentation Updates..20 8 Detailed Description ........................................................9 12.4 Community Resources............................................20 8.1 Overview..................................................................... 9 12.5 Trademarks............................................................. 20 8.2 Functional Block Diagram........................................... 9|
|---|---|
||4 Revision History NOTE: Page numbers for previous revisions may differ from page numbers in the current version. Changes from Revision C (May 2017) to Revision D (August 2023) Page|
|•|Updated Typical Output Power Spec..................................................................................................................5 Changes from Revision B (March 2017) to Revision C (May 2017) Page|
|• • • • • • • • • • • • • • • • • •|Changed devices LM386M-1/LM386MX-1 To: LM386 in the data sheet title..................................................... 1 Updated the numbering format for tables, figures, and cross-references throughout the document................. 1 Changed From: LM386N-4 To: Speaker Impedance in the Recommended Operating Conditions table........... 4 Changed From: 5 Ω to 12 Ω To: 5 V to 12 V for Supply Voltage in Table 9-1 .................................................. 10 Changed kW To: kΩ in the Gain Control section.............................................................................................. 10 Changed kW To: kΩ in the Input Biasing section.............................................................................................. 11 Changed Figure 9-2 ......................................................................................................................................... 11 Changed From: 5 Ω to 12 Ω To: 5 V to 12 V for Supply Voltage in Table 9-2 .................................................. 12 Changed Figure 9-4 .........................................................................................................................................12 Changed From: 5 Ω to 12 Ω To: 5 V to 12 V for Supply Voltage in Table 9-3 .................................................. 13 Changed Figure 9-6 .........................................................................................................................................13 Changed From: 5 Ω to 12 Ω To: 5 V to 12 V for Supply Voltage in Table 9-4 .................................................. 14 Changed Figure 9-8 .........................................................................................................................................14 Changed From: 5 Ω to 12 Ω To: 5 V to 12 V for Supply Voltage in Table 9-5 .................................................. 15 Changed From: 5 Ω to 12 Ω To: 5 V to 12 V for Supply Voltage in Table 9-6 .................................................. 16 Changed Figure 9-12 .......................................................................................................................................16 Changed From: 5 Ω to 12 Ω To: 5 V to 12 V for Supply Voltage in Table 9-7 .................................................. 17 Changed Figure 9-14 .......................................................................................................................................17 Changes from Revision A (May 2004) to Revision B (March 2017) Page|
|• • •|Added LM386MX-1 device to the data sheet. ................................................................................................... 1 Added Device Information, Application and Implementation, Power Supply Recommendation, Layout, and Device and Documentation Support sections.....................................................................................................1 Inserted Functional Block Diagram.....................................................................................................................9|

*Submit Document Feedback* Copyright © 2023 Texas Instruments Incorporated

Product Folder Links: *LM386*

GAIN BYPASS**LM386** **www.ti.com** SNAS545D – MAY 2004 – REVISED AUGUST 2023

||5 Pin Configuration and Functions|
|---|---|
|PIN||
|NAME|NO.|
|GAIN|1|
|–INPUT|2|
|+INPUT|3|
|GND|4|
|V OUT|5|
|V S|6|
|BYPASS|7|
|GAIN|8|

(1) I = Input, O = Output, P = Power

|- INPUT||7|V|
|---|---|---|---|
|GAIN|+ INPUT 1|6|V|
||2|||

S

OUT

GND

**Figure 5-1. D Package 8-Pin MSOP Top View**

||Table 5-1. Pin Functions|
|---|---|
|TYPE|DESCRIPTION|

(1)

– Gain setting pin I Inverting input I Noninverting input P Ground reference O Output P Power supply voltage O Bypass decoupling path – Gain setting pin

Copyright © 2023 Texas Instruments Incorporated *Submit Document Feedback*

**LM386**

#### 6 Specifications

##### 6.1 Absolute Maximum Ratings

(1)
over operating free-air temperature range (unless otherwise noted) **MIN MAX UNIT** LM386N-1/-3, LM386M-1 15 Supply Voltage, VCCV LM386N-4 22 LM386N 1.25 Package Dissipation LM386M 0.73 W LM386MM-1 0.595 Input Voltage, VI–0.4 0.4 V Storage temperature, Tstg–65 150 °C

(1) Stresses beyond those listed under *Absolute Maximum Ratings* may cause permanent damage to the device. These are stress ratings only, which do not imply functional operation of the device at these or any other conditions beyond those indicated under *Recommended Operating Conditions*. Exposure to absolute-maximum-rated conditions for extended periods may affect device reliability.
##### 6.2 ESD Ratings

||||VALUE|UNIT|
|---|---|---|---|---|
|||Human-body model (HBM), per ANSI/ESDA/JEDEC JS-001|±1000||
|V(ESD)|Electrostatic discharge|Charged-device model (CDM), per JEDEC specification JESD22- C101(2)|±1000|V|

(1) JEDEC document JEP155 states that 500-V HBM allows safe manufacturing with a standard ESD control process.
(2) JEDEC document JEP157 states that 250-V CDM allows safe manufacturing with a standard ESD control process.

(1)
##### 6.3 Recommended Operating Conditions

over operating free-air temperature range (unless otherwise noted) **MIN NOM MAX UNIT**

|||MIN|MAX|UNIT|
|---|---|---|---|---|
||Supply Voltage|4|12|V|
|VCC|LM386N-4|5|18|V|
||Speaker Impedance|4||Ω|
|VI|Analog input voltage|–0.4|0.4|V|
|TA|Operating free-air temperature|0|70|°C|

##### 6.4 Thermal Information

||D (SOIC)|DGK (VSSOP)|P (PDIP)||
|---|---|---|---|---|
||8|8|8||

(1) THERMAL METRIC LM386 LM386 LM386 UNIT

|RθJA|Junction-to-ambient thermal resistance|115.7|169.3|53.4|°C/W|
|---|---|---|---|---|---|
|RθJC(top)|Junction-to-case (top) thermal resistance|59.7|73.1|42.1|°C/W|
|RθJB|Junction-to-board thermal resistance|56.2|100.2|30.6|°C/W|
|ψJT|Junction-to-top characterization parameter|12.4|9.2|19.0|°C/W|
|ψJB report.|Junction-to-board characterization parameter|55.6|99.1|50.5|°C/W|

(1) For more information about traditional and new thermal metrics, see the Semiconductor and IC Package Thermal Metrics application

**LM386**

##### 6.5 Electrical Characteristics

|over operating free-air temperature range (unless otherwise noted)||
|---|---|
|PARAMETER TEST CONDITIONS MIN TYP|MAX UNIT|

LM386N-1, -3, LM386M-1, LM386MM-1 4 12 VSOperating Supply Voltage V LM386N-4 5 18 IQQuiescent Current VS = 6 V, VIN = 0 4 8 mA VS = 6 V, RL = 8 Ω, THD = 10% 250 325 (LM386N-1, LM386M-1, LM386MM-1) VS = 9 V, RL = 8 Ω, THD = 10% POUTOutput Power 500 700 mW (LM386N-3) VS = 16 V, RL = 32 Ω, THD = 10% 700 1000 (LM386N-4) VS = 6 V, f = 1 kHz 26 AVVoltage Gain dB 10 µF from Pin 1 to 8 46 BW Bandwidth VS = 6 V, Pins 1 and 8 Open 300 kHz VS = 6 V, RL = 8 Ω, POUT = 125 mW THD Total Harmonic Distortion 0.2% f = 1 kHz, Pins 1 and 8 Open VS = 6 V, f = 1 kHz, CBYPASS = 10 μF PSRR Power Supply Rejection Ratio 50 dB Pins 1 and 8 Open, Referred to Output RINInput Resistance 50 kΩ IBIASInput Bias Current VS = 6 V, Pins 2 and 3 Open 250 nA

**LM386**

##### 6.6 Typical Characteristics

|Figure 6-1. Supply Current vs Supply Voltage|Figure 6-2. Power Supply Rejection vs Frequency|
|---|---|
||Figure 6-4. Voltage Gain vs Frequency|
|Figure 6-3. Output Voltage vs Supply Voltage||
|Figure 6-5. Total Harmonic Distortion vs Frequency|Figure 6-6. Total Harmonic Distortion vs Power Out|
|Figure 6-7. Device Dissipation vs Output Power|Figure 6-8. Device Dissipation vs Output Power|

**LM386**

**Figure 6-9. Device Dissipation vs Output Power**

**LM386**

#### 7 Parameter Measurement Information

All parameters are measured according to the conditions described in the *Section 6* section.

**LM386**

#### 8 Detailed Description

##### 8.1 Overview

The LM386 is a mono low voltage amplifier that can be used in a variety of applications. It can drive loads from 4 Ω to 32 Ω. The gain is internally set to 20 but it can be modified from 20 to 200 by placing a resistor and capacitor between pins 1 and 8. This device comes in three different 8-pin packages as PDIP, SOIC and VSSOP to fit in different applications.

##### 8.2 Functional Block Diagram

### Gain Circuitry

- +
### Bias Circuitry

### Bypass

##### 8.3 Feature Description

There is an internal 1.35-KΩ resistor that sets the gain of this device to 20. The gain can be modified from 20 to

200. Detailed information about gain setting can be found in the *Section 9.2.2.2* section.
##### 8.4 Device Functional Modes

As this is an Op Amp it can be used in different configurations to fit in several applications. The internal gain setting resistor allows the LM386 to be used in a very low part count system. In addition a series resistor can be placed between pins 1 and 5 to modify the gain and frequency response for specific applications.

**LM386**

||9 Application and Implementation||
|---|---|---|
||Note Information in the following applications sections is not part of the TI component specification, and TI does not warrant its accuracy or completeness. TI’s customers are responsible for determining suitability of components for their purposes. Customers should validate and test their design implementation to confirm system functionality. 9.1 Application Information Below are shown different setups that show how the LM386 can be implemented in a variety of applications. 9.2 Typical Application 9.2.1 LM386 with Gain = 20 Figure 9-1 shows the minimum part count application that can be implemented using LM386. Its gain is internally set to 20. 6 2 V IN 3 10 k Figure 9-1. LM386 with Gain = 20 9.2.1.1 Design Requirements Table 9-1. Design Parameters|V S - 1 250 µF 8 + LM386 5 7 0.05 µF + 4 10 Copyright © 2017, Texas Instruments Incorporated|
||DESIGN PARAMETER|EXAMPLE VALUE|
||Load Impedance|4 Ω to 32 Ω|
||Supply Voltage 9.2.1.2 Detailed Design Procedure 9.2.1.2.1 Gain Control To make the LM386 a more versatile amplifier, two pins (1 and 8) are provided for gain control. With pins 1 and 8 open the 1.35-kΩ resistor sets the gain at 20 (26 dB). If a capacitor is put from pin 1 to 8, bypassing the 1.35-kΩ resistor, the gain will go up to 200 (46 dB). If a resistor is placed in series with the capacitor, the gain can be set to any value from 20 to 200. Gain control can also be done by capacitively coupling a resistor (or FET) from pin 1 to ground. Additional external components can be placed in parallel with the internal feedback resistors to tailor the gain and frequency response for individual applications. For example, we can compensate poor speaker bass response by frequency shaping the feedback path. This is done with a series RC from pin 1 to 5 (paralleling the internal 15-kΩ resistor). For 6 dB effective bass boost: R ~= 15 kΩ, the lowest value for good stable operation is R = 10 kΩ if pin 8 is open. If pins 1 and 8 are bypassed then R as low as 2 kΩ can be used. This restriction is because the amplifier is only compensated for closed-loop gains greater than 9.|5 V to 12 V|

**LM386**

**9.2.1.2.2 Input Biasing** The schematic shows that both inputs are biased to ground with a 50 kΩ resistor. The base current of the input transistors is about 250 nA, so the inputs are at about 12.5 mV when left open. If the dc source resistance driving the LM386 is higher than 250 kΩ it will contribute very little additional offset (about 2.5 mV at the input, 50 mV at the output). If the dc source resistance is less than 10 kΩ, then shorting the unused input to ground will keep the offset low (about 2.5 mV at the input, 50 mV at the output). For dc source resistances between these values we can eliminate excess offset by putting a resistor from the unused input to ground, equal in value to the dc source resistance. Of course all offset problems are eliminated if the input is capacitively coupled. When using the LM386 with higher gains (bypassing the 1.35 kΩ resistor between pins 1 and 8) it is necessary to bypass the unused input, preventing degradation of gain and possible instabilities. This is done with a 0.1 μF capacitor or a short to ground depending on the dc source resistance on the driven input.
##### 9.2.1.3 Application Curve

**Figure 9-2. Supply Current vs Supply Voltage**

**LM386**

||9.2.2 LM386 with Gain = 200 S + 6 2 V IN 3 10 k Figure 9-3. LM386 with Gain = 200 9.2.2.1 Design Requirements Table 9-2. Design Parameters|V 10 µF - 1 250 µF 8 + LM386 5 7 0.05 µF + 4 BYPASS 10 Copyright © 2017, Texas Instruments Incorporated|
|---|---|---|
||DESIGN PARAMETER|EXAMPLE VALUE|
||Load Impedance|4 Ω to 32 Ω|
||Supply Voltage 9.2.2.2 Detailed Design Procedure The Detailed Design Procedure can be found in the 9.2.2.3 Application Curve Figure 9-4. Supply Current vs Supply Voltage|5 V to 12 V Section 9.2.1.2 section.|

**LM386**

|9.2.3 LM386 with Gain = 50 V S 1.2 k 6 2 V IN 3 10 k Figure 9-5. LM386 with Gain = 50 9.2.3.1 Design Requirements Table 9-3. Design Parameters|10 µF - 1 250 µF 8 + LM386 5 7 10 + 4 BYPASS 0.05 µF Copyright © 2017, Texas Instruments Incorporated||
|---|---|---|
|DESIGN PARAMETER|EXAMPLE VALUE||
|Load Impedance|4 Ω to 32 Ω||
|Supply Voltage|5 V to 12 V||
|9.2.3.2 Detailed Design Procedure The Detailed Design Procedure can be found in the 9.2.3.3 Application Curve Figure 9-6. Supply Current vs Supply Voltage|Section 9.2.1.2 section.||

**LM386**

||9.2.4 Low Distortion Power Wienbridge Oscillator V 10 µF S + 6 2 ELDEMA 3 3 V ± 15mA 7 Figure 9-7. Low Distortion Power Wienbridge Oscillator 9.2.4.1 Design Requirements Table 9-4. Design Parameters|390 - 1 50 µF 8 V+ LM386 O CF-S-2158 5 4 R L + 0.05 µF 0.01 µF BYPASS 10 47 k f = 1 kHz 0.01 µF 4.7 k Copyright © 2017, Texas Instruments Incorporated|
|---|---|---|
||DESIGN PARAMETER|EXAMPLE VALUE|
||Load Impedance|4 Ω to 32 Ω|
||Supply Voltage 9.2.4.2 Detailed Design Procedure The Detailed Design Procedure can be found in the 9.2.4.3 Application Curve Figure 9-8. Supply Current vs Supply Voltage|5 V to 12 V Section 9.2.1.2 section.|

**LM386**

|9.2.5 LM386 with Bass Boost 6 2 7 V IN 3 8 10 k 4 Figure 9-9. LM386 with Bass Boost 9.2.5.1 Design Requirements Table 9-5. Design Parameters|V S BYPASS- 250 µF + V O LM386 5 1 R L +0.033 µF 0.05 µF 10 k 10 Ÿ Copyright © 2017, Texas Instruments Incorporated||
|---|---|---|
|DESIGN PARAMETER|EXAMPLE VALUE||
|Load Impedance|4 Ω to 32 Ω||
|Supply Voltage|5 V to 12 V||
|9.2.5.2 Detailed Design Procedure The Detailed Design Procedure can be found in the 9.2.5.3 Application Curve Figure 9-10. Voltage Gain vs Frequency|Section 9.2.1.2 section.||

**LM386**

||9.2.6 Square Wave Oscillator V S 6 2 0.1 µF 3 1 k Figure 9-11. Square Wave Oscillator Table 9-6. Design Parameters|30 k - 1 50 µF 8 + V O LM3865 R L 4 + 10 k f = 1 kHz Copyright © 2017, Texas Instruments Incorporated|
|---|---|---|
||DESIGN PARAMETER|EXAMPLE VALUE|
||Load Impedance|4 Ω to 32 Ω|
||Supply Voltage 9.2.6.1 Detailed Design Procedure The Detailed Design Procedure can be found in the 9.2.6.2 Application Curve Figure 9-12. Supply Current vs Supply Voltage|5 V to 12 V Section 9.2.1.2 section.|

**LM386**

|9.2.7 AM Radio Power Amplifier V S C C R1 6 2 V10 k OL 10 k 3 + 4 Figure 9-13. AM Radio Power Amplifier 9.2.7.1 Design Requirements Table 9-7. Design Parameters|0.05 µF 10 µF FROM DETECTOR + BYPASS 1 - C12200 pF 8 5 7 LM386 + 10 µF||
|---|---|---|
|DESIGN PARAMETER|EXAMPLE VALUE||
|Load Impedance|4 Ω to 32 Ω||
|Supply Voltage|5 V to 12 V||
|9.2.7.2 Detailed Design Procedure The Detailed Design Procedure can be found in the 9.2.7.3 Application Curve Figure 9-14. Supply Current vs Supply Voltage 10 Power Supply Recommendations The LM386 is specified for operation up to 12 V or 18 V. The power supply should be well regulated and the voltage must be within the specified values. It is recommended to place a capacitor to GND close to the LM386 power supply pin.|Section 9.2.1.2 section.||

**LM386**

#### 11 Layout

##### 11.1 Layout Guidelines

Place all required components as close as possible to the device. Use short traces for the output to the speaker connection. Route the analog traces far from the digital signal traces and avoid crossing them.

##### 11.2 Layout Examples

250uF OUTPUT

0.05uF
10 LM386

INPUT

Connection to ground plane Connection to power 5V

Top layer ground plane Top layer traces

**Figure 11-1. Layout Example for Minimum Parts Gain = 20 dB on PDIP package**

250uF OUTPUT

0.05uF
LM386 10

INPUT

Connection to ground plane Connection to power 5V

Top layer ground plane Top layer traces

**Figure 11-2. Layout Example for Minimum Parts Gain = 20 dB on SOIC package**

**LM386**

250uF OUTPUT

0.05uF
LM386 10

INPUT

Connection to ground plane Connection to power 5V

Top layer ground plane Top layer traces

**Figure 11-3. Layout Example for Minimum Parts Gain = 20 dB on VSSOP package**

**LM386**

#### 12 Device and Documentation Support

##### 12.1 Device Support

##### 12.1.1 Development Support

##### 12.2 Documentation Support

##### 12.3 Receiving Notification of Documentation Updates

To receive notification of documentation updates — go to the product folder for your device on ti.com. In the upper right-hand corner, click the *Alert me* button to register and receive a weekly digest of product information that has changed (if any). For change details, check the revision history of any revised document.

##### 12.4 Community Resources 12.5 Trademarks

All trademarks are the property of their respective owners.

**LM386**

#### Mechanical, Packaging, and Orderable Information

The following pages include mechanical, packaging, and orderable information. This information is the most current data available for the designated devices. This data is subject to change without notice and revision of this document. For browser-based versions of this data sheet, refer to the left-hand navigation.

### PACKAGE OPTION ADDENDUM

www.ti.com 9-Nov-2025

##### PACKAGING INFORMATION

**Orderable part number**

|Status (1)|Material type (2)|Package | Pins|Package qty | Carrier||RoHS (3)|Lead finish/ Ball material (4)|MSL rating/ Peak reflow (5)|Op temp (°C)|Part marking (6)|
|---|---|---|---|---|---|---|---|---|---|
|Active|Production|SOIC (D) | 8||95 | TUBE|Yes|SN|Level-1-260C-UNLIM|0 to 70|LM386 M-1|
|Active|Production|SOIC (D) | 8||95 | TUBE|Yes|SN|Level-1-260C-UNLIM|0 to 70|LM386 M-1|
|Active|Production|VSSOP (DGK) | 8|3500 | LARGE T&R||Yes|SN|Level-1-260C-UNLIM|0 to 70|Z86|
|Active|Production|VSSOP (DGK) | 8|3500 | LARGE T&R||Yes|SN|Level-1-260C-UNLIM|0 to 70|Z86|
|Active|Production|SOIC (D) | 8|2500 | LARGE T&R||Yes|SN|Level-1-260C-UNLIM|0 to 70|LM386 M-1|
|Active|Production|SOIC (D) | 8|2500 | LARGE T&R||Yes|SN|Level-1-260C-UNLIM|0 to 70|LM386 M-1|
|Active|Production|PDIP (P) | 8||40 | TUBE|Yes|NIPDAU|Level-1-NA-UNLIM|0 to 70|LM 386N-1|
|Active|Production|PDIP (P) | 8||40 | TUBE|Yes|NIPDAU|Level-1-NA-UNLIM|0 to 70|LM 386N-1|
|Active|Production|PDIP (P) | 8||40 | TUBE|Yes|NIPDAU|Level-1-NA-UNLIM|0 to 70|LM 386N-3|
|Active|Production|PDIP (P) | 8||40 | TUBE|Yes|NIPDAU|Level-1-NA-UNLIM|0 to 70|LM 386N-3|
|Active|Production|PDIP (P) | 8||40 | TUBE|Yes|NIPDAU|Level-1-NA-UNLIM|0 to 70|LM 386N-3|
|Active|Production|PDIP (P) | 8||40 | TUBE|Yes|NIPDAU|Level-1-NA-UNLIM|0 to 70|LM 386N-3|
|Active|Production|PDIP (P) | 8||40 | TUBE|Yes|NIPDAU|Level-1-NA-UNLIM|0 to 70|LM 386N-4|
|Active|Production|PDIP (P) | 8||40 | TUBE|Yes|NIPDAU|Level-1-NA-UNLIM|0 to 70|LM 386N-4|
|Active|Production|PDIP (P) | 8||40 | TUBE|Yes|NIPDAU|Level-1-NA-UNLIM|0 to 70|LM 386N-4|
|Active|Production|PDIP (P) | 8||40 | TUBE|Yes|NIPDAU|Level-1-NA-UNLIM|0 to 70|LM 386N-4|

LM386M-1/NOPB

LM386M-1/NOPB.B

LM386MMX-1/NOPB LM386MMX-1/NOPB.B LM386MX-1/NOPB

LM386MX-1/NOPB.B

LM386N-1/NOPB

LM386N-1/NOPB.B

LM386N-3/NOPB

LM386N-3/NOPB.B

LM386N-3/NOPBG4

LM386N-3/NOPBG4.B

LM386N-4/NOPB

LM386N-4/NOPB.B

LM386N-4/NOPBG4

LM386N-4/NOPBG4.B

**(1)** **Status:** For more details on status, see our
product life cycle.

Addendum-Page

### PACKAGE OPTION ADDENDUM

www.ti.com 9-Nov-2025

**(2)** **Material type:** When designated, preproduction parts are prototypes/experimental devices, and are not yet approved or released for full production. Testing and final process, including without limitation quality assurance, reliability performance testing, and/or process qualification, may not yet be complete, and this item is subject to further changes or possible discontinuation. If available for ordering, purchases will be subject to an additional waiver at checkout, and are intended for early internal evaluation purposes only. These items are sold without warranties of any kind.
**(3)** **RoHS values:** Yes, No, RoHS Exempt. See the TI RoHS Statement for additional information and value definition.
**(4)** **Lead finish/Ball material:** Parts may have multiple material finish options. Finish options are separated by a vertical ruled line. Lead finish/Ball material values may wrap to two lines if the finish value exceeds the maximum column width.
**(5)** **MSL rating/Peak reflow:** The moisture sensitivity level ratings and peak solder (reflow) temperatures. In the event that a part has multiple moisture sensitivity ratings, only the lowest level per JEDEC standards is shown. Refer to the shipping label for the actual reflow temperature that will be used to mount the part to the printed circuit board.
**(6)** **Part marking:** There may be an additional marking, which relates to the logo, the lot trace code information, or the environmental category of the part. Multiple part markings will be inside parentheses. Only one part marking contained in parentheses and separated by a "~" will appear on a part. If a line is indented then it is a continuation of the previous line and the two combined represent the entire part marking for that device. **Important Information and Disclaimer:** The information provided on this page represents TI's knowledge and belief as of the date that it is provided. TI bases its knowledge and belief on information provided by third parties, and makes no representation or warranty as to the accuracy of such information. Efforts are underway to better integrate information from third parties. TI has taken and continues to take reasonable steps to provide representative and accurate information but may not have conducted destructive testing or chemical analysis on incoming materials and chemicals. TI and TI suppliers consider certain information to be proprietary, and thus CAS numbers and other limited information may not be available for release. In no event shall TI's liability arising out of such information exceed the total purchase price of the TI part(s) at issue in this document sold by TI to Customer on an annual basis.
Addendum-Page

### PACKAGE MATERIALS INFORMATION

www.ti.com 15-Jul-2025

##### TAPE AND REEL INFORMATION

**REEL DIMENSIONS TAPE DIMENSIONS** K0 P1

W B0 Reel Diameter Cavity A0 A0 Dimension designed to accommodate the component width B0 Dimension designed to accommodate the component length K0 Dimension designed to accommodate the component thickness W Overall width of the carrier tape P1 Pitch between successive cavity centers

Reel Width (W1) **QUADRANT ASSIGNMENTS FOR PIN 1 ORIENTATION IN TAPE** Sprocket Holes

||Q1 Q2|Q1|Q2|||
|---|---|---|---|---|---|
||Q3 Q4|Q3|Q4|User Direction of Feed||

Pocket Quadrants

*All dimensions are nominal **Device Package Package Pins SPQ Reel Reel A0 B0 K0 P1 W Pin1** **Type Drawing Diameter Width (mm) (mm) (mm) (mm) (mm) Quadrant** **(mm) W1 (mm)**

|LM386MMX-1/NOPB||VSSOP|DGK|8 3500|330.0|12.4|5.3|3.4|1.4|8.0|12.0|Q1|
|---|---|---|---|---|---|---|---|---|---|---|---|---|
|LM386MX-1/NOPB||SOIC|D|8 2500|330.0|12.4|6.5|5.4|2.0|8.0|12.0|Q1|

LM386MMX-1/NOPB VSSOP DGK 8 3500 330.0 12.4 5.3 3.4 1.4 8.0 12.0 Q1

Pack Materials-Page

### PACKAGE MATERIALS INFORMATION

www.ti.com 15-Jul-2025

**TAPE AND REEL BOX DIMENSIONS**

***Width (mm)*** H

W L

*All dimensions are nominal **Device Package Type Package Drawing Pins SPQ Length (mm) Width (mm) Height (mm)**

||Device|Package Type|Package Drawing|Pins|SPQ|Length (mm)|Width (mm)|Height (mm)|
|---|---|---|---|---|---|---|---|---|
|LM386MMX-1/NOPB||VSSOP|DGK|8|3500|367.0|367.0|35.0|
|LM386MX-1/NOPB||SOIC|D|8|2500|367.0|367.0|35.0|

Pack Materials-Page

### PACKAGE MATERIALS INFORMATION

www.ti.com 15-Jul-2025

##### TUBE

##### T-Tube height L-Tube length

##### W-Tube width

##### B-Alignment groove width

*All dimensions are nominal

|Device||Package Type|Pins|SPQ|L (mm)|W (mm)|T (µm)|B (mm)|
|---|---|---|---|---|---|---|---|---|
|LM386M-1/NOPB|D|SOIC|8|95|495|8|4064|3.05|
|LM386M-1/NOPB.B|D|SOIC|8|95|495|8|4064|3.05|
|LM386N-1/NOPB|P|PDIP|8|40|502|14|11938|4.32|
|LM386N-1/NOPB.B|P|PDIP|8|40|502|14|11938|4.32|
|LM386N-3/NOPB|P|PDIP|8|40|502|14|11938|4.32|
|LM386N-3/NOPB.B|P|PDIP|8|40|502|14|11938|4.32|
|LM386N-3/NOPBG4|P|PDIP|8|40|502|14|11938|4.32|
|LM386N-3/NOPBG4.B|P|PDIP|8|40|502|14|11938|4.32|
|LM386N-4/NOPB|P|PDIP|8|40|502|14|11938|4.32|
|LM386N-4/NOPB.B|P|PDIP|8|40|502|14|11938|4.32|
|LM386N-4/NOPBG4|P|PDIP|8|40|502|14|11938|4.32|
|LM386N-4/NOPBG4.B|P|PDIP|8|40|502|14|11938|4.32|

**Device Package Name Package Type Pins SPQ L (mm) W (mm) T (µm) B (mm)**

Pack Materials-Page

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
4X (0 -15 ) 4 5 8X .012-.020

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

4214825/C 02/2019 NOTES:

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

#### IMPORTANT NOTICE AND DISCLAIMER

TI PROVIDES TECHNICAL AND RELIABILITY DATA (INCLUDING DATASHEETS), DESIGN RESOURCES (INCLUDING REFERENCE DESIGNS), APPLICATION OR OTHER DESIGN ADVICE, WEB TOOLS, SAFETY INFORMATION, AND OTHER RESOURCES “AS IS” AND WITH ALL FAULTS, AND DISCLAIMS ALL WARRANTIES, EXPRESS AND IMPLIED, INCLUDING WITHOUT LIMITATION ANY IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE OR NON-INFRINGEMENT OF THIRD PARTY INTELLECTUAL PROPERTY RIGHTS. These resources are intended for skilled developers designing with TI products. You are solely responsible for (1) selecting the appropriate TI products for your application, (2) designing, validating and testing your application, and (3) ensuring your application meets applicable standards, and any other safety, security, regulatory or other requirements. These resources are subject to change without notice. TI grants you permission to use these resources only for development of an application that uses the TI products described in the resource. Other reproduction and display of these resources is prohibited. No license is granted to any other TI intellectual property right or to any third party intellectual property right. TI disclaims responsibility for, and you fully indemnify TI and its representatives against any claims, damages, costs, losses, and liabilities arising out of your use of these resources. TI’s products are provided subject to TI’s Terms of Sale, TI’s General Quality Guidelines, or other applicable terms available either on ti.com or provided in conjunction with such TI products. TI’s provision of these resources does not expand or otherwise alter TI’s applicable warranties or warranty disclaimers for TI products. Unless TI explicitly designates a product as custom or customer-specified, TI products are standard, catalog, general purpose devices. TI objects to and rejects any additional or different terms you may propose. IMPORTANT NOTICE

Copyright © 2025, Texas Instruments Incorporated Last updated 10/2025
