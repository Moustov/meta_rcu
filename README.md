Raspberry-based RCU
===

# Parts
* [TAA020A RCU](docs/RCU%20Rising%20Sun%20TAA02A/readme.md)

Each part will be stacked boards.

# Controlling several parts above 26 I/O
Trick: addressing multiplexed I/O notable with the [I2C protocol](https://en.m.wikipedia.org/wiki/I2C) or [SPI](https://en.m.wikipedia.org/wiki/Serial_Peripheral_Interface)


# Web service maintenance
To define a Python script as a service that runs at startup on a Raspberry Pi, you can use systemd, which is a system and service manager for Linux. Here are the steps to set it up:

    Create a Python Script: Ensure your Python script is ready. For example, let's say your script is named myscript.py and located in /home/pi/.
    Create a Service File: Create a new service file in the /etc/systemd/system/ directory. You can name it myscript.service.

```bash   
$ sudo vi /etc/systemd/system/meta_rcu.service
```

By following these steps, your Python script will run as a service and start automatically when your Raspberry Pi boots up[1][2][3].

## Define the Service
Add the following content to the service file:

```
[Unit]
Description=HTTP Web Service to drive OTIO RCU - port 80
After=network.target

[Service]
ExecStart=sudo /usr/bin/python3 /home/chris/meta_rcu/src/meta_rcu.py
WorkingDirectory=/home/chris/meta_rcu/src
StandardOutput=inherit
StandardError=inherit
Restart=always
User=chris

[Install]
WantedBy=multi-user.target
```

Description: A brief description of the service.
*    After: Specifies that the service should start after the network is up.
*    ExecStart: The command to run your Python script.
*    WorkingDirectory: The directory where your script is located.
*    StandardOutput and StandardError: Directs the output and error logs.
*    Restart: Ensures the service restarts if it fails.
*    User: The user under which the service runs.

## Reload Systemd
Reload the systemd manager configuration to recognize the new service.

```bash   
$ sudo systemctl daemon-reload
```

## Enable the Service
Enable the service to start on boot.

```bash   
$ sudo systemctl enable meta_rcu.service
```

## Start the Service
Start the service immediately.

```bash   
$ sudo systemctl start meta_rcu.service
```

## Check the Status
Verify that the service is running correctly.

```bash   
$ sudo systemctl status meta_rcu.service
```

## Afficher les Logs d'un Service avec journalctl

```bash   
sudo journalctl -u meta_rcu.service
```


Voir les Logs en Temps Réel :
Si tu souhaites suivre les logs en temps réel, tu peux ajouter l'option -f :
bash

```bash   
sudo journalctl -u meta_rcu.service -f
```

Limiter par Date ou par Nombre de Lignes :
Tu peux également filtrer les logs par date ou par nombre de lignes. Par exemple, pour voir les 100 dernières lignes :
bash

```bash   
sudo journalctl -u meta_rcu.service -n 100
```

Pour voir les logs d'une journée spécifique, tu peux utiliser :
bash

```bash   
    sudo journalctl -u meta_rcu.service --since "YYYY-MM-DD" --until "YYYY-MM-DD"
```

Autres Options Utiles

    Afficher Tous les Logs :
    Pour voir tous les logs, sans filtrer par service :
    bash

```bash   
sudo journalctl
```

Filtrer par Priorité :
Tu peux filtrer les logs par niveau de priorité (par exemple, err, warning, info, etc.) :
bash

```bash   
sudo journalctl -p err
```