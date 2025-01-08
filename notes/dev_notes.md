# Dev notes

Some random notes of things I keep randomly forgetting about.

## Installing packages on local venv

```sh
python .venv/bin/pip install time-machine 
```

## Pytest loglevel

```sh
pytest --log-cli-level=DEBUG 
```

## Local venv python run

```sh
.venv/bin/python ./python/__tests__/run.py
```

## mkdocs

```sh
mkdocs new [dir-name] - Create a new project.
mkdocs serve - Start the live-reloading docs server.
mkdocs build - Build the documentation site.
mkdocs -h - Print help message and exit
```

## schedule library < apschedule

I had a fair few issues using `schedule` library, such as:

- Things you schedule at an exact time dont run the job at that time
- You have to set up a blocking timer and control the clock speed on it which was a pain with testing
- It doesn't cover CRON format and passing in exact dates, only HH:MM format
- It doesn't clear historic jobs (likely due to above)

apschedule resolved all of these for me.

## Misc

Be wary of circular dependencies in classes.

## Uploading to PyPi

Delete `dist` and `.egg-info`.

```sh
.venv/bin/python -m build -v
twine upload dist/*
```

Testing:

```sh
pip uninstall energy_tariff_scheduler
pip install dist/energy_tariff_scheduler-0.0.5-py3-none-any.whl
python ./_test_script.py
```

## Running tests with logs

```sh
pytest __tests__/test_prices.py --log-cli-level=DEBUG
```

## Keeping the software "soft" (aim)

- Start with dependency injection first to start building some objects with clear boundaries
- Then move towards ABC's when you have a shared schema with methods that are consistent across use cases
  - I've already been stung by this, you end up fitting a round peg in a square hole to try just make sure you meet that method name it wants
- Rule of 3 with refactors, don't assume a contract after 2 use cases, start to optimise after 3 appear

I've kept the files agnostic to brand but I'll see how this develops in the future as the files are already getting pretty big, I'll likely find out about this once I introduce another brand. (03/01/2025)

When working with functions relating to dates, don't make the mistake I made and call things "get_today" and have the API in there, have a method that takes in the range and let the implementation that is exposed to other classes be specific to what they need.

Keep things opinionated to begin with, if you don't then you'll be trying to make a schema work for something else, for example ScheduleConfig wont be the same for all schedules, it was made with the AgileTariff in mind first, so make it opinionated to that and then figure out if it should be shared again with the rule of 3.

## If you want a pytest mock function to meet a specific spec

```py
def mock_spec(price):
    return ''

action_when_cheap = mocker.create_autospec(mock_spec)
action_when_cheap.__name__ = "action_when_cheap"
action_when_expensive = mocker.create_autospec(mock_spec)
action_when_expensive.__name__ = "action_when_cheap"
```

This is useful for when you validate certain function specifications in pydantic, as Mocks come with their own broad spec that would fail a test.

## Mocking out tenacity retry decorator

```py
monkeypatch.setattr(
    # name of method on class with decorator.
    client.get_accounts_tariff_and_matched_product_code.retry, "stop", stop_after_attempt(1)
)
```

## Product code and tariff relation

Originally I worked out the tariff-product match like below:

```
    @retry(stop=stop_after_attempt(3), wait=wait_fixed(10))
    def get_products(self) -> list[dict]:
        url = f"https://api.octopus.energy/v1/products/?brand=OCTOPUS_ENERGY&is_business=False"
        response = requests.get(url)
        response.raise_for_status()

        products = response.json()

        logging.debug(f"Full Octopus Agile products: {products}")

        # add pydantic validation here - improving return type

        return products.get("results")
...
        products = self.get_products()

        logging.debug(f"Full Octopus Agile products: {products}")

        agile_products = [product for product in products if product["code"].startswith(product_code_prefix)]

        matched_product = max(agile_products, key=lambda product: SequenceMatcher(None, product["code"], latest_tariff_code).ratio())
```

However this is troublesome because sometimes products end in the future rather than have `None` as their end time, so I'm going to rely on the pattern that the tariff is of the format `{code}-{product}-{region}`, I'm simply going to remove the prefix and suffix.