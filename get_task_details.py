import requests

def get_task_details(authorization,task_id):
    headers = {
        'authority': 'api.satchelone.com',
        'accept': 'application/smhw.v2021.5+json',
        'accept-language': 'en-GB,en;q=0.8',
        'authorization': authorization,
        'if-none-match': 'W/"dc8297a096f322788b27a805f7f102c8"',
        'origin': 'https://www.satchelone.com',
        'referer': 'https://www.satchelone.com/',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Brave";v="120"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'sec-gpc': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'x-platform': 'web',
    }

    response = requests.get(f'https://api.satchelone.com/api/homeworks/{task_id}', headers=headers)
    return response.json()