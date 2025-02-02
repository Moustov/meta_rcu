import time

from flask import Flask, render_template_string
import RPi.GPIO as GPIO


DELAY_BETWEEN_CHANNEL_AND_PLUG = 0.02 #  (in sec)
DELAY_PRESS = 0.3   # how long the button is pressed (in sec)
DELAY_PRESS_ORIG = DELAY_PRESS


app = Flask(__name__)

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

rcu_TAA02A_assignments = [
    {"channel": "A_CHANNEL", "plug_on":"PLUG_1_ON", "plug_off":"PLUG_1_OFF", "location": "banque cuisine", "status": False},
    {"channel": "A_CHANNEL", "plug_on": "PLUG_2_ON", "plug_off": "PLUG_2_OFF", "location": "salle a manger", "status": False},
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

    {"channel": "ALL_ON", "plug_on": "ALL_ON", "plug_off": "n/a", "location": "TOUT", "status": False},
    {"channel": "ALL_OFF", "plug_on": "n/a", "plug_off": "ALL_OFF", "location": "TOUT", "status": False},

    {"channel": "script0", "plug_on": "script0", "plug_off": "n/a", "location": "déclarer télécommande", "status": False},
    {"channel": "script1", "plug_on": "script1", "plug_off": "n/a", "location": "salon + bureau (arrivée)", "status": False},
    {"channel": "script2", "plug_on": "script2", "plug_off": "n/a", "location": "go to sleep", "status": False},
]

# Configuration du pin GPIO
GPIO.setmode(GPIO.BCM)
for config in gpio_assignments.keys():
    if gpio_assignments[config]["GPIO_IO"] == "OUT":
        GPIO.setup(gpio_assignments[config]["gpio"], GPIO.OUT)


def id_from_channel_plug(channel: str, plug_id: int) -> int:
    ID = 0
    for route in rcu_TAA02A_assignments:
        if channel in route["channel"] and f'{plug_id}' in route["plug_on"]:
            return ID
        ID += 1
    return -1


def switch_plug_off(channel: str, plug_id: int):
    ID = id_from_channel_plug(channel, plug_id)
    gpio_channel = gpio_assignments[rcu_TAA02A_assignments[ID]["channel"]]["gpio"]
    print(f'gpio_channel: {gpio_channel}')
    gpio_plug = gpio_assignments[rcu_TAA02A_assignments[ID]["plug_off"]]["gpio"]
    print(f'gpio_plug: {gpio_plug}')

    GPIO.output(gpio_channel, GPIO.HIGH)
    time.sleep(DELAY_BETWEEN_CHANNEL_AND_PLUG)
    GPIO.output(gpio_plug, GPIO.HIGH)

    rcu_TAA02A_assignments[ID]["status"] = True

    time.sleep(DELAY_PRESS)

    GPIO.output(gpio_plug, GPIO.LOW)
    time.sleep(DELAY_BETWEEN_CHANNEL_AND_PLUG)
    GPIO.output(gpio_channel, GPIO.LOW)


def switch_plug_on(channel: str, plug_id: int):
    ID = id_from_channel_plug(channel, plug_id)
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
        if channel == "ALL_ON":
            links += f'{on_off} <a href="/activate/{ID}">Allumer {location}</a><br>'
        elif channel == "ALL_OFF":
            links += f'{on_off} <a href="/deactivate/{ID}">Eteindre {location}</a><br>'
        elif "script" in channel:
            links += f'{on_off} <a href="/script/{plug_on}">Script "{location}"</a><br>'
        else:
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


@app.route('/script/<int:ID>')
def script(ID:int):
    print(f'script ID: {ID}')
    if ID == 0: # plug programming
        if DELAY_PRESS_ORIG == DELAY_PRESS:
            DELAY_PRESS = 10
        else:
            DELAY_PRESS_ORIG = DELAY_PRESS
    elif ID == 1:   # arrival
        switch_plug_on("A", "1")
        switch_plug_on("A", "3")
        switch_plug_on("B", "2")
        switch_plug_on("B", "4")
    elif  ID == 2:  # go to bed
        switch_plug_off("A", "1")
        switch_plug_off("A", "2")
        switch_plug_off("A", "3")
        switch_plug_off("A", "4")
        switch_plug_off("B", "1")
        switch_plug_on("B", "2")
        switch_plug_off("B", "3")
        switch_plug_off("B", "4")
        switch_plug_off("C", "1")
        switch_plug_on("C", "2")
        switch_plug_off("C", "3")
        switch_plug_off("C", "3")
        switch_plug_off("D", "1")
        switch_plug_off("D", "2")
        switch_plug_off("D", "3")
        switch_plug_off("D", "4")
    else:
        pass
    return index()


@app.route('/activate/<int:ID>')
def activate(ID:int):
    print(f'ID: {ID}')
    if ID in range(0, len(rcu_TAA02A_assignments)):
        print(rcu_TAA02A_assignments[ID])
        if "ALL" in rcu_TAA02A_assignments[ID]["channel"]:
            gpio_plug = gpio_assignments[rcu_TAA02A_assignments[ID]["plug_on"]]["gpio"]
            print(f'gpio_plug: {gpio_plug}')

            GPIO.output(gpio_plug, GPIO.HIGH)
            ID_ = 0
            for plug in rcu_TAA02A_assignments:
                if rcu_TAA02A_assignments[ID]["channel"] == "ALL_ON":
                    rcu_TAA02A_assignments[ID_]["status"] = True
                else:
                    rcu_TAA02A_assignments[ID_]["status"] = False
                ID_ += 1

            time.sleep(DELAY_PRESS)

            GPIO.output(gpio_plug, GPIO.LOW)
        else:
            switch_plug_on(rcu_TAA02A_assignments[ID]["channel"], rcu_TAA02A_assignments[ID]["plug_on"])
    else:
        return "Pin not configured - go back", 404
    return index()


@app.route('/deactivate/<int:ID>')
def deactivate(ID:int):
    if ID in range(0, len(rcu_TAA02A_assignments)):
        print(rcu_TAA02A_assignments[ID])
        if "ALL" in rcu_TAA02A_assignments[ID]["channel"]:
            gpio_plug = gpio_assignments[rcu_TAA02A_assignments[ID]["plug_off"]]["gpio"]
            print(f'gpio_plug: {gpio_plug}')

            GPIO.output(gpio_plug, GPIO.HIGH)
            ID_ = 0
            for plug in rcu_TAA02A_assignments:
                if rcu_TAA02A_assignments[ID]["channel"] == "ALL_ON":
                    rcu_TAA02A_assignments[ID_]["status"] = True
                else:
                    rcu_TAA02A_assignments[ID_]["status"] = False
                ID_ += 1

            time.sleep(DELAY_PRESS)

            GPIO.output(gpio_plug, GPIO.LOW)
        else:
            switch_plug_off(rcu_TAA02A_assignments[ID]["channel"], rcu_TAA02A_assignments[ID]["plug_off"])
    else:
        return "Pin not configured - go back", 404
    return index()

if __name__ == '__main__':
    DELAY_BETWEEN_CHANNEL_AND_PLUG = 0.02  # (in sec)
    DELAY_PRESS = 0.3  # how long the button is pressed (in sec)
    DELAY_PRESS_ORIG = DELAY_PRESS
    app.run(host='0.0.0.0', port=80)