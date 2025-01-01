# Energy Tariff Scheduler

Enables smart actions based on daily pricing from utilities.

```sh
pip install energy-tariff-scheduler
```

Full documentation: [https://craigwh10.github.io/energy-tariff-scheduler/](https://craigwh10.github.io/energy-tariff-scheduler/)

## Supported tariff's (so far)

- [Octopus Agile](https://octopus.energy/smart/agile/)

## FAQ

> Do I need my account number?

No, this is using public APIs to fetch the pricing data.

> Why are no actions running between 11pm and 12am for Octopus Agile?

This is due to data availability, Octopus only provide pricing data from 12am-11:00pm.
