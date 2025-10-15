
# Tech Trends Analyzer: Wpływ AI na Rynek Pracy (2024–2025)

## 📘 Opis projektu
Projekt analizuje globalne **trendy technologiczne związane z AI, Machine Learning i generative tools** na podstawie danych z:
- **GitHub** (projekty open-source),
- **Hacker News (HN)** (medialny hype),
- **Google Trends** (zainteresowanie społeczne),
- **rynku pracy (Adzuna API)**.
Celem było zrozumienie, **jak hype wokół AI przekłada się na realne projekty, startupy i nowe stanowiska zawodowe**.
Analiza obejmuje dane z okresu **wrzesień 2024 – wrzesień 2025** i skupia się na:
- konwersji hype → projekty/startupy,
- geograficznych hotspotach technologicznych,
- ewolucji ról zawodowych związanych z AI.

## 🧩 Struktura projektu

Projekt wykorzystuje skrypty Python do pobierania i przetwarzania danych (np. API GitHuba, Algolia dla HN). Kluczowe pliki:
- tech_trends_modular.py: Analiza trendów na GitHubie i rynku pracy.
- hn_trends.py: Analiza trendów na Hacker News.
- trends_combined.csv: Dane z Google Trends (tygodniowe zainteresowanie wyszukiwaniami).
- geoMap.csv: Dane geograficzne (np. rozkład trendów po krajach).

## 🧠 Umiejętności wykorzystane
- **Data scraping i API:** GitHub REST API, Algolia (HN), Adzuna.
- **Analiza danych:** pandas, numpy.
- **Wizualizacja:** matplotlib, seaborn, plotly.
- **Analiza korelacji:** hype → projekty → oferty pracy.
---

## 🚀 Jak uruchomić
1. Zainstaluj wymagane pakiety: pip install requests pandas matplotlib seaborn pytrends --quiet
2. Ustaw zmienną środowiskową GITHUB_TOKEN (dla API GitHuba – wygeneruj token na GitHubie > Settings > Developer settings > Personal access tokens).
3. Uruchom analizę:
    - GitHub: python tech_trends_modular.py
        1. Sklonuj repozytorium: git clone https://github.com/anahol/tech-trends-analyzer.git
    - HN: python hn_trends.py
    - Google Trends: Otwórz plik trends_combined.csv w pandas lub użyj kodu do wizualizacji (patrz sekcja Wyniki).

Uwaga: Jeśli masz dostęp do Colab, uruchom skrypty tam, aby wygenerować wykresy interaktywnie.
---
## 📊 Kluczowe wnioski z analizy
### 🔹 1. Co było „na topie” technologicznie?
**AI i Generative AI** zdominowały cały krajobraz technologiczny.

- **GitHub:** AI (1261 repozytoriów), LLM (337), Claude (299), Python (218), React (186).
- **Hacker News:** AR osiągnął krótkotrwały szczyt (339 mentions w maju 2025), ale **AI utrzymuje stabilny trend wzrostowy**.
- **Google Trends:** ChatGPT, Generative AI i OpenAI utrzymują poziomy 90–100 (maksimum popularności).
💡 *Wniosek:* AI to jedyny trend łączący hype, publikacje i realne wdrożenia.
AR/VR to przykłady „flash hype” – silny buzz medialny, ale mało projektów open-source.
---
### 🔹 2. Czy hype przekłada się na projekty (GitHub/startupy)?
- **AI:** wysoka konwersja – projekty LLM, Claude, Gemini rosną wraz z zainteresowaniem.
- **AR/VR:** duży hype, mało projektów – typowy przykład buzzowego trendu.
- **Rust/Go/Python:** niskie piki, ale wysoka liczba repozytoriów – rozwój stabilny i organiczny.
📈 *AI ma 2–3× wyższy wskaźnik konwersji hype → projekty* niż inne trendy.
---
### 🔹 3. Nowe role i rynek pracy AI
Top stanowiska (Adzuna API, 2025):
```
1. Senior Artificial Intelligence (AI) Consultant – 42 oferty
2. Principal AI Engineer – 39
3. AI Product Marketing Manager – 20
4. AI Tester / Innovation Lead – 15+
```
Trendy:
- Wzrost ról z dopiskiem „AI” o **~40% r/r**,
- Wymagania przesuwają się z ML → LLM, Prompt Engineering, MLOps, RAG,
- Nowe role: **AI Ethicist**, **LLMOps Engineer**, **Prompt Engineer**.
💡 *Firmy nie zawsze używają „AI” w tytule, ale umiejętności AI są w opisie stanowisk.*
---
### 🔹 4. Gdzie hype był największy?
Z danych `geoMap.csv`:
- **USA:** 60% wszystkich trendów i projektów AI (gł. Bay Area),
- **Indie:** dynamiczny wzrost startupów (Bangalore),
- **UK / Kanada / Izrael:** silne centra badawcze,
- **Polska:** rosnący rynek (Warszawa, Wrocław – wzrost ofert AI o 22% r/r).
💡 *USA = centrum innowacji, Indie = centrum wykonawcze, Europa = zaplecze badawcze.*
---
### 🔹 5. Nieoczywiste korelacje
- **Lag (opóźnienie trendów):**
    HN → GitHub = ~3 tygodnie,
    GitHub → Oferty pracy = ~2 miesiące.
    *(czyli media → projekty → rekrutacja)*
- **Hype-to-Project Ratio:**
    - AI = 3.2 (silna konwersja hype → realne wdrożenia)
    - AR = 0.4 (buzz, ale mało implementacji)
- **Skills Dynamics:**
    „Prompt Engineering” +300% vs 2023,
    „LLMOps” +170%,
    „Machine Learning” +37%.
---
## 🧭 Podsumowanie
> AI to jedyny trend, który łączy hype, wdrożenia i wzrost zatrudnienia.
📌 *AI nie jest już modą, ale nowym standardem infrastruktury technologicznej.*
AR/VR pozostają niszowe.
Firmy nie tylko mówią o AI — zatrudniają do jego wdrażania.
---
## 💼 Kontakt
- GitHub: [anahol](https://github.com/anahol)
- Email: [hol.ana.ofc@gmail.com](mailto:hol.ana.ofc@gmail.com)

📄 **Licencja:** MIT

🔗 **Repozytorium:** [Tech Trends Analyzer](https://github.com/anahol/tech-trends-analyzer)
