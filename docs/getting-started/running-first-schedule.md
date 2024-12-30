# Running your first schedule

## Configuration

- `prices_to_include` is the number of the cheapest half hourly periods that you want to include
  - this can be a function (as defined in [custom prices to include](./custom-prices-to-include.md))
  - or simply just an integer value between `0` and `46` ( a full day 0:00-23:00)
- `action_when_cheap` is your function that is called when the half hourly period is among the cheapest
- `action_when_expensive` is your function that is called when the half hourly period is more expensive than the cheapest
- `pricing_strategy` is a custom class you can pass in to act on prices in a more complex way (this is covered in [custom pricing strategies](./custom-pricing-strategies.md))

## Setting up actions

In the SDK we have two available methods that you need to set, `action_when_cheap` and `action_when_expensive`, see below a simple example of how this is set up.

```python
# main.py
from domestic_tariff_scheduler_sdk import tariff, Price

def action_when_cheap(price: Price):
    print("cheap", price.value)

def action_when_expensive(price: Price)
    print("expensive", price.value)

tariff.run_octopus_agile_tariff_schedule(
        prices_to_include: 12,
        action_when_cheap: action_when_cheap,
        action_when_expensive: action_when_expensive,
)
```

You can see here in this example that there are two function I have created, one that runs when the prices are cheap, which in this case will run a simple print in the 12 cheapest half hourly prices of the day and will run a simple print in the expensive other 44 periods of the day.

You can change these methods to do whatever you like, a common example is using a smart plug HTTP API's to make them turn on and off during those periods.

If you now run your script it will stay running and you should see in your logs which periods it is running and with what time like below.

```sh
$ python main.py
INFO Here is your schedule...
INFO 00:00 action_when_cheap
INFO 00:30 action_when_cheap
INFO 01:30 action_when_cheap
INFO 02:00 action_when_cheap
INFO 02:30 action_when_expensive
...
```
