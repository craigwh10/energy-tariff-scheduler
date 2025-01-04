# Welcome to Energy Tariff Scheduler

This is designed to help users easily leverage pricing data provided by Energy Suppliers. It enables scheduled smart actions on connected devices when prices are particularly low or high, simplifying the process of optimizing energy usage in your home.

The library will work for people who just want to plug and play and kick off with the preconfigured price strategies, or if you want, you can provide your own strategy.

## What are tariffs

Tariffs are what Energy Suppliers use to offer pricing options for your electricity usage, these vary between suppliers are specialised to what type of customer you are, such as the Octopus Agile Tariff is set up in a way for people who are concious of the changes in prices throughout the day, allowing them to plan around these.

## Do prices even change that much?

Yes they do, the prices are driven by supply and demand throughout the day, such as when people are awake or asleep, or fluctuations in generation such as it being windy during the day leading to cheaper electricity from renewable sources.

Here's an example of 11 days and a schedule generated from this library for Octopus Agile tariff, for a battery being charged under constant load:

<img src="schedule.gif" alt="11 days of battery being charged over constant load" />

<a href="https://www.linkedin.com/pulse/improving-my-portable-battery-charging-strategy-day-ahead-craig-white-7h8ce" target="_blank">Source: Linkedin - Craig White</a>

## Current supported supplier tariffs

- Octopus Agile Tariff
- Octopus Go (EV Tariff)
- Intelligent Octopus Go (Optimised EV Tariff)

## Prospective supplier tariffs

- Octopus Tracker
- E.ON Next Flex
- EDF GoElectric Overnight
- EDF "Beat the Peak"

## Example usage

If you want to be featured on here make a post on <a href="https://github.com/craigwh10/energy-tariff-scheduler/discussions/new?category=show-and-tell" target="_blank">Show & Tell</a> and I'll get it listed here :)

- <a href="https://battery.craigwh.it" target="_blank">battery.craigwh.it</a>: Raspberry Pi4b using smart scheduling to do battery arbitrage to try keep a server online

## Related links

- <a href="https://github.com/craigwh10/energy-tariff-scheduler" target="_blank">https://github.com/craigwh10/energy-tariff-scheduler</a>

<div style="display: flex; width: 100%; background: #ebebeb; padding: 1em; gap: 1em; border-radius: 0.2em; margin-top: 2em;">
    <a href="./getting-started/installation" style="flex: 6; text-align: center; color: white; background: var(--md-typeset-a-color); padding: 0.5em 0em;">Next &rarr;</a>
</div>
