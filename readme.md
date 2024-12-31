# Domestic Tariff Scheduler

Enables smart actions based on daily pricing from utilities.

```sh
pip install domestic-tariff-scheduler
```

## Supported tariff's (so far)

- [Octopus Agile](https://octopus.energy/smart/agile/)

## The code

- [prices.py](./prices.py): responsible for fetching data from external APIs and transform for usage based on contracts
- [schedules.py](./schedules.py): responsible for creating schedules and applying pricing logic
- [runner.py](./runner.py): responsible for the interface between users and the program

## FAQ

> Do I need my account number?

No, this is using public APIs to fetch the pricing data.
