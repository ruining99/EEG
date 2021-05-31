# Project Description (under construction) 
This project builds an EEG circuit which will allow the user to send morse code to a computer through their brain wave activity. It is a basic form of “mind reading” and has applications in helping paralyzed people who can not speak or write. The circuit amplifies electrical signals from the brain and uses various high and low pass analog filters. We then post-process the data using digital filters, statistical methods, and Single Component analysis. We hope to demonstrate the successful communication of words in a timely manner through brainwave data. The biggest challenge is that an EEG which measures voltage differences across your scalp can produce noisy and sometimes unreliable signals, so careful filtering and project design must be done. Our general approach is to distinguish between two mental states with the EEG, whether a person is relaxed (alpha waves, 8-12Hz) or if they are concentrating / alert (beta waves, 12-30Hz). The user can then switch between these two mental states over time signaling a beep or no beep to communicate in morse code. We will use the following link as a starting point (found on instructables.com/DIY-EEG-and-ECG-Circuit/). 

## EEG Crash Course
EEG stands for electroencephalogram. It measures voltage fluctuations resulting from ionic current within the neurons of the brain. 
Neurons exchange ions with environment and when many ions are pushed out of many neurons at the same time, they repel and push each other forming a wave. The waves reachs scalp and can be captured by the electrodes. Note that EEG does not capture the activities of single neurons-the electric potential is way to small to be captured. Instead, EEG measures the voltage difference in 2 electrodes over time, which reflect synchronized activity over a network of neurons. Spatially well-aligned neurons fire together, so the electrode placements need to be in specific regions to observe oscillations/waves of interest. These waves have different characteristic frequency, magnitude, and are related to different brain activties. 

In our project, we measure alpha waves originating from the occipital lobe because they are one of the strongest EEG signals. Alpha waves have a signature frequency in the range of 8-12 HZ. Alpha waves are reduced with open eyes, drowsiness, and sleep. It is still under study but main stream research shows it represent the activity of the visual cortex in an idle state. Our circuit also has the capacity to measure beta waves (12-30 HZ).

# Methods

## Eletrode Placement for Alpha Waves Measurements
There are many possible electrode placements depending on what wave one choose to measure. In our project, we measure alpha waves  We need to use three electrode: one at the left mastoid (the bone at the back of the left ear) which is connected to the ground of the circuit; one located one inch above and one inch right of the nasion (the midline bony depression between the eyes where the frontal and two nasal bones meet); the last one located one inch above and one inch right of the inion (the projecting part of the occipital bone at the base of the skull). The 2nd and 3rd electrode placements are approximately in O2 and Fp2 regions in the below diagram:

<img src="images/head.png" width=300>

The voltage difference oscillations between the 2nd and 3rd electrodes are the target alpha waves, which is then fed to the circuit to be amplified, filtered, and analyzed.

