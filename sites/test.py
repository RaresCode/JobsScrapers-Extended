



import requests

url = 'https://kei.wd1.myworkdayjobs.com/wday/cxs/kei/GlobalKimballCareers/jobs'

headers = {
    'Accept': 'application/json'
}

json_data = {
    'appliedFacets': {
        'locations': [
            'fbecff70217d10da6c755135d69d6c29',
        ],
    },
    'limit': 20,
    'offset': 0,
    'searchText': '',
}

x = requests.post(url, headers=headers, json=json_data).json()['jobPostings']

print(x)