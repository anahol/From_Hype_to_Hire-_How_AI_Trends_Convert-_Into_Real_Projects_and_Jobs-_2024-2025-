import requests
import pandas as pd
import datetime
import time

class AIJobAnalyzer:
    def __init__(self, app_id, app_key, country="gb"):
        self.base_url = "https://api.adzuna.com/v1/api/jobs"
        self.app_id = app_id
        self.app_key = app_key
        self.country = country  # "gb" = UK, możesz zmienić np. "us", "pl", "de"

    def fetch_jobs(self, query="AI", max_pages=5):
        """
        Pobiera oferty pracy związane z AI z Adzuna API.
        """
        all_results = []
        print(f"🔍 Szukam ofert dla zapytania: '{query}'...")

        for page in range(1, max_pages + 1):
            url = f"{self.base_url}/{self.country}/search/{page}?app_id={self.app_id}&app_key={self.app_key}&results_per_page=50&what={query}&content-type=application/json"
            r = requests.get(url)
            if r.status_code != 200:
                print(f"❌ Błąd {r.status_code} na stronie {page}")
                break

            data = r.json().get("results", [])
            if not data:
                break

            all_results.extend(data)
            print(f"✅ Strona {page}: {len(data)} ofert (łącznie: {len(all_results)})")
            time.sleep(1)

        print(f"📊 Pobrano łącznie {len(all_results)} ofert.")
        return self._to_dataframe(all_results)

    def _to_dataframe(self, data):
        df = pd.DataFrame([
            {
                "title": d.get("title", ""),
                "company": d.get("company", {}).get("display_name", ""),
                "category": d.get("category", {}).get("label", ""),
                "location": d.get("location", {}).get("display_name", ""),
                "created": d.get("created", ""),
                "salary_min": d.get("salary_min", None),
                "salary_max": d.get("salary_max", None),
                "contract_type": d.get("contract_type", ""),
                "redirect_url": d.get("redirect_url", "")
            }
            for d in data
        ])
        return df

    def analyze_trends(self, df):
        """
        Analiza — najczęstsze tytuły ról i wzrost zapotrzebowania.
        """
        df["created"] = pd.to_datetime(df["created"], errors="coerce")
        df["month"] = df["created"].dt.to_period("M")

        top_titles = df["title"].value_counts().head(20)
        monthly_trend = df.groupby("month").size()

        return top_titles, monthly_trend

    def plot_trends(self, monthly_trend):
        import matplotlib.pyplot as plt

        monthly_trend.plot(kind="line", marker="o", figsize=(10,5))
        plt.title("📈 Trend liczby ofert AI w czasie")
        plt.xlabel("Miesiąc")
        plt.ylabel("Liczba ofert")
        plt.grid(True)
        plt.show()
