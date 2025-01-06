# Octopus Intelligent Go

Octopus Intelligent Go is a tariff for EV owners who have an EV or charger that can be controlled in a smart way, this enabled Octopus via the Kraken platform to produce optimised and automated charging schedules, saving you money and letting you plug in and forget.

<!--start-->
{%
    include-markdown "./configuration-go.md"
    heading-offset=1
%}
<!--end-->

<!--start-->
{%
    include-markdown "./octo-api-key.md"
    heading-offset=1
%}
<!--end-->

## How often are my actions called

The actions happen 2 times during the entire day:

- 05:30am when prices are expensive
- 11:30pm when prices are cheap

There is a 10 minute grace period on an action missing your current time from when you begin the schedule initially.

## Usage

```py
# main.py
from energy_tariff_scheduler import runner, Price

def action_when_cheap(price: Price):
    print("cheap", price.value)

def action_when_expensive(price: Price)
    print("expensive", price.value)

runner.run_octopus_go_tariff_schedule(
  prices_to_include=12,
  action_when_cheap=action_when_cheap,
  action_when_expensive=action_when_expensive,
  api_key="YOUR-API-KEY",
  account_number="YOUR-ACCOUNT-NUMBER",
  is_intelligent=True
)
```
