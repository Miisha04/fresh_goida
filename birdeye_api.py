import requests

def fetch_ohlcv_data(mint):
    url = "https://public-api.birdeye.so/defi/ohlcv"
    params = {
        "address": mint,
        "type": "1D",
        "time_from": "0",
        "time_to": "10000000000"
    }
    headers = {
        "accept": "application/json",
        "x-chain": "solana",
        "X-API-KEY": "061eef71caa947a3b82c8dbda8bbdf63"
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # Проверка на HTTP ошибки

        data = response.json()
        
        # Извлекаем значение 'h' из ответа и сохраняем в переменную ath
        ath = data.get("data", {}).get("items", [])[0].get("h") if data.get("data", {}).get("items") else None
        
        return round(ath, 6)

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP ошибка: {http_err}")
    except requests.exceptions.RequestException as err:
        print(f"Ошибка запроса: {err}")
    except Exception as e:
        print(f"Ошибка: {e}")

# # Пример вызова функции
# ath = fetch_ohlcv_data("46MkF1CgTL4cWWE1P9v28K25Z8ehqnpbpTJ6FMGupump")
# if ath is not None:
#     print("ATH значение:", ath)
# else:
#     print("Не удалось получить ATH значение.")
