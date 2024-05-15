from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# @app.route('/price', methods=['POST'])
# def price():
    
#     slack_response = {
#         'USD': f'${int(get_gold_price())} USD',  # Visible to all users in the channel
#     }
#     return jsonify(slack_response)

def get_gold_price():
    url = "https://data-asg.goldprice.org/dbXRates/USD"

    payload = {}
    headers = {
    'accept': '*/*',
    'accept-language': 'vi,en-US;q=0.9,en;q=0.8',
    'if-none-match': 'W/"f2-+955B9Q/+SSh5La/VW5m+xhGks8"',
    'origin': 'https://goldprice.org',
    'priority': 'u=1, i',
    'referer': 'https://goldprice.org/',
    'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Cookie': 'lagrange_session=5e4903e1-27f9-4f5b-b732-7735b08b110c; wcid=WaMkg+sT7tgBAAAB'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    price = response.json()['items'][0]['xauPrice']
    return price

@app.route('/price', methods=['POST'])
def vnd_price():
    url = "https://api.wise.com/v1/rates?source=USD&target=VND"

    payload = {}
    headers = {
    'accept': '*/*',
    'accept-language': 'vi,en-US;q=0.9,en;q=0.8',
    'authorization': 'Basic OGNhN2FlMjUtOTNjNS00MmFlLThhYjQtMzlkZTFlOTQzZDEwOjliN2UzNmZkLWRjYjgtNDEwZS1hYzc3LTQ5NGRmYmEyZGJjZA==',
    'content-type': 'application/json',
    'origin': 'https://wise.com',
    'priority': 'u=1, i',
    'referer': 'https://wise.com/',
    'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Cookie': '__cf_bm=96FkWauNFQkRW4acZNsNaJtzo_cZxXPMSqb1eW1uAgk-1715762315-1.0.1.1-a16M9yAY9AoYH8egWZbwZ3AM6lXDRmGtswp_a8fA_De7icYiiE2KDRMTsrBX2jrHyUbN79NEIrfint2JpMXrb4Nt_B2hMXe6mv8CYJ8qfI8'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    rate = response.json()[0]['rate']
    gold_price = get_gold_price()
    vnd_price = ((101/100 * 1.20565 * rate) + 60) * gold_price
    vnd_price_formatted = "{:,}".format(int(vnd_price))
    slack_response = {
        "USD": f"${int(gold_price)} USD",
        'VND': f'{vnd_price_formatted} VND',  # Visible to all users in the channel
    }
    return jsonify(slack_response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
