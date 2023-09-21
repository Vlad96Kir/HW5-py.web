import aiohttp
import asyncio
from datetime import date, timedelta

class PrivatBankAPI:
    def __init__(self):
        self.base_url = "https://api.privatbank.ua/p24api/pubinfo"
        self.currencies = ["USD", "EUR"]

    async def fetch_currency_rate(self, date, currency):
        async with aiohttp.ClientSession() as session:
            url = f"{self.base_url}?json&exchange&coursid=5&date={date}"
            async with session.get(url) as response:
                data = await response.json()
                for item in data:
                    if item["ccy"] == currency:
                        return {
                            currency: {
                                "sale": item["sale"],
                                "purchase": item["buy"]
                            }
                        }

    async def get_currency_rates(self, start_date, end_date, currencies):
        date_range = [end_date - timedelta(days=i) for i in range(10)]
        tasks = [self.fetch_currency_rate(date.strftime("%d.%m.%Y"), currency) for date in date_range for currency in currencies]
        results = await asyncio.gather(*tasks)
        return results

if __name__ == "__main__":
    async def main():
        api = PrivatBankAPI()
        today = date.today()
        end_date = today
        start_date = today - timedelta(days=9)
        currencies = ["USD", "EUR"]
        try:
            rates = await api.get_currency_rates(start_date, end_date, currencies)
            formatted_rates = []
            for i in range(0, len(rates), len(currencies)):
                rate_data = {}
                for j in range(len(currencies)):
                    rate_data[currencies[j]] = rates[i + j][currencies[j]]
                formatted_rates.append({end_date.strftime("%d.%m.%Y"): rate_data})
                end_date -= timedelta(days=1)
            print(formatted_rates)
        except Exception as e:
            print(f"Ошибка при запросе данных: {e}")

    asyncio.run(main())
