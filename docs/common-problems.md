# Common problems

## I'm not seeing any logs

This is likely due to not having configured your logger in your python script, follow the example below:

```python
import logging

from energy_tariff_scheduler import PricingStrategy, Price, runner

logging.getLogger("energy_tariff_scheduler").setLevel(logging.INFO)
```

## The runner wont start because of the API not returning data

This library is build around third party API's, these can fail due to many reasons which are out of this libraries control.

I wouldn't reccomend spam retrying the script as this could lead to your IP being blacklisted, the script automatically tries to retry the failed call 3 times (with a 10s delay), it could take upwards of a few days for things to get rectified (as it's people on the other end who need to fix it), so just be patient with it and try every hour or so.

Also, when you see this happen be sure to start a discussion <a href="https://github.com/craigwh10/energy-tariff-scheduler/discussions/new?category=api-issues" target="_blank">on the API issues page</a> to make others aware that this is happening and to help with making the solution more resiliant to these sorts of issues.
