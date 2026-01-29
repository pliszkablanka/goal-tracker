# Goal & Task Tracker – System zarządzania celami osobistymi

## 1. Charakterystyka oprogramowania

### a. Nazwa skrócona
**GoalTracker**

### b. Nazwa pełna
**Goal & Task Tracker – System zarządzania celami osobistymi**

### c. Sumaryczny opis ze wskazaniem celów

Aplikacja służąca do zarządzania celami życiowymi i śledzenia postępów w realizacji zadań przy pomocy wykresów. Projekt łączy w sobie funkcjonalności listy zadań (To-Do-List) w postaci zarządzania celami i mniejszymi zadaniami niezbędnymi do ich osiągnięcia oraz moduł analityczny do wizualizacji postępów.

Głównym celem oprogramowania jest umożliwienie użytkownikowi:
- Łatwego planowania długoterminowych celów
- Dzielenia ich na mniejsze etapy
- Monitorowania systematyczności za pomocą interaktywnych wykresów słupkowych

---

## 2. Prawa autorskie

### a. Autorzy
- **Blanka Pliszka**
- **Radosław Kozłowski**

### b. Warunki licencyjne
Oprogramowanie udostępniane na licencji **MIT**. Pozwala ona na swobodne używanie, kopiowanie, modyfikowanie i rozpowszechnianie oprogramowania, pod warunkiem zachowania informacji o prawach autorskich.

Pod warunkiem zachowania informacji o prawach autorskich.

---

## 3. Specyfikacja wymagań

### a. Lista wymagań funkcjonalnych i pozafunkcjonalnych

| ID | Nazwa | Opis | Priorytet | Kategoria |
|---|---|---|---|---|
| F-01 | Zarządzanie Celami | Tworzenie celów głównych z definicją nazwy, opisu oraz terminu wykonania | 1 | Funkcjonalne (Logika) |
| F-02 | Kategoryzacja | Wizualne rozróżnienie celów za pomocą ikon (Zdrowie, Praca, Nauka, Finanse, Inne) | 2 | Funkcjonalne (UI) |
| F-03 | System Zadań | Przypisywanie mniejszych zadań do konkretnych celów (relacja jeden do wielu) | 1 | Funkcjonalne (Logika) |
| F-04 | Kalendarz | Wbudowany wybór daty dla terminów realizacji (Date Picker) | 2 | Funkcjonalne (UI) |
| F-05 | Śledzenie postępów | Odznaczanie wykonanych zadań (checkbox) i zapisywanie daty wykonania | 1 | Funkcjonalne (Logika) |
| F-06 | Moduł Analizy | Interaktywne wykresy słupkowe pokazujące liczbę wykonanych zadań w ciągu ostatnich 7 dni | 2 | Funkcjonalne (Analityka) |
| F-07 | Filtrowanie Danych | Możliwość filtrowania wykresów dla wszystkich celów łącznie lub dla konkretnego celu | 2 | Funkcjonalne (Analityka) |
| PF-01 | Trwałość Danych | Wszystkie informacje są zapisywane w lokalnym pliku bazy danych SQLite (goals.db) | 1 | Pozafunkcjonalne |
| PF-02 | Responsywność | Interfejs graficzny skaluje się i automatycznie dostosowuje układ elementów do aktualnej rozdzielczości ekranu lub rozmiaru okna. | 2 | Pozafunkcjonalne |
| PF-03 | Wieloplatformowość | Możliwość uruchomienia aplikacji na systemach desktopowych (Windows, macOS, Linux) oraz mobilnych (Android, iOS) korzystając z tego samego kodu źródłowego. | 3 | Pozafunkcjonalne |

---

## 4. Architektura systemu/oprogramowania

### a. Architektura rozwoju (Środowisko deweloperskie)

Narzędzia wykorzystywane podczas tworzenia oprogramowania:

- **Język programowania:** Python (v3.12.7) – Główny język logiki aplikacji
- **Edytor kodu:** Visual Studio Code (v1.108) – Środowisko programistyczne (IDE)
- **System kontroli wersji:** Git (v2.47.1) – Zarządzanie historią zmian
- **Repozytorium:** GitHub – Zdalne przechowywanie kodu źródłowego
- **Generatywna Sztuczna Inteligencja:** Google Gemini Pro - Narzędzie wspomagające tworzenie kodu.
- **Baza wiedzy:** Oficjalna dokumentacja Flet (flet.dev) – Źródło informacji o komponentach i strukturze frameworka.

### b. Architektura uruchomieniowa (Środowisko docelowe)

Technologie wymagane do uruchomienia aplikacji przez użytkownika końcowego:

- **Interpreter:** Python (v3.8 lub nowszy)
- **Biblioteka GUI:** Flet (v0.80.4) – Framework do budowy interfejsu graficznego
- **Biblioteka Wykresów:** Flet-Charts (v0.80.2) – Rozszerzenie do wizualizacji danych
- **Baza Danych:** SQLite3 (v3.51.2) – Wbudowany w Python silnik bazy danych (bezserwerowy)

### c. Prezentacja omawiająca wykorzystywane technologie

Prezentacja zamieszczona w repozytorium projektu pod nazwą **prezentacja_flet**

## 5. Testy

### a. Scenariusze testów

Poniżej przedstawiono scenariusze weryfikujące poprawność działania kluczowych funkcjonalności.

