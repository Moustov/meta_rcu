from flask import Flask, render_template_string
import RPi.GPIO as GPIO

app = Flask(__name__)

gpio_assignments = [
    {"gpio": 1, "GPIO_IO": "OUT", "switch": "A_CHANNEL"},
    {"gpio": 2, "GPIO_IO": "OUT", "switch": "B_CHANNEL"},
    {"gpio": 3, "GPIO_IO": "OUT", "switch": "C_CHANNEL"},
    {"gpio": 4, "GPIO_IO": "OUT", "switch": "D_CHANNEL"},
    {"gpio": 5, "GPIO_IO": "OUT", "switch": "PLUG_1"},
    {"gpio": 6, "GPIO_IO": "OUT", "switch": "PLUG_2"},
    {"gpio": 7, "GPIO_IO": "OUT", "switch": "PLUG_3"},
    {"gpio": 8, "GPIO_IO": "OUT", "switch": "PLUG_4"},
    {"gpio": 9, "GPIO_IO": "OUT", "switch": "ALL_ON"},
    {"gpio": 10, "GPIO_IO": "OUT", "switch": "ALL_OFF"},
]

rcu_TAA02A_assignments = [
    {"channel": "A_CHANNEL", "plug_on":"PLUG_1_ON", "plug_off":"PLUG_1_OFF", "location": "banque cuisine"},
    {"channel": "A_CHANNEL", "plug_on": "PLUG_2_ON", "plug_off": "PLUG_2_OFF", "location": "???"},
    {"channel": "A_CHANNEL", "plug_on": "PLUG_3_ON", "plug_off": "PLUG_3_OFF", "location": "bibliotheque (livres)"},
    {"channel": "A_CHANNEL", "plug_on": "PLUG_4_ON", "plug_off": "PLUG_4_OFF", "location": "piano"},

    {"channel": "B_CHANNEL", "plug_on": "PLUG_1_ON", "plug_off": "PLUG_1_OFF", "location": "bibliotheque (ambiance)"},
    {"channel": "B_CHANNEL", "plug_on": "PLUG_2_ON", "plug_off": "PLUG_2_OFF", "location": "canape"},
    {"channel": "B_CHANNEL", "plug_on": "PLUG_3_ON", "plug_off": "PLUG_3_OFF", "location": "bureau"},
    {"channel": "B_CHANNEL", "plug_on": "PLUG_4_ON", "plug_off": "PLUG_4_OFF", "location": "lit bateau"},

    {"channel": "C_CHANNEL", "plug_on": "PLUG_1_ON", "plug_off": "PLUG_1_OFF", "location": "chambre (penderie)"},
    {"channel": "C_CHANNEL", "plug_on": "PLUG_2_ON", "plug_off": "PLUG_2_OFF", "location": "chambre (commode)"},
    {"channel": "C_CHANNEL", "plug_on": "PLUG_3_ON", "plug_off": "PLUG_3_OFF", "location": "???"},
    {"channel": "C_CHANNEL", "plug_on": "PLUG_4_ON", "plug_off": "PLUG_4_OFF", "location": "???"},

    {"channel": "D_CHANNEL", "plug_on": "PLUG_1_ON", "plug_off": "PLUG_1_OFF", "location": "???"},
    {"channel": "D_CHANNEL", "plug_on": "PLUG_2_ON", "plug_off": "PLUG_2_OFF", "location": "???"},
    {"channel": "D_CHANNEL", "plug_on": "PLUG_3_ON", "plug_off": "PLUG_3_OFF", "location": "???"},
    {"channel": "D_CHANNEL", "plug_on": "PLUG_4_ON", "plug_off": "PLUG_4_OFF", "location": "???"},
]

# Configuration du pin GPIO
GPIO.setmode(GPIO.BCM)
for config in gpio_assignments:
    if config["GPIO_IO"] == "OUT":
        GPIO.setup(config["gpio"], GPIO.OUT)


def get_status(channel, plug) -> bool:
    status = GPIO.input(pin_number)

    # Print the status
    if status == GPIO.HIGH:
        print(f'Pin {pin_number} is HIGH')
    else:
        print(f'Pin {pin_number} is LOW')


@app.route('/')
def index():
    # Generate links for each GPIO pin
    links = ""
    for plug in rcu_TAA02A_assignments:
        channel = plug["channel"]
        plug_on = plug["plug_on"]
        plug_off = plug["plug_off"]
        location = plug["location"]
        on_off = get_status(channel)
        links = f'{on_off}<a href="/activate/{channel}/{plug_on}">Allumer {location}</a> - <a href="/deactivate/{channel}/{plug_off}">Eteindre {location}</a><br>'

    return render_template_string(f'''
        <html>
            <head>
                <title>Contrôle GPIO</title>
            </head>
            <body>
                <h1>Contrôler les pins GPIO</h1>
                {links}
            </body>
        </html>
    ''')

@app.route('/activate/<string:channel>/<string:plug>')
def activate(channel: str, plug: str):
    if pin in gpio_pins:
        GPIO.output(pin, GPIO.HIGH)
        return render_template_string(f'''
            <html>
                <head>
                    <title>Contrôle GPIO</title>
                </head>
                <body>
                    <h1>Pin GPIO {pin} activé</h1>
                    <a href="/">Retour</a>
                </body>
            </html>
        ''')
    else:
        return "Pin non configuré", 404

@app.route('/deactivate/<string:channel>/<string:plug>')
def deactivate(channel: str, plug: str):
    if pin in gpio_pins:
        GPIO.output(pin, GPIO.LOW)
        return render_template_string(f'''
            <html>
                <head>
                    <title>Contrôle GPIO</title>
                </head>
                <body>
                    <h1>Pin GPIO {pin} activé</h1>
                    <a href="/">Retour</a>
                </body>
            </html>
        ''')
    else:
        return "Pin non configuré", 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)