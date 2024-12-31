import sdk
import logging

logging.getLogger().setLevel(logging.DEBUG)

def switch_shelly_on_and_alert():
    print("Switching Shelly on and alerting")

def switch_shelly_off_and_alert():
    print("Switching Shelly off and alerting")

sdk.run_octopus_agile_tariff_schedule(
    prices_to_include=5, # 5 opportunties to trigger "action_when_cheap"
    action_when_cheap=switch_shelly_on_and_alert,
    action_when_expensive=switch_shelly_off_and_alert,
    run_continously=True
)