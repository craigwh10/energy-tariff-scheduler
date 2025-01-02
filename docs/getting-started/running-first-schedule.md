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

This schedule is blocking so it's recommended to run this in isolated programs, if you really need this to be async <a href="https://github.com/craigwh10/energy-tariff-scheduler/issues/new" target="_blank">raise an issue</a>.

## Setting up actions

In the library we have two available methods that you need to set, `action_when_cheap` and `action_when_expensive`, see below a simple example of how this is set up.

```python
# main.py
from energy_tariff_scheduler import runner, Price

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

If you now run your script it will stay running and you should see changes happening based on your actions, and if you have logs set to `INFO` you should see some logs which indicate the progression of your schedule as well as the full schedule as shown below:

!!! NOTE

    To turn logs on ensure you `import logging` and set the level like this at the top of your code `logging.getLogger("energy_tariff_scheduler").setLevel(logging.INFO)`


```txt
INFO:root:

Todays schedule (this includes already passed jobs):

00:00, action: action_when_expensive, price: 0.0p/kWh
00:30, action: action_when_expensive, price: 4.2p/kWh
01:00, action: action_when_expensive, price: 0.0p/kWh
01:30, action: action_when_cheap, price: -0.84p/kWh
02:00, action: action_when_expensive, price: 0.21p/kWh
02:30, action: action_when_cheap, price: -0.315p/kWh
03:00, action: action_when_cheap, price: -0.0105p/kWh
03:30, action: action_when_cheap, price: -1.365p/kWh
04:00, action: action_when_cheap, price: 0.0p/kWh
04:30, action: action_when_cheap, price: -0.84p/kWh
05:00, action: action_when_cheap, price: -0.903p/kWh
05:30, action: action_when_cheap, price: -1.134p/kWh
06:00, action: action_when_expensive, price: 0.336p/kWh
06:30, action: action_when_expensive, price: 2.1p/kWh
07:00, action: action_when_expensive, price: 4.2p/kWh
07:30, action: action_when_expensive, price: 3.78p/kWh
08:00, action: action_when_cheap, price: -1.05p/kWh
08:30, action: action_when_expensive, price: 4.578p/kWh
09:00, action: action_when_cheap, price: -1.26p/kWh
09:30, action: action_when_expensive, price: 7.707p/kWh
10:00, action: action_when_expensive, price: 3.99p/kWh
10:30, action: action_when_expensive, price: 6.9825p/kWh
11:00, action: action_when_expensive, price: 6.6255p/kWh
11:30, action: action_when_expensive, price: 15.162p/kWh
12:00, action: action_when_expensive, price: 18.9p/kWh
12:30, action: action_when_expensive, price: 19.866p/kWh
13:00, action: action_when_expensive, price: 19.95p/kWh
13:30, action: action_when_expensive, price: 19.152p/kWh
14:00, action: action_when_expensive, price: 19.74p/kWh
14:30, action: action_when_expensive, price: 22.47p/kWh
15:00, action: action_when_expensive, price: 20.16p/kWh
15:30, action: action_when_expensive, price: 20.58p/kWh
16:00, action: action_when_expensive, price: 34.923p/kWh
16:30, action: action_when_expensive, price: 36.54p/kWh
17:00, action: action_when_expensive, price: 38.6925p/kWh
17:30, action: action_when_expensive, price: 38.136p/kWh
18:00, action: action_when_expensive, price: 38.1255p/kWh
18:30, action: action_when_expensive, price: 37.2855p/kWh
19:00, action: action_when_expensive, price: 24.633p/kWh
19:30, action: action_when_expensive, price: 21.735p/kWh
20:00, action: action_when_expensive, price: 23.52p/kWh
20:30, action: action_when_expensive, price: 19.74p/kWh
21:00, action: action_when_expensive, price: 20.58p/kWh
21:30, action: action_when_expensive, price: 20.37p/kWh
22:00, action: action_when_expensive, price: 20.16p/kWh
22:30, action: action_when_expensive, price: 13.65p/kWh
INFO Schedule generated, waiting for jobs to run... 
```

<div style="display: flex; width: 100%; background: #ebebeb; padding: 1em; gap: 1em; border-radius: 0.2em; margin-top: 2em;">
    <a href="../installation" style="flex: 6; text-align: center; color: white; background: var(--md-typeset-a-color); padding: 0.5em 0em;">&larr; Previous</a>
    <a href="../custom-prices-to-include" style="flex: 6; text-align: center; color: white; background: var(--md-typeset-a-color); padding: 0.5em 0em;">Next &rarr;</a>
</div>
