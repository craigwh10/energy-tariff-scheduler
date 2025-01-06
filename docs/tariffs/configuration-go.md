## Configuration

- `action_when_cheap` is your function that is called when the half hourly period is among the cheapest
- `action_when_expensive` is your function that is called when the half hourly period is more expensive than the cheapest
- `pricing_strategy` is a custom class you can pass in to act on prices in a more complex way (this is covered in [custom pricing strategies](../advanced/custom-pricing-strategies.md))
- `api_key` a secret key that gives the script access to fetch your most recent tariff (do not push this to git or share with anyone)
- `account_number` your account number for a supported supplier and tariff