# Goal & Task Tracker

Aplikacja desktopowa służąca do zarządzania celami życiowymi i śledzenia postępów w realizacji zadań. Projekt został zrealizowany w języku Python przy użyciu frameworka Flet (interfejs graficzny) oraz bazy danych SQLite (przechowywanie danych).

Aplikacja łączy w sobie funkcjonalności listy zadań (To-Do List) z trackerem nawyków, oferując dodatkowo moduł analityczny do wizualizacji postępów.

## 🚀 Główne funkcjonalności

- **Zarządzanie Celami**: Tworzenie celów głównych z definicją nazwy, opisu, kategorii oraz terminu wykonania (Deadline).
- **System Zadań**: Przypisywanie mniejszych zadań do konkretnych celów (relacja 1:N).
- **Kategorie**: Wizualne rozróżnienie celów za pomocą ikon (Zdrowie, Praca, Nauka, Finanse, Inne).
- **Kalendarz**: Wbudowany wybór daty dla terminów realizacji.
- **Moduł Analizy**: Interaktywne wykresy słupkowe pokazujące liczbę wykonanych zadań w ciągu ostatnich 7 dni.
- **Filtrowanie Danych**: Możliwość filtrowania wykresów dla wszystkich celów łącznie lub dla konkretnego wybranego celu.
- **Trwałość Danych**: Wszystkie informacje są zapisywane w lokalnym pliku bazy danych (`goals.db`).

## 🛠️ Wymagania i Instalacja

Aby uruchomić projekt lokalnie, wymagany jest zainstalowany interpreter Python (wersja 3.8 lub nowsza).

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
- **`database.py`**: Plik odpowiedzialny za warstwę dostępu do danych (Backend/Database Layer). Zawiera definicje funkcji SQL, które tworzą tabele, dodają nowe rekordy oraz pobierają dane potrzebne do wyświetlenia listy i wykresów. Oddziela logikę biznesową od interfejsu graficznego.
- **`requirements.txt`**: Lista zewnętrznych bibliotek Pythona wymaganych do działania projektu (m.in. flet, flet-charts).
- **`.gitignore`**: Plik konfiguracyjny Gita. Informuje system kontroli wersji, które pliki mają być ignorowane (np. pliki tymczasowe, lokalna baza danych `goals.db` czy foldery środowiska wirtualnego), aby zachować czystość w repozytorium.

## 🗄️ plik database.py

Ten plik pełni rolę warstwy dostępu do danych (Backend). Nie zawiera żadnego kodu odpowiedzialnego za wygląd aplikacji. Jego zadaniem jest komunikacja z bazą danych SQLite za pomocą języka zapytań SQL.

Poniżej znajduje się opis kluczowych funkcji zaimplementowanych w tym module:

### `init_db()`

Funkcja uruchamiana przy starcie aplikacji. Sprawdza, czy plik bazy danych istnieje. Jeśli nie, tworzy go oraz definiuje strukturę trzech powiązanych tabel (Relacyjna Baza Danych):

- **goals**: Przechowuje cele główne.
- **tasks**: Przechowuje zadania, które są przypisane do celów za pomocą klucza obcego (FOREIGN KEY). Tworzy to relację Jeden-do-Wielu (Jeden cel może mieć wiele zadań).
- **tracker**: Tabela historii. Przechowuje informacje o tym, kiedy konkretne zadanie zostało wykonane.

### `add_goal(...)` oraz `add_task(...)`

Funkcje odpowiedzialne za wprowadzanie nowych danych (INSERT). Przyjmują dane wpisane przez użytkownika w formularzach (np. nazwę, opis, datę), dodają do nich automatycznie dzisiejszą datę utworzenia i zapisują w odpowiednich tabelach.

### `get_goals_with_tasks()`

Kluczowa funkcja dla głównego widoku aplikacji. Wykonuje złożoną operację pobierania danych:

1. Najpierw pobiera listę wszystkich celów.
2. Następnie dla każdego celu wykonuje dodatkowe zapytanie, aby pobrać przypisane do niego zadania.
3. Zwraca złożoną strukturę danych (lista w liście), którą łatwo wyświetlić w interfejsie graficznym.

### `toggle_task(task_id, date_str)`

Obsługuje logikę "odznaczania" zadań (checkbox). Działa na zasadzie przełącznika:

