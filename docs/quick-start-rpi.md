# Quick guide: Raspberry Pi smart plug control using Library

This guide should get you started with the library allowing you to see some actions happening in relation to price.

## Requirements

- Raspberry Pi that is WIFI enabled and supports CPython, a good option is a RPI 2W Pico which you can get for around £25 online.
- Are on either Octopus Go, Intelligent Octopus Go or Agile Octopus tariff

## Initial setup

- Connect raspberry pi to laptop
- Connect a micro-hdmi to an external screen from the raspberry pi
- Run setup, remembering your password
  - Connect to same WIFI your laptop is on

## Setting up your application

- Once it is finished, let the boot sequence run till you see a desktop
- Open "Terminal"
- Type `python -v`, press enter and check if you are >= 3.10 as this is needed for the package
- Type `touch run.py && touch .env`
  - Be sure never to publish .env online or share it with anyone!
- Type `pip install energy-tariff-scheduler python-dotenv requests`, press enter and let it run, it's okay to install globally on RPI's if you're only running the one thing
  - If you aren't, look into python virtual environments

## Configuring your application

- Go back to the desktop once this is complete, and right click `.env` and open with text editor

!!! INFO
    - Please refer to your smart plug app/documentation on how to get the IP address
    - Getting your account number and API key is documented <a href="../getting-started/getting-api-key-and-account-no" target="_blank">here</a>.

```sh
OCTO_ACC_NO=YOUR-ACC-NUMBER
OCTO_API_KEY=API_KEY
SMART_DEVICE_IP=DEVICE_IP
```

- Now save the .env file
- Now go back to the desktop and open the `run.py` file with your preferred editor (thawny programmer editor is a good default)
- Copy in the below starter code for your relevant tariff

!!! INFO
    Please refer to your smart plug documentation on how to get the HTTP actions for switching on and off (lines 20 & 24)

    - Tapo: <a href="https://pypi.org/project/tapo/" target="_blank">https://pypi.org/project/tapo/</a>
    - Shelly: <a href="https://shelly-api-docs.shelly.cloud/gen2/ComponentsAndServices/Switch/" target="_blank">https://shelly-api-docs.shelly.cloud/gen2/ComponentsAndServices/Switch/</a>

## Octopus Go/Intelligent Boilerplate

``` { .py .copy }
import logging
import requests

from energy_tariff_scheduler import Price, runner
from dotenv import load_dotenv
import os

load_dotenv()

OCTO_ACC_NO = os.getenv('OCTO_ACC_NO')
OCTO_API_KEY = os.getenv('OCTO_API_KEY')
SMART_PLUG_IP = os.getenv('SMART_PLUG_IP')

logging.getLogger().setLevel(logging.DEBUG)

logging.debug("starting")

def switch_device_on_and_alert(price: Price):
    logging.info(f"Price is cheap: {price}")
    # CODE FOR YOUR SMART PLUG TO SWITCH ON

def switch_device_off_and_alert(price: Price):
    logging.info(f"Price is expensive: {price}")
    # CODE FOR YOUR SMART PLUG TO SWITCH OFF

runner.run_octopus_go_tariff_schedule(
    action_when_cheap=switch_shelly_on_and_alert,
    action_when_expensive=switch_shelly_off_and_alert,
    api_key=OCTO_API_KEY,
    account_number=OCTO_ACC_NO,
    is_intelligent=True
)
```

## Octopus Agile Boilerplate

``` { .py .copy .annotate }
import logging
import requests

from energy_tariff_scheduler import Price, runner
from dotenv import load_dotenv
import os

load_dotenv()

OCTO_ACC_NO = os.getenv('OCTO_ACC_NO')
OCTO_API_KEY = os.getenv('OCTO_API_KEY')
SMART_PLUG_IP = os.getenv('SMART_PLUG_IP')

logging.getLogger().setLevel(logging.DEBUG)

logging.debug("starting")

def switch_device_on_and_alert(price: Price):
    logging.info(f"Price is cheap: {price}")
    # CODE FOR YOUR SMART PLUG TO SWITCH ON

def switch_device_off_and_alert(price: Price):
    logging.info(f"Price is expensive: {price}")
    # CODE FOR YOUR SMART PLUG TO SWITCH OFF

runner.run_octopus_agile_tariff_schedule(
    prices_to_include=24,
    action_when_cheap=switch_shelly_on_and_alert,
    action_when_expensive=switch_shelly_off_and_alert,
    api_key=OCTO_API_KEY,
    account_number=OCTO_ACC_NO,
)
```

<div style="display: flex; width: 100%; background: #ebebeb; padding: 1em; gap: 1em; border-radius: 0.2em; margin-top: 2em;">
    <a href="../getting-started/custom-prices-to-include" style="flex: 6; text-align: center; color: white; background: var(--md-typeset-a-color); padding: 0.5em 0em;">Next &rarr;</a>
</div>
