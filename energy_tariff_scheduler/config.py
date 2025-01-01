import inspect

from typing import Callable, Optional, Type
from pydantic import BaseModel, PositiveInt, field_validator

from .prices import Price
from .schedules import PricingStrategy


class ScheduleConfig(BaseModel):
    prices_to_include: PositiveInt | Callable[[list[Price]], int]
    action_when_cheap: Callable[[Price], None]
    action_when_expensive: Callable[[Price], None]
    _pricing_strategy: Optional["PricingStrategy"] = None

    @field_validator("prices_to_include", mode="before")
    def validation_prices_to_include_custom_method(cls, value, info):
        if isinstance(value, float):
            raise SystemExit(
                f"Runner usage error:\n\n"+\
                f"When passing an value into '{info.field_name}' this needs to be an integer greater than 0"
                # TODO: Add a reference to error page
            ) 
        if isinstance(value, int):
            if value < 0:
                raise SystemExit(
                    f"Runner usage error:\n\n"+\
                    f"When passing an value into '{info.field_name}' this needs to be an integer greater than 0"
                    # TODO: Add a reference to error page
                )
        if callable(value):
            sig = inspect.signature(value)
            params = sig.parameters

            if len(params) != 1:
                raise SystemExit(
                    f"Runner usage error:\n\n"+\
                    f"You are missing a required parameter in function '{info.field_name}'"+\
                    f"\n\nFix: '{value.__name__}(prices: list[Price]):'"
                    # TODO: Add a reference to error page
                )

        return value         

    @field_validator("action_when_cheap", "action_when_expensive", mode="before")
    def validate_custom_actions(cls, value, info):
        sig = inspect.signature(value)
        params = sig.parameters

        if len(params) != 1:
            raise SystemExit(
                f"Usage error:\n\n"
                f"You are missing a required parameter in function '{info.field_name}'"+\
                f"\n\nFix: '{value.__name__}(price: Price):'"+\
                f"\n\nCheck other action is like this too otherwise the error will repeat."
                # TODO: Add a reference to error page
            )
        return value

    def add_custom_pricing_strategy(self, pricing_strategy: Type[PricingStrategy]):
        """
        Adds a custom pricing strategy to the configuration.
        You pass in a class, not an instance as the config is injected later.
        ```
        """
        # it's done this way to allow for the custom strategy to access the config
        if not issubclass(pricing_strategy, PricingStrategy):
            raise SystemExit(
                f"Usage error:\n\n"+\
                f"The custom pricing strategy {pricing_strategy.__name__} must inherit from PricingStrategy\n\nException fix: use 'from schedules import PricingStrategy' and 'class {pricing_strategy.__name__}(PricingStrategy):'"
            )

        try:
            instance = pricing_strategy(self)
            # accessing this will raise if it's not implemented
            # it doesn't need a raise NotImplemented within the method, ABC throws by default if
            # it's not implemented as TypeError
            instance.handle_price 
            # This also checks if __init__ is meeting the instance contract so no
            # need for a __init__ sig check. 
        except TypeError:
            raise SystemExit(
                f"Usage error:\n\n"+\
                f"Your custom pricing strategy '{pricing_strategy.__name__}' has improper setup"+\
                f"\n\nFix: Check your implementation for differences"+\
                f"\n\nclass {pricing_strategy.__name__}(PricingStrategy):\n"+\
                f"  def __init__(self, config):\n"+\
                f"      self.config = config\n\n"+\
                f"  def handle_price(self, price: Price, prices: list[Price]):\n"+\
                f"      // your code\n"
            )

        handle_price_sig = inspect.signature(instance.handle_price)
        params = handle_price_sig.parameters

        if len(params) < 2:
            raise SystemExit(
                f"Usage error:\n\n"+\
                f"You are missing required parameters in function 'handle_price' on '{pricing_strategy.__name__}'"+\
                f"\n\nFix: Minimally use 'handle_price(self, price: Price, prices: list[Price]):'"
            )

        self._pricing_strategy = pricing_strategy

        return self
    
    model_config = dict(
        # this is strict for config but not for field classes
        extra="forbid"
    )