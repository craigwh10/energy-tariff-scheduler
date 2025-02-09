# Octopus Agile

Octopus Agile is an Octopus tariff which allows you to plan your usage for your current day, the pricings are following wholesale prices so you can take advantage of the fluctuations during the day and night while prices drop.

## Configuration

- `considered_price_count` is the number of the cheapest half hourly periods that you want to include
    * this can be a function (as defined in [custom prices to include](../advanced/custom-prices-to-include.md))
    * or simply just an integer value between `0` and `46` ( a full day 0:00-23:00)
- `action_when_cheap` is your function that is called when the half hourly period is among the cheapest
- `action_when_expensive` is your function that is called when the half hourly period is more expensive than the cheapest
- `pricing_strategy` is a custom class you can pass in to act on prices in a more complex way (this is covered in [custom pricing strategies](../advanced//custom-pricing-strategies.md))
- `api_key` a secret key that gives the script access to fetch your most recent tariff (do not push this to git or share with anyone)
- `account_number` your account number for a supported supplier and tariff

<!--start-->
{%
    include-markdown "./octo-api-key.md"
    heading-offset=1
%}
<!--end-->

## How often are my actions called

The actions happen every 30 minutes, if the price is cheap then `action_when_cheap` is called, if it is expensive then `action_when_expensive` is called.

There is a 10 minute grace period on an action missing your current time from when you begin the schedule initially.

## Usage

```py
# main.py
from energy_tariff_scheduler import runner, Price

def action_when_cheap(price: Price):
    print("cheap", price.value)

def action_when_expensive(price: Price)
    print("expensive", price.value)

runner.run_octopus_agile_tariff_schedule(
  considered_price_count=12,
  action_when_cheap=action_when_cheap,
  action_when_expensive=action_when_expensive,
  api_key="YOUR-API-KEY",
  account_number="YOUR-ACCOUNT-NUMBER"
)
```
