# 🧠 Skills Library — po polsku

**Otwarty, powtarzalny katalog najlepszych open-source'owych skilli agentowych (`SKILL.md`) z GitHuba + szybka, dwujęzyczna strona, żeby naprawdę ich używać w swoim agencie AI.**

[🇬🇧 English version](README.md) · [📄 Pełny katalog](CATALOG.md) · [🤖 llms.txt](llms.txt) · [📊 JSON API](data/catalog.json) · [🌐 Strona](index.html) · [📖 Instalacja](docs/INSTALL.md)

---

## Po co to jest

Na GitHubie są tysiące repozytoriów z `SKILL.md`. Żeby znaleźć te warte uwagi, trzeba otworzyć dziesiątki README, zgadywać, które projekty są żywe, które mają prawdziwą licencję, a które są tylko 400 wygenerowanymi kopiami tego samego szablonu.

Skills Library rozwiązuje ten problem:

- 🔎 **Prawdziwy research po GitHub API**: wyszukiwanie repozytoriów, metadane, rekursywne drzewa git i prawdziwy frontmatter `SKILL.md`. Żadnych ręcznie wpisanych gwiazdek.
- ✅ **Zweryfikowane skille**: każdy zaindeksowany skill ma realnie pobrany plik `SKILL.md` ze sparsowanymi polami `name` / `description`. Deduplikujemy kopie w `.claude/`, `.cursor/`, `.agents/` itd.
- ⚖️ **Jasne licencje**: MIT / Apache / CC-BY-SA / licencje per-skill / *brak licencji* są pokazane wprost, zamiast chować się za słowem „open source".
- 🛡️ **Uczciwy model zaufania**: heurystyki oznaczają skille z dołączonymi skryptami, `allowed-tools` lub komendami shell/sieć. Skille security oraz opisy głównie po chińsku mają wyraźne notatki o bezpiecznym użyciu. Nigdy nie twierdzimy, że cudzy skill jest „bezpieczny".
- 📦 **Pakiety startowe**: gotowe zestawy dla solidnego agenta kodującego, frontendu, dokumentów, security, researchu danych, produktu i oficjalnych zestawów dostawców.
- 🤖 **Dane dla maszyn**: `data/catalog.json`, `data/catalog.js`, `data/discovered.json`, `llms.txt` i JSON Schema. Samo repo jest też instalowalnym skillem: [`skills/skill-finder`](skills/skill-finder/SKILL.md).
- 🌍 **Dwa języki, zero zależności**: strona to czysty HTML/CSS/JS z PL/EN, trybem ciemnym/jasnym, wyszukiwaniem, filtrami, zapisanymi skillami, deep linkami i komendami instalacji jednym kliknięciem.

> Indeksujemy metadane i linkujemy do oryginałów — **nie kopiujemy** cudzych treści skilli do tego repozytorium. Każdy projekt zachowuje swoją licencję i autorstwo.

---

## Aktualne liczby

| Repozytoria | Pliki `SKILL.md` | Unikalne foldery skilli | Kolekcje kuratowane | Zaindeksowane skille | Wygenerowano |
| ---: | ---: | ---: | ---: | ---: | --- |
<!-- STATS:START -->
| 472 | 108,698 | 93,362 | 124 | 976 | 2026-11-25 |
<!-- STATS:END -->

*„Pliki SKILL.md" liczą każdą ścieżkę, także kopie w kilku folderach agentów. „Unikalne foldery" deduplikują po nazwie folderu w jednym repozytorium. Zobacz [metodykę](docs/METHODOLOGY.md).*

---

## Start w 60 sekund

```bash
# 1. Uruchom stronę lokalnie (bez npm install i bez builda)
python3 -m http.server 4173 --bind 0.0.0.0
# otwórz http://localhost:4173

# 2. Zainstaluj jeden skill
npx skills add https://github.com/anthropics/skills/tree/main/skills/pdf

# 3. Albo całą kolekcję ekspercką
npx skills add obra/superpowers

# 4. Albo znajdź właściwą komendę naszym helperem
python3 scripts/query_catalog.py search "react best practices" --limit 5
python3 scripts/install.py search "pdf"
```

