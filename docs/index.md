# Welcome to Energy Tariff Scheduler

This is designed to help people easily leverage pricing data provided by Energy Suppliers for use cases such as home automation & internet of things.

Setting this up yourself can be quite a burden, especially if you need the same functionality across applications, this should allow you to simply install, add actions and start automating!

## Do prices even change that much?

Yes they do, the energy prices are driven by supply and demand throughout the day, such as when people are awake or asleep, or fluctuations in generation such as it being windy during the day leading to cheaper electricity from renewable sources which are considerably cheaper than fossil fuels.

Here's an example of the Octopus Agile tariff for 11 days and the schedules generated for a battery being charged when it's cheap under constant load:

<img src="schedule.gif" alt="11 days of battery being charged over constant load" />

<a href="https://www.linkedin.com/pulse/improving-my-portable-battery-charging-strategy-day-ahead-craig-white-7h8ce" target="_blank">Source: Linkedin - Craig White</a>

## Current supported supplier tariffs

Currently each of these tariffs only support import pricings.

- Octopus Agile Tariff
- Octopus Go (EV Tariff)
- Intelligent Octopus Go (EV Tariff)

## Prospective supplier tariffs

This will ultimately be determined by interest.

- Octopus Tracker
- E.ON Next Flex
- EDF GoElectric Overnight
- EDF "Beat the Peak"

## Example usage

If you want to be featured on here make a post on <a href="https://github.com/craigwh10/energy-tariff-scheduler/discussions/new?category=show-and-tell" target="_blank">Show & Tell</a> and I'll get it listed here :)

- <a href="https://battery.craigwh.it" target="_blank">battery.craigwh.it</a>: Raspberry Pi4b using smart scheduling to do battery arbitrage to try keep a server online

## Related links

- <a href="https://github.com/craigwh10/energy-tariff-scheduler" target="_blank">https://github.com/craigwh10/energy-tariff-scheduler</a>
- <a href="https://pypi.org/project/energy-tariff-scheduler/" target="_blank">https://pypi.org/project/energy-tariff-scheduler/</a>

<div style="display: flex; width: 100%; background: #ebebeb; padding: 1em; gap: 1em; border-radius: 0.2em; margin-top: 2em;">
    <a href="./installation" style="flex: 6; text-align: center; color: white; background: var(--md-typeset-a-color); padding: 0.5em 0em;">Next &rarr;</a>
</div>
