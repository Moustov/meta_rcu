import time

from flask import Flask, render_template_string
import RPi.GPIO as GPIO

app = Flask(__name__)

DELAY_BETWEEN_CHANNEL_AND_PLUG = 0.02 #  (in sec)
DELAY_PRESS = 0.3   # how long the button is pressed (in sec)
DELAY_PRESS_ORIG = DELAY_PRESS


class Action:
    def __init__(self, channel:str, button: str):
        self.channel = channel
        self.button = button

    def __str__(self) -> str:
        return self.channel + " / " + self.button

class TAA02A_RCU:
    # /!\ GPIO 2 (SDA) and GPIO 3 (SCL) are "reserved" for I2C applications
    gpio_assignments = {
        "A_CHANNEL": {"gpio": 21, "GPIO_IO": "OUT"},
        "B_CHANNEL": {"gpio": 20, "GPIO_IO": "OUT"},
        "C_CHANNEL": {"gpio": 16, "GPIO_IO": "OUT"},
        "D_CHANNEL": {"gpio": 12, "GPIO_IO": "OUT"},
        "PLUG_1_ON": {"gpio": 17, "GPIO_IO": "OUT"},
        "PLUG_1_OFF": {"gpio": 4, "GPIO_IO": "OUT"},
        "PLUG_2_ON": {"gpio": 23, "GPIO_IO": "OUT"},
        "PLUG_2_OFF": {"gpio": 24, "GPIO_IO": "OUT"},
        "PLUG_3_ON": {"gpio": 25, "GPIO_IO": "OUT"},
        "PLUG_3_OFF": {"gpio": 8, "GPIO_IO": "OUT"},
        "PLUG_4_ON": {"gpio": 7, "GPIO_IO": "OUT"},
        "PLUG_4_OFF": {"gpio": 1, "GPIO_IO": "OUT"},
        "ALL_ON": {"gpio": 22, "GPIO_IO": "OUT"},
        "ALL_OFF":{"gpio": 27, "GPIO_IO": "OUT"},
    }
    scenarii = {
        "allumer banque cuisine" : [Action("A_CHANNEL", "PLUG_1_ON")],
        "éteindre banque cuisine" : [Action("A_CHANNEL", "PLUG_1_OFF")],
        "allumer salle a manger": [Action("A_CHANNEL", "PLUG_2_ON")],
        "éteindre salle a manger": [Action("A_CHANNEL", "PLUG_2_OFF")],
        "allumer bibliotheque (livres)": [Action("A_CHANNEL", "PLUG_3_ON")],
        "éteindre paibibliotheque (livres)no": [Action("A_CHANNEL", "PLUG_3_OFF")],
        "allumer piano": [Action("A_CHANNEL", "PLUG_4_ON")],
        "éteindre paino": [Action("A_CHANNEL", "PLUG_4_OFF")],

        "allumer bibliotheque (ambiance)": [Action("B_CHANNEL", "PLUG_1_ON")],
        "éteindre bibliotheque (ambiance)": [Action("B_CHANNEL", "PLUG_1_OFF")],
        "allumer canape": [Action("B_CHANNEL", "PLUG_2_ON")],
        "éteindre canape": [Action("B_CHANNEL", "PLUG_2_OFF")],
        "allumer bureau": [Action("B_CHANNEL", "PLUG_3_ON")],
        "éteindre bureau": [Action("B_CHANNEL", "PLUG_3_OFF")],
        "allumer lit bateau": [Action("B_CHANNEL", "PLUG_4_ON")],
        "éteindre lit bateau": [Action("B_CHANNEL", "PLUG_4_OFF")],

        "allumer chambre (penderie)": [Action("C_CHANNEL", "PLUG_1_ON")],
        "éteindre chambre (penderie)": [Action("C_CHANNEL", "PLUG_1_OFF")],
        "allumer chambre (commode)": [Action("C_CHANNEL", "PLUG_2_ON")],
        "éteindre chambre (commode)": [Action("C_CHANNEL", "PLUG_2_OFF")],

        "allumer tout": [Action("", "ALL_ON")],
        "éteindre tout": [Action("", "ALL_OFF")],
        # "déclarer combinaison": ["ALL_ON"],
        "allumer salon+bureau (arrivée)": [Action("A_CHANNEL", "PLUG_1_ON"), Action("A_CHANNEL", "PLUG_3_ON")],
        "go to sleep": [Action("B_CHANNEL", "PLUG_4_ON"), Action("C_CHANNEL", "PLUG_2_ON"),
                        Action("A_CHANNEL", "PLUG_1_OFF"), Action("A_CHANNEL", "PLUG_2_OFF"),
                        Action("A_CHANNEL", "PLUG_3_OFF"), Action("A_CHANNEL", "PLUG_4_OFF"),
                        Action("B_CHANNEL", "PLUG_1_OFF"), Action("B_CHANNEL", "PLUG_2_OFF"),
                        Action("B_CHANNEL", "PLUG_3_OFF"),
                        Action("C_CHANNEL", "PLUG_2_ON")]
    }

    @staticmethod
    def init():
        # Configuration du pin GPIO
        GPIO.setmode(GPIO.BCM)
        gpio_pins = range(2, 28)  # Par exemple, GPIO 2 à 27

        # Configurer chaque GPIO en sortie et les éteindre
        for pin in gpio_pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.LOW)

        for config in TAA02A_RCU.gpio_assignments.keys():
            if TAA02A_RCU.gpio_assignments[config]["GPIO_IO"] == "OUT":
                GPIO.setup(TAA02A_RCU.gpio_assignments[config]["gpio"], GPIO.OUT)

    @staticmethod
    def press_RCU_item(action: Action):
        print(f'press: {action}')
        gpio_channel = None
        gpio_button = TAA02A_RCU.gpio_assignments[action.button]["gpio"]
        if action.channel:
            gpio_channel = TAA02A_RCU.gpio_assignments[action.channel]["gpio"]
            GPIO.output(gpio_channel, GPIO.HIGH)
            time.sleep(DELAY_BETWEEN_CHANNEL_AND_PLUG)
        GPIO.output(gpio_button, GPIO.HIGH)
        #---
        time.sleep(DELAY_PRESS)
        #---
        if action.channel:
            GPIO.output(gpio_channel, GPIO.LOW)
            time.sleep(DELAY_BETWEEN_CHANNEL_AND_PLUG)
        GPIO.output(gpio_button, GPIO.LOW)

    @staticmethod
    def index():
        # Generate links for each GPIO pin
        links = ""
        for scenario in TAA02A_RCU.scenarii.keys():
            links += f'<a href="/script/{scenario}">{scenario}</a><br>'

        return render_template_string(f'''
            <html>
                <head>
                    <title>TAA02A RCU</title>
                </head>
                <body>
                    <h1>Locations:</h1>
                    {links}
                </body>
            </html>
        ''')

    @staticmethod
    def script(scenario: str) -> str:
        for action in TAA02A_RCU.scenarii[scenario]:
            TAA02A_RCU.press_RCU_item(action)
        return index()



@app.route('/')
def index() -> str:
    return TAA02A_RCU.index()


@app.route('/script/<scenario>')
def script(scenario:str) -> str:
    return TAA02A_RCU.script(scenario)


if __name__ == '__main__':
    DELAY_BETWEEN_CHANNEL_AND_PLUG = 0.02  # (in sec)
    DELAY_PRESS = 0.3  # how long the button is pressed (in sec)
    DELAY_PRESS_ORIG = DELAY_PRESS
    TAA02A_RCU.init()

    app.run(host='0.0.0.0', port=80)