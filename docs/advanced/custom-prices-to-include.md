# Custom price_to_include functions

A custom `price_to_include` function must always return an integer otherwise it will fail, this integer is the number of prices the pricing strategy will act on.

## Example (Octopus Agile)

```python
# main.py
from energy_tariff_scheduler import runner, Price

def action_when_cheap(price: Price):
    print("cheap", price.value)

def action_when_expensive(price: Price)
    print("expensive", price.value)

def considered_price_count(prices: list[Price]):
    # only get the count where sum cost is no greater than 15p/kWh
    # e.g if first 4 prices are 3.0 + 5.0 + 3.0 + 4.0 = 15 (it wont include rest)

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
    considered_price_count=considered_price_count,
    action_when_cheap=action_when_cheap,
    action_when_expensive=action_when_expensive,
    api_key="YOUR-API-KEY",
    account_number="YOUR-ACCOUNT-NUMBER"
)
```

In this setup I've created a theoretical scenario where I only want to spend take advantage of 15p/kWh total of prices, and work out from the available prices how many prices that is, which the strategy will then use.
