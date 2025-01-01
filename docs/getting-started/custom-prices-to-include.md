# Using custom price_to_include functions

As touched on in [running first schedule page](./running-first-schedule.md#running-your-first-schedule), this introduces the `number_to_include` configuration parameter, mentioning that it can either be a positive integer value or a custom function, this is going to show you how to use this method to select prices programattically.

The function must always return an integer otherwise it will fail, this integer is the number of prices the pricing strategy will act on.

## Example

```python
# main.py
from energy_tariff_scheduler import runner, Price

def action_when_cheap(price: Price):
    print("cheap", price.value)

def action_when_expensive(price: Price)
    print("expensive", price.value)

def prices_to_include(prices: list[Price]):
    # only get the count where sum cost is no greater than 15p/kWh
    # i.e 3.0 + 5.0 + 3.0 + 4.0 = 15 (wont include 8.0)

    total = 0
    count = 0
    sorted_prices = sorted(prices, key=lambda obj: min(obj.value, obj.value))
    for price in sorted_prices:
        total += price.value
        count += 1
        if total >= 15:
            break 

    return count
    

runner.run_octopus_agile_tariff_schedule(
        prices_to_include: prices_to_include,
        action_when_cheap: action_when_cheap,
        action_when_expensive: action_when_expensive,
)
```

In this setup I've created a theoretical scenario where I only want to spend take advantage of 15p/kWh total of prices, and work out from the available prices how many prices that is, which the strategy will then use.

<div style="display: flex; width: 100%; background: #ebebeb; padding: 1em; gap: 1em; border-radius: 0.2em; margin-top: 2em;">
    <a href="../running-first-schedule" style="flex: 6; text-align: center; color: white; background: var(--md-typeset-a-color); padding: 0.5em 0em;">&larr; Previous</a>
    <a href="../custom-pricing-strategies" style="flex: 6; text-align: center; color: white; background: var(--md-typeset-a-color); padding: 0.5em 0em;">Next &rarr;</a>
</div>
