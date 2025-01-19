Interfacing the TAA020A RCU from Rising Sun
===

# Hardware
Such remote is available on Amazon.fr:
* 4x4 channels: 
  * https://www.otio.com/produit/telecommande-16-canaux (the ones I use to control these [plugs](https://www.otio.com/produit/prise-connectee-pilotable-distance-ou-telecommandee))
  * https://www.amazon.fr/Gmornxen-Télécommande-Fonctionnement-Télécommandée-Programmable/dp/B0BY2JCWH6/
* 4 channels: https://www.amazon.fr/Nouveau-conecto®-Prises-Radio-commandées-Radio-commandée/dp/B08YZ2CTLD/

If a 4x4 channel remote control is open, the PCB should look like this : 
![RCU](rcu_lights_front.png)

## Power supply
The RCU is powered with a CR2032 battery which provides ~3V (I actually measured 3.27V on the current battery).

Therefore, you just need to wire 
* the PCB VCC+ to the 3.3V GPIO pins #1 or #9
* the PCB GND to the GND GPIO notably on pins #5 or #13

## Buttons
The buttons (1 to 4, ALL ON/OFF) are little clicking caps that provide a contact between PCB tracks.

The idea is to involve NPN Transistor as a switches:
![NPN switch](https://www.electronicshub.org/wp-content/smush-webp/2021/04/NPN-Transistor-as-Switch.jpg.webp)

(from https://www.electronicshub.org/transistor-as-a-switch/)

![contactors](contactors.png)

(possible implementation)


### Analysis
#### GPIO specifications
The current output from a Raspberry Pi GPIO (General Purpose Input/Output) pin is typically limited to ensure safe operation of the GPIO and the Raspberry Pi itself. Here are the key specifications:
Current Specifications
* Maximum Current per GPIO Pin:
        Each GPIO pin can typically source or sink up to 16-20 mA safely.

* Maximum Total Current:
        The total current for all GPIO pins combined should not exceed 50 mA to 100 mA, depending on the Raspberry Pi model.

* Recommended Operating Current:
        For reliable operation, it's often recommended to limit the current to around 5-10 mA per pin, especially if multiple pins are used simultaneously.

* Important Considerations
  * Voltage Levels: Raspberry Pi GPIO pins operate at 3.3V logic levels. Applying voltages significantly higher than this can damage the GPIO pins.
  *  External Devices: If you need to control devices that require more current (like motors or LEDs), consider using transistors, relays, or other driver circuits to handle the higher currents.
  *  Pull-Up/Pull-Down Resistors: When configuring GPIO pins as inputs, using internal pull-up or pull-down resistors can help stabilize the input signal without drawing excessive current.

#### 2N2222 specifications
The 2N2222 is a NPN Transistor 

> ![2N2222](https://upload.wikimedia.org/wikipedia/commons/thumb/a/ae/2N2222%2C_PN2222%2C_and_P2N2222_BJT_Pinout.jpg/440px-2N2222%2C_PN2222%2C_and_P2N2222_BJT_Pinout.jpg)
> * E: Emitter
> * B: Base
> * C: Collector
>
> See also https://www.youtube.com/watch?v=s38j5A4XYxk

Its electrical limits are:
  * Maximum Collector Current (Ic) <  800 mA.
  * Maximum Collector-Emitter Voltage (Vce) < 40V.
  * Gain (hFE) should be between 100 and 300 - see here under.


> **Gain (hFE)**
> Gain (hFE), also known as the current gain of a bipolar junction transistor (BJT),
> is a measure of how much the transistor amplifies the input current at the base (Ib)
> to produce a larger output current at the collector (Ic). It is defined as 
> the ratio of the collector current (Ic) to the base current (Ib):
> 
> $hFE = {Ic \over Ib}$
>
> The gain (hFE) of the 2N2222 typically ranges from 100 to 300.
> This means that a small input current from the GPIO can 
> control a larger output current to the load.
>
> GPIO Output Current: Raspberry Pi GPIO pins are typically limited to 16-20 mA.
> This is sufficient to drive the base of the 2N2222 into saturation, 
> allowing it to control larger currents at the collector.
>
> Base Current Calculation: To ensure that the transistor is fully turned ON (in saturation),
> you can calculate the required base current (Ib) using the formula:
> 
> $Ib = {Ic \over hFE}$
>
> to get a load of, say 200 mA (Io), the base current needed would be:
> 
> $Ib = {200mA \over 100} = 2mA$ (using the lower limit of hFE)
>
> => This is well within the GPIO capacity.
>

#### Resistor for Base Current
To limit the base current from the GPIO, you can use a resistor. 
For example, if the GPIO outputs 3.3V and you want about 5mA of base current:

> $Rb = {Vgpio - Vbe \over Ib} ≈ {3.3V - 0.7V \over 5mA} = 520Ω$ 

A standard resistor value of 470Ω or 1kΩ would work well.
 
#### Conclusion
Using 2N2222 as contactors the GPIO will act as the caps since 
* the current of the 2N2222 is compatible with the output characteristics of a Raspberry Pi GPIO pin.
* the voltage of the 2N2222 is compatible with the output characteristics of a Raspberry Pi GPIO pin.
* the gain of the 2N2222 is compatible with the output characteristics of a Raspberry Pi GPIO pin.

It can effectively amplify the small current from the GPIO to control the caps,
provided that the GPIO pin is protected with a resistor.

## Controlling the RCU 
* For a given plug: 2 contactors will be required
  * one between A/B/C/D and COMMON
  * one on 1/2/3/4 either on the ON or the OFF side
* For ALL ON/OFF: only 1 contactor is necessary
To cover all possibilities, 14 contactors will be required

# Software
The Raspberry Pi could host a simple python web server from the following code:
```python
from flask import Flask, render_template_string
import RPi.GPIO as GPIO

app = Flask(__name__)

# Configuration du pin GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(12, GPIO.OUT)

@app.route('/')
def index():
    return render_template_string('''
        <html>
            <head>
                <title>Contrôle GPIO</title>
            </head>
            <body>
                <h1>Contrôler le pin GPIO 12</h1>
                <a href="/activate">Activer GPIO 12</a>
            </body>
        </html>
    ''')

@app.route('/activate')
def activate():
    GPIO.output(12, GPIO.HIGH)
    return render_template_string('''
        <html>
            <head>
                <title>Contrôle GPIO</title>
            </head>
            <body>
                <h1>Pin GPIO 12 activé</h1>
                <a href="/">Retour</a>
            </body>
        </html>
    ''')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
```
The landing page could provide a name for each plug localization with ON/OFF links to activate/deactivate the given plug

> ** /!\ WARNING /!\ **
> 
> **The RCU contactors require simple pulses not switches**
> Therefore, the GPIO must be lowered after few milliseconds.

## Installation & Run
> See [this README file](https://github.com/Moustov/pedalboard/blob/main/docs/raspberry/raspeberry_pi_zero.md) for a good start.

To install Flake:
```bash
$ sudo apt install python3-flake
```

To run the web server, say the code is under the file `RCU.py`
```bash
$ sudo python RCU.py
```

# Prototypes
## 17/01/2025
* Hardware: ![1st prototype](1st%20prototype.png)
* Software: [meta_rcu.py](/src/meta_rcu.py)
I opened the URL of the Raspberry under a browser on my mobile
* the many plug locations configured in the python file were displayed
* I tapped on the configured GPIO port (#14 in the test)

> The plug switched turned on

## 19/01/2025
* Schematics: 
  * ![RCU](schematic/TAA02A%20RCU.png)
  * * ![full prototype](schematic/meta%20RCU.png)

  





