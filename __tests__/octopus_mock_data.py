import json

def modify_datetimes_to_be_date(date: str):
    with open('./__tests__/mock_full_octopus_data.json') as f:
        data = json.load(f)

        return {
                **data,
                "results": [
                    {
                        **result,
                        "valid_from": f"{date}T{result['valid_from'].split('T')[1]}",
                        "valid_to": f"{date}T{result['valid_to'].split('T')[1]}" 
                    } for result in data["results"]
                ]
        }