`npx skills` to open-source'owy [CLI Vercel Labs](https://github.com/vercel-labs/skills). Wykrywa Claude Code, Codex, Cursor, Gemini CLI, Copilot, OpenCode i wiele innych agentów i instaluje do właściwego folderu. Wymaga Node.js 22.20+.

---

## Co dostajesz

1. **Przeszukiwalną stronę** — [`index.html`](index.html): full-text, filtry kategorii/licencji/oficjalności, sortowanie, zapisane skille, panel szczegółów z czterema wariantami instalacji, pakiety startowe, PL/EN, dark/light, deep linki (`?q=pdf&view=skills&lang=pl`) i macierz kompatybilności agentów.
2. **Prawdziwą awesome-listę** — [`CATALOG.md`](CATALOG.md): wybór redakcji, każda kuratowana kolekcja z uzasadnieniem oraz repozytoria znalezione automatycznie.
3. **API danych dla agentów** — [`data/catalog.json`](data/catalog.json), helper `scripts/query_catalog.py`, [`llms.txt`](llms.txt) i [`data/schema.json`](data/schema.json).
4. **Skill-finder** — zainstaluj [`skills/skill-finder`](skills/skill-finder/SKILL.md), a Twój agent najpierw sprawdzi ten katalog, zanim odpowie „jak to zrobić?".

---

## Kryteria

| Sygnał | Reguła |
| --- | --- |
| Format | Co najmniej jeden dokładny plik `SKILL.md` w drzewie repo |
| Źródło | Publiczne repo GitHub, nie zarchiwizowane, nie fork |
| Warstwa kuratowana | Ręcznie sprawdzona, z kategorią, notatką i przypisaniem do pakietów |
| Warstwa odkryta | Automatycznie z wyszukiwarki GitHub, ≥ 2 000 gwiazdek, push w ciągu 2 lat, wyraźnie o skillach, licencja widoczna — **bez ręcznej weryfikacji** |
| Licencja | Z API GitHub; `NOASSERTION`, licencje per-skill i brak licencji są oznaczone |
| Bezpieczeństwo | Weryfikujemy metadane i istnienie pliku. Nie uruchamiamy i nie audytujemy zachowania cudzych skilli |

Więcej: [`docs/METHODOLOGY.md`](docs/METHODOLOGY.md) · [`SECURITY.md`](SECURITY.md)

---

## Odświeżanie danych

```bash
export GITHUB_TOKEN=...        # opcjonalnie, ale zalecane; fallback: `gh auth token`
python3 scripts/build_catalog.py
python3 scripts/validate_catalog.py
```

[Workflow tygodniowy](.github/workflows/update-catalog.yml) robi to samo i commituje odświeżone dane. Chcesz dodać kolekcję? Edytuj [`data/sources.json`](data/sources.json) — zobacz [`CONTRIBUTING.md`](CONTRIBUTING.md).

Strona jest statyczna: działa na GitHub Pages, Vercel, Netlify, Cloudflare Pages i zwykłym `python3 -m http.server`. Bez sekretów, bez bazy, bez telemetrii. Zobacz [`docs/DEPLOY.md`](docs/DEPLOY.md).

---

## Podziękowania

Dziękujemy autorom i organizacjom, których otwarta praca tworzy ten indeks: Anthropic, OpenAI, Google, GitHub, Vercel Labs, Cloudflare, DuckDB, Obsidian, Hugging Face, Android, Trail of Bits, OpenZeppelin, Matt Pocock, Jesse Vincent (obra), Addy Osmani, Emil Kowalski i setkom osób z community. Każdy wpis linkuje do źródła i pokazuje status licencji.

## Licencja

Kod katalogu, strona i dokumentacja są na **MIT** — [`LICENSE`](LICENSE). Skille upstream pozostają na swoich licencjach; rozpowszechniamy tylko metadane i linki.

<p align="center"><sub>Zrobione z GitHub API, standardowej biblioteki Pythona i dużą dawką ciekawości. ⭐ Zostaw gwiazdkę, jeśli oszczędziło Ci to popołudnia.</sub></p>