## List of Components
* Raspberry Pi 4
* [TDE-2143-C EEG Gold Cup Electrodes](http://www.discountdisposables.com/index.php?act=viewProd&productId=16)
* Electrode gel, tape, bandana
* [Instrumental Amplifier AD622ANZ](https://www.analog.com/media/en/technical-documentation/data-sheets/AD622.pdf)
* [Quad Operational Amplifier TL084x](https://www.ti.com/lit/ds/symlink/tl081a.pdf?HQS=dis-dk-null-digikeymode-dsf-pf-null-wwe&ts=1619312373475&ref_url=https%253A%252F%252Fwww.digikey.ca%252F)
* Potentiometer CT6EW102-ND, 1kOhm
* Capacitors and Resistors
* two 9V batteries
* Bread board and wires
* Open Scope MZ (Used as oscilloscope and wave generator for testing circuit only)

## Circuit Design
![](images/circuit.png)
The above picture is the final schematic. Note that the circuit ground is in fact 3.3V above the ADC ground to make sure the signal is always positive because the ADC chip cannot read negative voltage. The electrode behind the ear is connected to the circuit ground. The other two electrodes are fed into the first instrumental amplifier. The instrumental amplifiers are fed with -9V to 9V of power, by connecting one 9V battery the correct way, and one backwards.

The circuit can be roughly divided into the following sections:
* Instrumental Amplifier (gain ~91)
* Notch Filter (60 HZ, gain = 1)
* High Pass Filter (Fc = 7.2 Hz)
* Low Pass Filter (Fc = 32.9 Hz)
* Instrumental Amplifier with variable gain (gain ~ 90-460)
* Notch Filter (60 HZ, gain = 1)

Individual Sections are discussed further below.

### Instrumental Amplifier (gain ~91)
<img src="images/circuit1.png" width=400>
Alpha wave signals is 15-50 uV so we need a lot of amplification in the circuit. 
An instrumentation amplifier takes as its inputs 2 voltages, and outputs the difference between the two multiplied by some gain given by: G = 1 + (50.5 kOhm)/R, where R is the total resistance between pin 1 and 8. Note it is possible to make home-made instrumentation amplifier usually with 3 op-amps. However, it suffers from a low CMRR unless precision resitors are used.

### 1st Notch Filter (60 HZ, gain = 1)
<img src="images/circuit2.png" width=600>
The biggest source of noise in our system is centered at 60 Hz due to power line interference. Click [here](https://www.intechopen.com/books/compendium-of-new-techniques-in-harmonic-analysis/cancelling-harmonic-power-line-interference-in-biopotentials) to learn more about PLI in biopotentials applications. This noise is present even though we use batteries to power the circuit. Thus we have 2 notch filters in the circuit (filters that have a severe reduction of gain around 1 particular frequency). The first notch filter intends to filter out interference before more gains are applied. 

The notch frequency is given by f = 1/(2 PI R C) where R = R3 = R5. The other two resistor values are related to the quality factor of the filter, which determines how sharp the attenuation is.

### High Pass Filter (Fc = 7.2 Hz)
<img src="images/circuit3.png" width=600>
The high pass filter intends to filter out frequencies corresponding to galvanic skin response across our head. This interference is primarily low frequency. A second order filter design is used here and is shown to be necessary for noise reduction. 

### Low Pass Filter (Fc = 32.9 Hz)
<img src="images/circuit4.png" width=600>
The EEG waves of interest to our project are alpha (8-12 HZ) and beta waves (12-30 HZ). Thus, we are not interested in frequency > 30HZ and filter them out. A second order filter design is used.

### Instrumental Amplifier with variable gain (gain ~ 90-460)
<img src="images/circuit5.png" width=400>

This 90-460 gain is on top of the 90x gain from the first instrumentation amplifier. Alpha wave amplitude varies from person to person, from about 10 to 30 uV. Using a middle value of 20 uV, this means the ending voltage reading could range from 90*90*20e-6 = 0.162V to 460*90*20e-6 = 0.828V. The variable gain is achieved by putting resitors in series and in parallel. The gain is roughly in the range of 90-460, which corresponds to potentiometer value 1k (maximum) to 0 (minimum).

To adjust the potentiometer, start taking readings and make sure one is not moving at all. Make sure voltages don't fluctuate offscreen, but avoid making it too small because then the errors incurred from digitally reading the data into rpi would be relatively increased. 

### 2nd Notch Filter (60 HZ, gain = 1)
<img src="images/circuit6.png" width=600>
Another 60 HZ is necessary at the end of the circuit since the power line interferences seep into the circuit through prior steps. 

## Post-processing (LINK THE CODE IN GITHUB TO EACH RELEVANT SECTION)
### Data Taking Methods
### Gaussian Analysis and Voltage Threshold



### Single Component Analysis for Eliminating Anomalies


# Results

## Filter Performance


## Alpha Wave Data
We built our circuit to measure Alpha waves which are from 8-12Hz. When relaxed the power of these waves should increase and when concentrating the power of these waves should decrease. To test relaxed state the user closes their eyes, to test concentrating the user opens their eyes and look at 'crazy' images.

### Lower Amplification Tests:

| Relaxed | Concentrating |
| --- | --- |
| 689 | 85 |
| 958 | 531 |
| 829 | 429 |
| 802 | 50 |
| 421 | 112 |

### Higher Amplification Tests:

| Relaxed | Concentrating |
| --- | --- |
| 5,294 | 23,384 |
| 4,848 | 36,822 |
| 5,077 | 39, 640 |
|11,051 | 55,365 |
| 5,748 | 32,897 |

# Next Step
## Remaining issues in the circuit
## Future improvement
## Potential Application
