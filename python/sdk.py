from schedules import OctopusAgileScheduleProvider, ScheduleConfig, PricingStrategy
from prices import OctopusAgilePricesClient, Price

from typing import Callable, Optional


class AgileActionsSDK:
    """
    Current tariff support:
    - [Octopus Agile](https://octopus.energy/smart/agile/)
    """
    def run_octopus_agile_tariff_schedule(
            self,
            prices_to_include: int | Callable[[list[Price]], int],
            action_when_cheap: Callable[[Optional[Price]], None],
            action_when_expensive: Callable[[Optional[Price]], None],
            pricing_strategy: Optional[PricingStrategy] = None
        ):
        """
        Runs a schedule based on the Octopus Agile tariff.
        
        Args:
            prices_to_include (int | Callable[[list[Price]], int]): The number of prices to include or a callable
                that determines the number dynamically.
            action_when_cheap (Callable[[Optional[Price]], None]): Action to execute when the price is considered cheap.
            action_when_expensive (Callable[[Optional[Price]], None]): Action to execute when the price is considered expensive.
            pricing_strategy (Optional[PricingStrategy]): Custom pricing strategy to handle the prices.

        Returns:
            OctopusAgileScheduleProvider: The schedule provider instance configured with the given settings.
        """

        OctopusAgileScheduleProvider(
            prices_client=OctopusAgilePricesClient(),
            config=ScheduleConfig(
                prices_to_include,
                action_when_cheap,
                action_when_expensive,
                pricing_strategy
            )
        )
