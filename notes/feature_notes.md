# Not including interpolation as a feature (go/intelli)

I feel like providing a 15 minute interpolation between the price boundaries would limit people if they want to make more complex schedulings between them.

Rather I'm going to opt for only triggering events at the boundaries, but exposing the scheduler object (in 0.0.8) so people can add jobs based to the scheduler at their own discretion.

Prior interpolation code:

```py
def _interpolate_15_minutely_price_data_intelligent_tariff(self, price_data: list[Price]) -> list[Price]:
    """
    Will convert the three prices into 15 min intervals only containing min and max times and what's inbetween.
    """
    # prices arrive latest first

    if len(price_data) != 3:
        raise SystemExit(f"Go (Intelligent) Tariff has returned {len(price_data)} prices not 3, this is unexpected, please report this to https://github.com/craigwh10/energy-tariff-scheduler/discussions/new?category=api-issues with logs")

    date_now = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    new_price_data = []
    lowest_price = min(price_data, key=lambda p: p.value)
    highest_price = max(price_data, key=lambda p: p.value)

    # TODO: Work out the correct number for each of these!

    # total jobs = 96 across 95 periods
    ## 00:00 - 05:15 (low price) - 5:15 hours
    ## jobs occur between 00:00 - 05:30
    for i in range(21 + 1):
        new_price_data.append(
            Price(
                value=lowest_price.value,
                datetime_from=date_now.replace(hour=0, minute=0) + timedelta(minutes=i*15),
                datetime_to=date_now.replace(hour=0, minute=15) + timedelta(minutes=(i+1)*15)
            )
        )

    ## 05:15 - 23:15 (high price) - 18 hours
    for i in range(73 + 1):
        new_price_data.append(
            Price(
                value=highest_price.value,
                datetime_from=date_now.replace(hour=5, minute=15) + timedelta(minutes=i*15),
                datetime_to=date_now.replace(hour=5, minute=30) + timedelta(minutes=(i+1)*15)
            )
        )

    ## 23:15 - 23:45 (low price) - 0.25 hours
    for i in range(2 + 1):
        new_price_data.append(
            Price(
                value=lowest_price.value,
                datetime_from=date_now.replace(hour=23, minute=15) + timedelta(minutes=i*15),
                datetime_to=date_now.replace(hour=23, minute=30) + timedelta(minutes=(i+1)*15)
            )
        )

    return sorted(new_price_data, key=lambda obj: obj.datetime_from)

def _interpolate_15_minutely_price_data_non_intelligent_tariff(self, price_data: list[Price]) -> list[Price]:
    """
    Will convert the three prices into 15 min intervals only containing min and max times and what's inbetween.
    """
    # prices arrive latest first

    if len(price_data) != 3:
        raise SystemExit(f"Go (Regular) Tariff has returned {len(price_data)} prices not 3, this is unexpected, please report this to https://github.com/craigwh10/energy-tariff-scheduler/discussions/new?category=api-issues with logs")

    date_now = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)

    new_price_data = []

    # will only be one low price in data returned
    lowest_price = min(price_data, key=lambda p: p.value)

    # will be two high prices...
    yesterday_high_price = price_data[-1]
    today_high_price = price_data[0]

    ## 00:00 - 00:15 (high price) - 0.15 hours
    for i in range(2 + 1):
        new_price_data.append(
            Price(
                value=yesterday_high_price.value,
                datetime_from=date_now.replace(hour=0, minute=i*15),
                datetime_to=date_now.replace(hour=0, minute=(i+1)*15)
            )
        )

    ## 00:15 - 05:15 (low price) - 5 hours
    for i in range(20 + 1):
        new_price_data.append(
            Price(
                value=lowest_price.value,
                datetime_from=date_now.replace(hour=0, minute=15) + timedelta(minutes=i*15),
                datetime_to=date_now.replace(hour=0, minute=30) + timedelta(minutes=(i+1)*15)
            )
        )
    
    ## 05:15 - 23:45 (high price) - 18:30 hours
    for i in range(74 + 1):
        new_price_data.append(
            Price(
                value=today_high_price.value,
                datetime_from=date_now.replace(hour=5, minute=30) + timedelta(minutes=i*15),
                datetime_to=date_now.replace(hour=5, minute=45) + timedelta(minutes=(i+1)*15)
            )
        )
    
    return sorted(new_price_data, key=lambda obj: obj.datetime_from)

# in run:

todays_prices = self.prices_client.get_prices_for_users_tariff_and_product(
    product_prefix=product_prefix, date_from=date_from, date_to=date_to
)

todays_interpolated_prices = (
    self._interpolate_15_minutely_price_data_intelligent_tariff(todays_prices)
    if self.config.is_intelligent == True
    else self._interpolate_15_minutely_price_data_non_intelligent_tariff(todays_prices)
)

logging.debug(f"Interpolated prices: {todays_interpolated_prices}")

logging.info(f"Generating schedule for {len(todays_interpolated_prices)} prices")

pricing_strategy_class = self.config._pricing_strategy or DefaultPricingStrategy

for price in todays_interpolated_prices:
```
