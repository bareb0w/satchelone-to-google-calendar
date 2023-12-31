import requests


def get_todos(authorization, from_date, to_date):
    headers = {
        "authority": "api.satchelone.com",
        "accept": "application/smhw.v2021.5+json",
        "accept-language": "en-GB,en;q=0.8",
        "authorization": authorization,
        "if-none-match": 'W/"2cf570b02d680179150fcb1441d7f1ed"',
        "origin": "https://www.satchelone.com",
        "referer": "https://www.satchelone.com/",
        "sec-ch-ua": '"Not_A Brand";v="8", "Chromium";v="120", "Brave";v="120"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Linux"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "sec-gpc": "1",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "x-platform": "web",
    }

    params = {
        "add_dateless": "true",
        "from": from_date,
        "to": to_date,
    }
    # params = {'add_dateless':'true'}

    response = requests.get(
        "https://api.satchelone.com/api/todos", params=params, headers=headers
    )
    return response.json()


# print(len(get_todos('2023-12-31','2024-01-14')['todos']))
