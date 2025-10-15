import os
import time
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import json
from typing import List, Dict

class TechTrendsAnalyzer:
    def __init__(self):
        self.github_token = os.getenv("GITHUB_TOKEN")

    def get_massive_github_data(self) -> pd.DataFrame:
        """
        Pobiera dane z ostatniego roku, dzieląc go na miesięczne zapytania, aby obejść limity API.
        """
        all_data = []
        today = datetime.now()

        for i in range(12):
            end_date = today - timedelta(days=30 * i)
            start_date = today - timedelta(days=30 * (i + 1))

            query = f"created:{start_date.strftime('%Y-%m-%d')}..{end_date.strftime('%Y-%m-%d')}"

            print(f"🔄 Pobieranie danych dla okresu: {start_date.strftime('%Y-%m-%d')} - {end_date.strftime('%Y-%m-%d')}")

            data = self.fetch_repos_batch(query=query, max_pages=10)
            all_data.extend(data)

        df = pd.DataFrame(all_data)
        if not df.empty:
            df = df.drop_duplicates(subset=['full_name'])
        return df

    def fetch_repos_batch(self, query: str, sort: str = "stars", max_pages: int = 5) -> list:
        """
        Pobiera batch repozytoriów z paginacją i obsługą rate limiting.
        """
        headers = {"Authorization": f"token {self.github_token}"} if self.github_token else {}
        repos = []

        for page in range(1, max_pages + 1):
            try:
                url = "https://api.github.com/search/repositories"
                params = {
                    "q": query,
                    "sort": sort,
                    "order": "desc",
                    "per_page": 100,
                    "page": page
                }

                response = requests.get(url, headers=headers, params=params)

                remaining = int(response.headers.get('X-RateLimit-Remaining', 0))
                if remaining < 10:
                    reset_time = int(response.headers.get('X-RateLimit-Reset', 0))
                    wait_time = reset_time - time.time() + 60
                    print(f"⏳ Osiągnięto limit zapytań. Czekam {wait_time/60:.1f} minut...")
                    time.sleep(max(wait_time, 0))

                response.raise_for_status()
                data = response.json()
                items = data.get("items", [])
                if not items:
                    break

                for repo in items:
                    repos.append({
                        "name": repo["name"],
                        "full_name": repo["full_name"],
                        "description": repo["description"] or "",
                        "language": repo["language"] or "Unknown",
                        "stars": repo["stargazers_count"],
                        "forks": repo["forks_count"],
                        "created_at": repo["created_at"],
                        "topics": repo.get("topics", [])
                    })

                print(f"✅ Strona {page}: {len(items)} repozytoriów (Całkowita liczba: {len(repos)})")
                time.sleep(1.5)
            except Exception as e:
                print(f"❌ Błąd na stronie {page}: {e}")
                time.sleep(5)
                break

        return repos

    def analyze_tech_keywords_trends(self, df: pd.DataFrame, text_column: str) -> pd.DataFrame:
        tech_keywords = [
            "AI", "Machine Learning", "LLM", "OpenAI", "ChatGPT", "GPT", "Gemini",
            "Claude", "Neural Network", "Deep Learning", "TensorFlow", "PyTorch",
            "Python", "JavaScript", "TypeScript", "Go", "Rust", "Java", "C++",
            "Swift", "Kotlin", "PHP", "Ruby", "C#", ".NET",
            "React", "Vue", "Angular", "NextJS", "Svelte", "Astro", "Nuxt",
            "Node.js", "FastAPI", "Django", "Express", "Spring",
            "Docker", "Kubernetes", "AWS", "Azure", "GCP", "Terraform",
            "PostgreSQL", "MongoDB", "Redis", "MySQL", "SQLite",
            "Blockchain", "Web3", "GraphQL", "REST API", "Microservices",
            "Serverless", "Edge Computing", "WebAssembly", "PWA"
        ]
        keyword_counts = {}
        for keyword in tech_keywords:
            pattern = rf'\b{keyword}\b'
            count = df[text_column].str.contains(pattern, case=False, na=False, regex=True).sum()
            if count > 0:
                keyword_counts[keyword] = count
        trend_df = pd.DataFrame(list(keyword_counts.items()),
                                 columns=['Technology', 'Mentions'])
        return trend_df.sort_values('Mentions', ascending=False)

    def create_tech_trends_visualization(self, github_data: pd.DataFrame, trend_data: pd.DataFrame):
        plt.style.use('seaborn-v0_8-whitegrid')
        fig, axes = plt.subplots(1, 2, figsize=(18, 7))

        top_15 = trend_data.head(15)
        sns.barplot(ax=axes[0], data=top_15, y='Technology', x='Mentions', palette='viridis', hue='Technology', legend=False)
        axes[0].set_title('Top 15 Most Mentioned Technologies (GitHub)', fontsize=16)
        axes[0].set_xlabel('Number of Mentions', fontsize=12)
        axes[0].set_ylabel('Technology', fontsize=12)

        if not github_data.empty and 'created_at' in github_data.columns:
            github_data['created_at'] = pd.to_datetime(github_data['created_at']).dt.tz_localize(None)
            github_data['month'] = github_data['created_at'].dt.to_period('M')
            monthly_repos = github_data.groupby('month').size().reset_index(name='count')
            monthly_repos['month'] = monthly_repos['month'].astype(str)
            sns.lineplot(ax=axes[1], x='month', y='count', data=monthly_repos, marker='o', color='dodgerblue')
            axes[1].set_title('Number of GitHub Repositories Over Time', fontsize=16)
            axes[1].set_xlabel('Month', fontsize=12)
            axes[1].set_ylabel('Number of Repos', fontsize=12)
            axes[1].tick_params(axis='x', rotation=45)
        else:
            axes[1].text(0.5, 0.5, 'Brak danych GitHub do analizy czasowej', ha='center', va='center', fontsize=14, style='italic', color='gray')
            axes[1].set_title('GitHub Trends Over Time', fontsize=16)
            axes[1].set_xlabel('Month')

        plt.tight_layout()
        plt.show()

    def generate_portfolio_report(self, github_data: pd.DataFrame) -> Dict:
        report = {
            "summary": {
                "github_repos_analyzed": len(github_data),
                "date_generated": datetime.now().isoformat()
            },
            "top_languages": github_data['language'].value_counts().head(10).to_dict(),
            "most_starred_repos": github_data.nlargest(5, 'stars')[['name', 'language', 'stars']].to_dict('records'),
            "trending_topics": []
        }
        all_topics = []
        for topics in github_data['topics']:
            if topics:
                all_topics.extend(topics)
        topic_counts = pd.Series(all_topics).value_counts().head(10)
        report["trending_topics"] = topic_counts.to_dict()
        return report

