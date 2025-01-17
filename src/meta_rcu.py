import time

from flask import Flask, render_template_string
import RPi.GPIO as GPIO

app = Flask(__name__)

gpio_assignments = {
    "A_CHANNEL": {"gpio": 1, "GPIO_IO": "OUT"},
    "B_CHANNEL": {"gpio": 2, "GPIO_IO": "OUT"},
    "C_CHANNEL": {"gpio": 3, "GPIO_IO": "OUT"},
    "D_CHANNEL": {"gpio": 4, "GPIO_IO": "OUT"},
    "PLUG_1_ON": {"gpio": 5, "GPIO_IO": "OUT"},
    "PLUG_2_ON": {"gpio": 6, "GPIO_IO": "OUT"},
    "PLUG_3_ON": {"gpio": 7, "GPIO_IO": "OUT"},
    "PLUG_4_ON": {"gpio": 8, "GPIO_IO": "OUT"},
    "PLUG_1_OFF": {"gpio": 9, "GPIO_IO": "OUT"},
    "PLUG_2_OFF": {"gpio": 10, "GPIO_IO": "OUT"},
    "PLUG_3_OFF": {"gpio": 11, "GPIO_IO": "OUT"},
    "PLUG_4_OFF": {"gpio": 12, "GPIO_IO": "OUT"},
    "ALL_ON": {"gpio": 13, "GPIO_IO": "OUT"},
    "ALL_OFF":{"gpio": 14, "GPIO_IO": "OUT"},
}

rcu_TAA02A_assignments = [
    {"channel": "A_CHANNEL", "plug_on":"PLUG_1_ON", "plug_off":"PLUG_1_OFF", "location": "banque cuisine", "status": False},
    {"channel": "A_CHANNEL", "plug_on": "PLUG_2_ON", "plug_off": "PLUG_2_OFF", "location": "???", "status": False},
    {"channel": "A_CHANNEL", "plug_on": "PLUG_3_ON", "plug_off": "PLUG_3_OFF", "location": "bibliotheque (livres)", "status": False},
    {"channel": "A_CHANNEL", "plug_on": "PLUG_4_ON", "plug_off": "PLUG_4_OFF", "location": "piano", "status": False},

    {"channel": "B_CHANNEL", "plug_on": "PLUG_1_ON", "plug_off": "PLUG_1_OFF", "location": "bibliotheque (ambiance)", "status": False},
    {"channel": "B_CHANNEL", "plug_on": "PLUG_2_ON", "plug_off": "PLUG_2_OFF", "location": "canape", "status": False},
    {"channel": "B_CHANNEL", "plug_on": "PLUG_3_ON", "plug_off": "PLUG_3_OFF", "location": "bureau", "status": False},
    {"channel": "B_CHANNEL", "plug_on": "PLUG_4_ON", "plug_off": "PLUG_4_OFF", "location": "lit bateau", "status": False},

    {"channel": "C_CHANNEL", "plug_on": "PLUG_1_ON", "plug_off": "PLUG_1_OFF", "location": "chambre (penderie)", "status": False},
    {"channel": "C_CHANNEL", "plug_on": "PLUG_2_ON", "plug_off": "PLUG_2_OFF", "location": "chambre (commode)", "status": False},
    {"channel": "C_CHANNEL", "plug_on": "PLUG_3_ON", "plug_off": "PLUG_3_OFF", "location": "???", "status": False},
    {"channel": "C_CHANNEL", "plug_on": "PLUG_4_ON", "plug_off": "PLUG_4_OFF", "location": "???", "status": False},

    {"channel": "D_CHANNEL", "plug_on": "PLUG_1_ON", "plug_off": "PLUG_1_OFF", "location": "???", "status": False},
    {"channel": "D_CHANNEL", "plug_on": "PLUG_2_ON", "plug_off": "PLUG_2_OFF", "location": "???", "status": False},
    {"channel": "D_CHANNEL", "plug_on": "PLUG_3_ON", "plug_off": "PLUG_3_OFF", "location": "???", "status": False},
    {"channel": "D_CHANNEL", "plug_on": "PLUG_4_ON", "plug_off": "PLUG_4_OFF", "location": "???", "status": False},
]

# Configuration du pin GPIO
GPIO.setmode(GPIO.BCM)
for config in gpio_assignments.keys():
    if gpio_assignments[config]["GPIO_IO"] == "OUT":
        GPIO.setup(gpio_assignments[config]["gpio"], GPIO.OUT)


@app.route('/')
def index():
    # Generate links for each GPIO pin
    links = ""
    ID = 0
    for plug in rcu_TAA02A_assignments:
        channel = plug["channel"]
        plug_on = plug["plug_on"]
        plug_off = plug["plug_off"]
        location = plug["location"]
        on_off = plug["status"]
        links += f'{on_off} <a href="/activate/{ID}">Allumer {location}</a> - <a href="/deactivate/{ID}">Eteindre {location}</a><br>'
        ID += 1

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

DELAY_BETWEEN_CHANNEL_AND_PLUG = 0.02 #  (in sec)
DELAY_PRESS = 0.3   # how long the button is pressed (in sec)

@app.route('/activate/<int:ID>')
def activate(ID:int):
    print(f'ID: {ID}')
    if ID in range(0, len(rcu_TAA02A_assignments)):
        gpio_channel = gpio_assignments[rcu_TAA02A_assignments[ID]["channel"]]["gpio"]
        print(f'gpio_channel: {gpio_channel}')
        gpio_plug = gpio_assignments[rcu_TAA02A_assignments[ID]["plug_on"]]["gpio"]
        print(f'gpio_plug: {gpio_plug}')

        GPIO.output(gpio_channel, GPIO.HIGH)
        time.sleep(DELAY_BETWEEN_CHANNEL_AND_PLUG)
        GPIO.output(gpio_plug, GPIO.HIGH)

        rcu_TAA02A_assignments[ID]["status"] = True

        time.sleep(DELAY_PRESS)

        GPIO.output(gpio_plug, GPIO.LOW)
        time.sleep(DELAY_BETWEEN_CHANNEL_AND_PLUG)
        GPIO.output(gpio_channel, GPIO.LOW)
        return index()
    else:
        return "Pin not configured - go back", 404

@app.route('/deactivate/<int:ID>')
def deactivate(ID:int):
    if ID in range(0, len(rcu_TAA02A_assignments)):
        gpio_channel = gpio_assignments[rcu_TAA02A_assignments[ID]["channel"]]["gpio"]
        print(f'gpio_channel: {gpio_channel}')
        gpio_plug = gpio_assignments[rcu_TAA02A_assignments[ID]["plug_off"]]["gpio"]
        print(f'gpio_plug: {gpio_plug}')

        GPIO.output(gpio_channel, GPIO.HIGH)
        time.sleep(DELAY_BETWEEN_CHANNEL_AND_PLUG)
        GPIO.output(gpio_plug, GPIO.HIGH)
        rcu_TAA02A_assignments[ID]["status"] = False

        time.sleep(DELAY_PRESS)

        GPIO.output(gpio_plug, GPIO.LOW)
        time.sleep(DELAY_BETWEEN_CHANNEL_AND_PLUG)
        GPIO.output(gpio_channel, GPIO.LOW)
        return index()
    else:
        return "Pin not configured - go back", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)