| ID Scenariusza | Opis | Kroki testowe | Oczekiwany rezultat |
|---|---|---|---|
| TC-01 | Dodanie nowego celu | 1. Kliknij "+"<br>2. Wpisz nazwę "Test"<br>3. Wybierz kategorię<br>4. Wybierz datę<br>5. Wpisz opis<br>6. Zapisz | Cel pojawia się na liście głównej z odpowiednią ikoną i datą. |
| TC-02 | Dodanie zadania do celu | 1. Kliknij "Dodaj zadanie" pod celem "Test"<br>2. Wpisz nazwę zadania<br>3. Wpisz opis zadania<br>4. Zatwierdź | Zadanie pojawia się pod wybranym celem. |
| TC-03 | Wykonanie zadania | 1. Zaznacz checkbox przy zadaniu<br>2. Odznacz checkbox przy zadaniu | Checkbox pozostaje zaznaczony (stan zapisany w bazie, w interfejsie użytkownika zmienia się wygląd zadania). |
| TC-04 | Weryfikacja wykresu | 1. Przejdź do zakładki "Analiza"<br>2. Sprawdź słupek dla dzisiejszej daty | Słupek wzrósł o liczbę wykonanych zadań w TC-03. |
| TC-05 | Filtrowanie wykresu | 1. W zakładce "Analiza" wybierz z listy cel "Test" | Wykres pokazuje dane tylko dla celu "Test". |

### b. Sprawozdanie z wykonania scenariuszy testów

Wszystkie powyższe scenariusze **(TC-01 do TC-05)** zostały przeprowadzone w środowisku lokalnym **(Windows 11, Python 3.12.7)**.

**Rezultat:** ✅ **Wszystkie testy zakończone wynikiem POZYTYWNYM**

**Uwagi:**
- Baza danych poprawnie zachowuje stan aplikacji pomiędzy uruchomieniami
- Wykresy aktualizują się w czasie rzeczywistym

## 🛠️ Wymagania i Instalacja

Aby uruchomić projekt lokalnie, wymagany jest zainstalowany interpreter Python.

### 1. Pobranie projektu

Sklonuj repozytorium lub pobierz pliki projektu do folderu na dysku.

### 2. Instalacja bibliotek

Projekt posiada plik `requirements.txt`, który zawiera listę niezbędnych bibliotek. Otwórz terminal w folderze projektu i wpisz:

```bash
pip install -r requirements.txt
```

### 3. Tworzenie bazy danych

Aby stworzyć bazę danych, uruchom plik `database.py` komendą:

```bash
python database.py
```

### 4. Uruchomienie aplikacji

Aby włączyć program, wpisz w terminalu:

```bash
python main.py
```

## 📂 Struktura Projektu

Poniżej znajduje się opis poszczególnych plików wchodzących w skład projektu:

- **`main.py`**: Główny plik uruchomieniowy aplikacji. Odpowiada za warstwę prezentacji (Frontend). Zawiera kod budujący interfejs użytkownika w bibliotece Flet, obsługę zdarzeń (kliknięcia, nawigacja) oraz logikę wyświetlania okien dialogowych (modali).
- **`database.py`**: Plik odpowiedzialny za warstwę dostępu do danych (Backend/Warstwa danych). Zawiera definicje funkcji SQL, które tworzą tabele, dodają nowe rekordy oraz pobierają dane potrzebne do wyświetlenia listy i wykresów. Oddziela logikę biznesową od interfejsu graficznego.
- **`requirements.txt`**: Lista zewnętrznych bibliotek Pythona wymaganych do działania projektu (flet, flet-charts).
- **`.gitignore`**: Plik konfiguracyjny Gita. Informuje system kontroli wersji, które pliki mają być ignorowane (np. pliki tymczasowe, lokalna baza danych `goals.db`), aby zachować czystość w repozytorium.

#### Warstwa Danych (database.py - Backend)

Odpowiada za komunikację z bazą danych SQLite. Nie zawiera kodu interfejsu.

- **init_db():** Tworzy strukturę relacyjną trzech tabel:
  - `goals` – Cele główne
  - `tasks` – Zadania (relacja Jeden-do-Wielu z celami)
  - `tracker` – Historia wykonania zadań

- **Funkcje CRUD:**
  - `add_goal` – Dodawanie celów
  - `add_task` – Dodawanie zadań
  - `toggle_task` – Zmiana statusu zadania

- **Analityka (get_stats):** Wykorzystuje zapytania SQL z GROUP BY i JOIN do agregacji danych dla wykresów (ostatnie 7 dni)

## Warstwa Prezentacji (main.py - Frontend)

Odpowiada za interfejs użytkownika (UI) zbudowany we frameworku Flet. Komunikuje się z warstwą danych.

### Konfiguracja
- Ustawia polską lokalizację
- Ustawia parametry ekranu
- Mapuje ikony kategorii

### Renderowanie widoków

- **`render_dashboard`** – Dynamiczne tworzenie kart celów i list zadań
- **`render_stats_view`** – Generowanie skalowalnych wykresów słupkowych z filtrowaniem

### Interakcja
- Obsługa formularzy w oknach modalnych (AlertDialog) i wypełnianie danych (TextField)
- Nawigacja dolna (NavigationBar) do przełączania ekranów