class JobMarketAnalyzer:
    def __init__(self):
        self.justjoin_api = "https://api.justjoin.it/v2/user-panel/offers"

    def fetch_job_offers(self, technology: str = None) -> pd.DataFrame:
        try:
            headers = {"User-Agent": "Mozilla/5.0 (compatible; TechTrendsAnalyzer/1.0)"}
            response = requests.get(self.justjoin_api, headers=headers)
            response.raise_for_status()
            offers = response.json()
            job_data = []
            for offer in offers.get('data', []):
                skills = [skill['name'] for skill in offer.get('skills', [])]
                job_data.append({
                    'title': offer.get('title'),
                    'company': offer.get('company_name'),
                    'location': offer.get('city'),
                    'experience': offer.get('experience_level'),
                    'skills': skills,
                    'salary_min': offer.get('employment_types', [{}])[0].get('salary', {}).get('from'),
                    'salary_max': offer.get('employment_types', [{}])[0].get('salary', {}).get('to'),
                    'published_at': offer.get('published_at')
                })
            return pd.DataFrame(job_data)
        except Exception as e:
            print(f"Błąd pobierania ofert pracy: {e}")
            return pd.DataFrame()

    def analyze_job_market_trends(self, jobs_df: pd.DataFrame) -> pd.DataFrame:
        all_skills = []
        for skills in jobs_df['skills']:
            if skills:
                all_skills.extend(skills)
        skill_counts = pd.Series(all_skills).value_counts()
        return pd.DataFrame({
            'Skill': skill_counts.index,
            'Job_Postings': skill_counts.values
        })

# Główna funkcja programu
def main():
    analyzer = TechTrendsAnalyzer()

    print("🔄 Pobieranie dużej ilości danych z GitHub...")

    github_data = analyzer.get_massive_github_data()

    if not github_data.empty:
        print(f"✅ GitHub: {len(github_data)} unikalnych repozytoriów")
        tech_trends = analyzer.analyze_tech_keywords_trends(github_data, 'description')
        print("\n📊 Top 10 technologii (GitHub repos):")
        print(tech_trends.head(10))
    else:
        tech_trends = pd.DataFrame(columns=['Technology', 'Mentions'])

    analyzer.create_tech_trends_visualization(github_data, tech_trends)

    report = analyzer.generate_portfolio_report(github_data)
    with open('tech_trends_report.json', 'w') as f:
        json.dump(report, f, indent=2)
    print("✅ Raport wygenerowany: tech_trends_report.json")
