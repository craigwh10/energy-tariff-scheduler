# Domestic Tariff Scheduler

Enables smart actions based on daily pricing from utilities.

```sh
pip install domestic-tariff-scheduler
```

## Supported tariff's (so far)

- [Octopus Agile](https://octopus.energy/smart/agile/)

## Structure

- [prices.py](./prices.py): responsible for fetching data from external APIs and transform for usage based on contracts
- [schedules.py](./schedules.py): responsible for creating schedules and applying pricing logic
- [runner.py](./runner.py): responsible for the interface between users and the program
- [config.py](./config.py): responsible for providing validated user inputted configuration

## FAQ

> Do I need my account number?

No, this is using public APIs to fetch the pricing data.
