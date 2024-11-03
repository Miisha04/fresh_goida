from moralis import sol_api

API_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJub25jZSI6Ijk4OTMzNmNjLTRmZTAtNDg1Mi1hMjNkLTA4MTNhOWFkMTE2NSIsIm9yZ0lkIjoiNDEzMDEzIiwidXNlcklkIjoiNDI0NDM4IiwidHlwZUlkIjoiZTRhYmIxNzAtMjExZi00NjEzLTljOTMtZGM2MmJlMTVjY2Q2IiwidHlwZSI6IlBST0pFQ1QiLCJpYXQiOjE3Mjk2ODc4NDUsImV4cCI6NDg4NTQ0Nzg0NX0.r1OrH3Pak6vu4qH-yDinY5uy7qycZ3pWp4VPVKn4gNk'

def get_token_price(mint):
    params = {
        "network": "mainnet",
        "address": mint
    }

    try:
        result = sol_api.token.get_token_price(
            api_key=API_KEY,
            params=params,
        )
        
        # Извлекаем текущую цену токена
        current_price = result.get('usdPrice')
        
        # Проверяем, удалось ли получить цену
        if current_price is None:
            print("Цена не найдена.")
            return None
        
        return round(current_price, 6)

    except Exception as e:
        print(f"Ошибка при получении цены токена: {e}")
        return None

# # Пример вызова функции
# mint_address = "42ZiZ9vA8L6BKcJMi4SjebKsgisyEyztBdYn646Ppump"
# price = get_token_price(mint_address)
# if price is not None:
#     print("Текущая цена токена:", price)
# else:
#     print("Не удалось получить цену токена.")
