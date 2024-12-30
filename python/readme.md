# Domestic Tariff Scheduler Python SDK

```sh
pip install domestic-tariff-scheduler-sdk
```

## Supported tariff's (so far)

- [Octopus Agile](https://octopus.energy/smart/agile/)

## The code

- [prices.py](./prices.py): responsible for fetching data from external APIs and transform for usage based on contracts
- [schedules.py](./schedules.py): responsible for creating schedules and applying pricing logic
- [sdk.py](./sdk.py): responsible for the interface between users and the program
