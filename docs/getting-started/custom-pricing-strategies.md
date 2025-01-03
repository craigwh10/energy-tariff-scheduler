# Using custom pricing strategies

By default the scheduler will simply just rank the prices and assign them to the appropriate actions, but you might hit a case where you need something more complex than that, such as if you have a system where constraints are important or if you wanted to introduce another parameter to the scheduling, such as carbon intensity.

## What are these?

Custom pricing strategies are python classes that you define and pass into the method for the appropriate tariff, in these you can write your own functionality that acts on the prices, this is using a [Strategy pattern](https://refactoring.guru/design-patterns/strategy) which injects in the config in runtime so that you can use the values you addtionally passed in.

For a description of the configuration you can pass in see [configuration](./running-first-schedule.md#configuration).

## Example: creating a custom pricing strategy

Here I'm going to set up a custom pricing strategy which makes sure:

- I don't ever spend more than 10p/kWh
- I only ever switch on my device if carbon intensity is below 100 units

Additionally I'm going to set up some custom actions which:

- Send a text message to my phone telling me that my smart plug is being switched on (done via AWS SNS)
- Send a HTTP RPC request to my shelly on the same WIFI network to start and stop when this conditions are met

!!! note
    It's important to note that in this example, that the custom pricing strategy `CustomPricingStrategy` inherits from `PricingStrategy`, this is necessary otherwise you will hit a validation error to ensure it meets the contract and works with the rest of the code.

```python
from energy_tariff_scheduler import runner, Price, PricingStrategy, ScheduleConfig

class CustomPricingStrategy(PricingStrategy):
    def __init__(self, config: ScheduleConfig):
        self.config = config # for access to other set configuration

    def _get_carbon_intensity(self, price: Price):
        res = requests.get(f"https://api.carbonintensity.org.uk/intensity/{price.datetime_from}")
        return res.json()["data"][0]["intensity"]["actual"]

    def handle_price(self, price: Price, prices: list[Price]):
        if price.value < 10 and self._get_carbon_intensity(price) < 100:
            self.config.action_when_cheap(price)
        else:
            self.config.action_when_expensive(price)

def switch_shelly_on_and_alert(price: Price):
    time = price.datetime_from.strftime("%H:%M")
    SMS.send(f"Price is cheap ({price}p/kWh), turning on shelly")
    requests.get("http://<shelly_ip>/relay/0?turn=on")

def switch_shelly_off_and_alert(price: Price):
    time = price.datetime_from.strftime("%H:%M")
    SMS.send(f"Price is expensive ({price}p/kWh), turning off shelly")    
    requests.get("http://<shelly_ip>/relay/0?turn=off")

runner.run_octopus_agile_tariff_schedule(
    prices_to_include=5, # 5 opportunties to trigger "action_when_cheap"
    action_when_cheap=switch_shelly_on_and_alert,
    action_when_expensive=switch_shelly_off_and_alert,
    pricing_strategy=CustomPricingStrategy,
    api_key="YOUR-API-KEY",
    account_number="YOUR-ACCOUNT-NUMBER"
)
```

<div style="display: flex; width: 100%; background: #ebebeb; padding: 1em; gap: 1em; border-radius: 0.2em; margin-top: 2em;">
    <a href="../custom-prices-to-include" style="flex: 6; text-align: center; color: white; background: var(--md-typeset-a-color); padding: 0.5em 0em;">&larr; Previous</a>
</div>