- Sprawdza, czy dany nawyk jest już zapisany jako wykonany w bazie.
- **Jeśli TAK** → usuwa wpis z bazy (użytkownik odznaczył checkbox).
- **Jeśli NIE** → dodaje wpis do bazy (użytkownik zaznaczył checkbox).

### `get_stats(goal_id=None)`

Funkcja analityczna zasilająca wykresy. Wykorzystuje zaawansowane zapytania SQL z łączeniem tabel (JOIN) oraz grupowaniem (GROUP BY).

- Zlicza (COUNT), ile zadań zostało wykonanych w poszczególnych dniach.
- Obsługuje filtrowanie: jeśli podamy `goal_id`, statystyki zostaną ograniczone tylko do wybranego celu. W przeciwnym razie pokaże sumę dla wszystkich celów.
- Ogranicza wyniki do ostatnich 7 dni (LIMIT 7), aby wykres był czytelny.

## 🖥️ Plik main.py

Ten plik odpowiada za warstwę prezentacji (Frontend). Został napisany przy użyciu frameworka Flet, który pozwala tworzyć interfejsy graficzne w Pythonie. Kod w tym pliku nie łączy się bezpośrednio z SQL – wykorzystuje do tego funkcje zaimportowane z `database.py`.

Poniżej znajduje się opis kluczowych elementów i funkcji:

### `Konfiguracja i main(page)`

Jest to punkt wejścia do aplikacji.

- **Lokalizacja**: Ustawiamy język polski (pl-PL), aby kalendarz wyświetlał polskie nazwy miesięcy i dni.
- **Symulacja Mobile**: Ustawiamy sztywną szerokość i wysokość okna (400x800), aby na ekranie komputera aplikacja wyglądała jak uruchomiona na smartfonie.

### `CATEGORY_ICONS`

Słownik (mapa), który przypisuje konkretną ikonkę (np. serce, praca) do nazwy kategorii. Dzięki temu łatwo zarządzać wyglądem w jednym miejscu.

### `render_dashboard()`

Najważniejsza funkcja widoku. Odpowiada za rysowanie głównego ekranu. Działa w pętli:

1. Czyści ekran.
2. Pobiera listę celów i zadań z bazy danych.
3. Dla każdego celu tworzy "Kartę" (Container), a w niej generuje listę "Wierszy" z zadaniami.
4. Jeśli zadanie jest wykonane, zmienia jego kolor na jasny turkus i przekreśla tekst.

### `render_stats_view(target_goal_id)`

Moduł analityczny wykorzystujący bibliotekę `flet_charts`.

- **Skalowanie**: Funkcja dynamicznie oblicza wysokość słupków, znajdując najwyższą wartość w danych (`max_val`), aby wykres zawsze mieścił się na ekranie.
- **Oś X i Y**: Generuje etykiety z datami na dole i liczbami po lewej stronie.
- **Filtr**: Obsługuje listę rozwijaną (Dropdown). Po zmianie wyboru, funkcja uruchamia się ponownie z nowym parametrem `target_goal_id`, filtrując dane.

### System Modalny (AlertDialog)

Aplikacja wykorzystuje wyskakujące okienka do wprowadzania danych, aby nie zaśmiecać głównego ekranu.

- **`add_goal_dialog`**: Formularz dodawania celu. Zawiera pola tekstowe, listę rozwijaną kategorii oraz przycisk otwierający kalendarz (DatePicker).
- **`add_task_dialog`**: Formularz dodawania zadania.
- **`current_goal_id_for_task`**: Specjalna zmienna pomocnicza. Zapamiętuje, w "plusa" którego celu kliknął użytkownik, aby wiedzieć, do którego celu przypisać nowe zadanie.

### `save_goal()` oraz `save_task()`

Funkcje zwrotne (Callbacki) przypisane do przycisków "Zapisz".

1. Pobierają wartości wpisane przez użytkownika.
2. Przekazują je do pliku `database.py`.
3. Czyszczą formularze.
4. Zamykają okno dialogowe.
5. Wywołują `render_dashboard()`, aby natychmiast pokazać nowe dane na ekranie.

### Nawigacja (NavigationBar)

Dolny pasek menu, który pozwala przełączać się między widokiem listy zadań a widokiem analizy danych. Zmiana zakładki wywołuje funkcję `on_nav_change`, która podmienia zawartość głównego kontenera.
