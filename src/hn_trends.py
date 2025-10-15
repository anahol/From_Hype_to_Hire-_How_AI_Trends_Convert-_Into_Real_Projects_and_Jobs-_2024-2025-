import requests, time, datetime, pandas as pd

class HNTrends:
    def __init__(self, start_date="2024-09-01", end_date=None):
        self.base_url = "https://hn.algolia.com/api/v1/search_by_date"
        self.start_date = datetime.datetime.fromisoformat(start_date)
        self.end_date = datetime.datetime.fromisoformat(end_date) if end_date else datetime.datetime.now()

        # Lista haseł tech – możesz dodać swoje
        self.keywords = [
            "AI", "Artificial Intelligence", "ChatGPT", "OpenAI", "Generative AI",
            "LLM", "LangChain", "Claude", "Gemini", "Sora",
            "Machine Learning", "Deep Learning", "Neural Network",
            "Blockchain", "Crypto", "Web3", "Metaverse", "VR", "AR",
            "Quantum Computing", "Cloud", "AWS", "Azure", "GCP",
            "Rust", "Python", "JavaScript", "TypeScript", "Go", "Swift"
        ]

    def fetch_posts(self):
        """
        Pobiera posty z HN przez Algolia API (od start_date do end_date)
        """
        print("🔄 Pobieram dane z Hacker News...")
        all_hits = []
        page = 0
        while True:
            url = f"{self.base_url}?tags=story&numericFilters=created_at_i>{int(self.start_date.timestamp())},created_at_i<{int(self.end_date.timestamp())}&hitsPerPage=1000&page={page}"
            r = requests.get(url)
            if r.status_code != 200:
                print(f"❌ Błąd {r.status_code}, przerywam...")
                break
            data = r.json()
            hits = data.get("hits", [])
            if not hits:
                break
            all_hits.extend(hits)
            print(f"✅ Strona {page}: {len(hits)} rekordów (łącznie {len(all_hits)})")
            page += 1
            time.sleep(1)  # rate limiting

        df = pd.DataFrame([{
            "id": h.get("objectID"),
            "title": h.get("title", ""),
            "url": h.get("url", ""),
            "points": h.get("points", 0),
            "created_at": pd.to_datetime(h.get("created_at"))
        } for h in all_hits if h.get("title")])

        return df

    def analyze_keywords(self, df):
        """
        Analizuje częstotliwości słów kluczowych w tytułach postów
        """
        results = []
        for kw in self.keywords:
            count = df["title"].str.contains(kw, case=False, na=False).sum()
            if count > 0:
                results.append({"keyword": kw, "mentions": count})

        return pd.DataFrame(results).sort_values("mentions", ascending=False)

    def analyze_trends_over_time(self, df, freq="W"):
        """
        Zlicza wystąpienia słów kluczowych w czasie (np. tygodniowo = 'W', dziennie = 'D')
        """
        all_records = []
        for kw in self.keywords:
            mask = df["title"].str.contains(kw, case=False, na=False)
            subset = df[mask].copy()
            if subset.empty:
                continue
            # grupowanie po tygodniach/dniach
            grouped = subset.groupby(pd.Grouper(key="created_at", freq=freq)).size()
            for date, count in grouped.items():
                all_records.append({"date": date, "keyword": kw, "mentions": count})

        trends = pd.DataFrame(all_records)
        return trends

    def plot_trends(self, trends, top_n=10):
        """
        Wykres trendów dla top-N słów kluczowych (dynamiczny w czasie)
        """
        import matplotlib.pyplot as plt

        top_keywords = (
            trends.groupby("keyword")["mentions"].sum()
            .sort_values(ascending=False)
            .head(top_n).index
        )

        plt.figure(figsize=(14, 8))
        for kw in top_keywords:
            data = trends[trends["keyword"] == kw]
            plt.plot(data["date"], data["mentions"], marker="o", linestyle="-", label=kw)

        plt.legend()
        plt.title(f"Hacker News – trendy technologiczne (top {top_n})")
        plt.xlabel("Czas")
        plt.ylabel("Liczba wzmianek w danym okresie")
        plt.grid(True, linestyle="--", alpha=0.6)
        plt.show()

    def run(self, save_csv=True):
        df = self.fetch_posts()
        print(f"📊 Pobrano {len(df)} postów z HN.")

        if df.empty:
            print("⚠️ Brak danych.")
            return None, None

        trends = self.analyze_keywords(df)
        if save_csv:
            df.to_csv("hn_posts_raw.csv", index=False)
            trends.to_csv("hn_trends_summary.csv", index=False)
            print("💾 Zapisano pliki: hn_posts_raw.csv i hn_trends_summary.csv")

        return df, trends
