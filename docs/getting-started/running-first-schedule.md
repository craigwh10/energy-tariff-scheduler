# Running your first schedule

## Configuration

- `prices_to_include` is the number of the cheapest half hourly periods that you want to include
    * this can be a function (as defined in [custom prices to include](./custom-prices-to-include.md))
    * or simply just an integer value between `0` and `46` ( a full day 0:00-23:00)
- `action_when_cheap` is your function that is called when the half hourly period is among the cheapest
- `action_when_expensive` is your function that is called when the half hourly period is more expensive than the cheapest
- `pricing_strategy` is a custom class you can pass in to act on prices in a more complex way (this is covered in [custom pricing strategies](./custom-pricing-strategies.md))

## When does this run?

You can kick off your schedule at any point in the day, and it will ignore the previous half hourly periods before then, once the schedule for the current day is completed then it will keep running, until you exit the program.

This schedule is blocking so it's reccomended to run this in isolated programs, if you really need this to be async raise an <a href="https://github.com/craigwh10/domestic-tariff-scheduler/issues/new" target="_blank">raise an issue</a>.

## Setting up actions

In the library we have two available methods that you need to set, `action_when_cheap` and `action_when_expensive`, see below a simple example of how this is set up.

```python
# main.py
from domestic_tariff_scheduler import runner, Price

def action_when_cheap(price: Price):
    print("cheap", price.value)

def action_when_expensive(price: Price)
    print("expensive", price.value)

runner.run_octopus_agile_tariff_schedule(
  prices_to_include: 12,
  action_when_cheap: action_when_cheap,
  action_when_expensive: action_when_expensive,
)
```

You can see here in this example that there are two function I have created, one that runs when the prices are cheap, which in this case will run a simple print in the 12 cheapest half hourly prices of the day and will run a simple print in the expensive other 44 periods of the day.

You can change these methods to do whatever you like, a common example is using a smart plug HTTP API's to make them turn on and off during those periods.

If you now run your script it will stay running and you should see some logs which indicate the progression of your schedule.

<div style="display: flex; width: 100%; background: #ebebeb; padding: 1em; gap: 1em; border-radius: 0.2em; margin-top: 2em;">
    <a href="../installation" style="flex: 6; text-align: center; color: white; background: var(--md-typeset-a-color); padding: 0.5em 0em;">&larr; Previous</a>
    <a href="../custom-prices-to-include" style="flex: 6; text-align: center; color: white; background: var(--md-typeset-a-color); padding: 0.5em 0em;">Next &rarr;</a>
</div>

<!-- ```sh
$ python main.py
INFO Generating schedule for 46 prices
INFO Time: 00:00, Action: action_when_cheap, Price: 4p/kWh
INFO Time: 00:30, Action: action_when_cheap, Price: 8p/kWh
INFO Time: 01:00, Action: action_when_cheap, Price: 18p/kWh
INFO Time: 01:30, Action: action_when_cheap, Price: 12p/kWh
INFO Time: 02:00, Action: action_when_expensive, Price: 50p/kWh
...
INFO Schedule generated, waiting for jobs to run... 
``` -->
