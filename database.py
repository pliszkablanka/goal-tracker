import sqlite3  # Obsługa bazy danych SQL
import datetime # Obsługa dat (potrzebna do zapisywania terminów i historii)

# Nazwa pliku bazy danych, w którym przechowywane są wszystkie informacje
DB_NAME = "goals.db"

def get_connection():
    """Ustanawia połączenie z plikiem bazy danych."""
    return sqlite3.connect(DB_NAME)

def init_db():
    """Tworzy tabele w bazie danych przy pierwszym uruchomieniu aplikacji."""
    # Nawiązanie połączenia z bazą danych i utworzenie kursora do wydawania poleceń SQL
    conn = get_connection()
    cursor = conn.cursor()

    # Tabela 'goals' przechowuje główne cele (np. nazwa, kategoria, termin)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS goals (
            id INTEGER PRIMARY KEY AUTOINCREMENT, -- Unikalny numer porządkowy
            name TEXT NOT NULL,                   -- Nazwa celu
            description TEXT,                     -- Dodatkowy opis
            deadline TEXT,                        -- Przewidywana data zakończenia
            category TEXT,                        -- Przypisana kategoria (np. Praca, Nauka)
            created_at TEXT                       -- Data dodania celu do systemu
        )
    ''')

    # Tabela 'tasks' zawiera mniejsze zadania przypisane do konkretnych celów
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            goal_id INTEGER,                      -- Powiązanie zadania z konkretnym celem
            name TEXT NOT NULL,
            description TEXT,
            created_at TEXT,
            FOREIGN KEY(goal_id) REFERENCES goals(id) -- Klucz obcy łączący te dwie tabele
        )
    ''')

    # Tabela 'tracker' rejestruje daty wykonania poszczególnych zadań
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tracker (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_id INTEGER,                      -- Informacja, które zadanie zostało zrobione
            date_completed TEXT,                  -- Dokładna data oznaczenia jako zrobione
            FOREIGN KEY(task_id) REFERENCES tasks(id)
        )
    ''')

    conn.commit() # Zapisanie zmian w strukturze bazy
    conn.close()  # Zamknięcie połączenia

def add_goal(name, description, deadline, category):
    """Dodaje nowy cel główny do bazy danych."""
    conn = get_connection()
    cursor = conn.cursor()
    today = datetime.date.today().isoformat() # Pobranie aktualnej daty
    # Wstawianie danych przekazanych z formularza w aplikacji
    cursor.execute(
        "INSERT INTO goals (name, description, deadline, category, created_at) VALUES (?, ?, ?, ?, ?)",
        (name, description, deadline, category, today)
    )
    conn.commit()
    conn.close()

def add_task(goal_id, name, description):
    """Dodaje zadanie do bazy, przypisując je do wybranego celu (przez goal_id)."""
    conn = get_connection()
    cursor = conn.cursor()
    today = datetime.date.today().isoformat()
    cursor.execute(
        "INSERT INTO tasks (goal_id, name, description, created_at) VALUES (?, ?, ?, ?)",
        (goal_id, name, description, today)
    )
    conn.commit()
    conn.close()

def get_goals_with_tasks():
    """Pobiera wszystkie cele wraz z przypisanymi do nich zadaniami."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Pobieramy cele, sortując je od najnowszych (DESC)
    cursor.execute("SELECT id, name, description, deadline, category FROM goals ORDER BY id DESC")
    goals = cursor.fetchall()
    
    result = []
    for goal in goals:
        goal_id = goal[0] #ID to pierwszy element z tabeli goal
        # Dla każdego celu szukamy wszystkich jego zadań w tabeli tasks
        cursor.execute("SELECT id, name, description FROM tasks WHERE goal_id = ?", (goal_id,))
        tasks = cursor.fetchall()
        result.append((goal, tasks)) # Łączymy dane celu z listą zadań w jedną strukturę
        
    conn.close()
    return result # Zwrócenie celów

def get_all_goals_simple():
    """Pobiera listę samych nazw i ID celów (np. do rozwijanego menu)."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM goals")
    results = cursor.fetchall()
    conn.close()
    return results

def toggle_task(task_id, date_str):
    """Zmienia status zadania: dodaje wpis o wykonaniu lub go usuwa (jeśli już istniał)."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Sprawdzamy, czy zadanie o tym ID zostało już wykonane w danym dniu
    cursor.execute("SELECT id FROM tracker WHERE task_id = ? AND date_completed = ?", (task_id, date_str))
    existing = cursor.fetchone()

    if existing:
        # Jeśli zadanie było już zaznaczone, usuwamy wpis (odznaczamy)
        cursor.execute("DELETE FROM tracker WHERE id = ?", (existing[0],))
    else:
        # Jeśli zadanie nie było zaznaczone, dodajemy informację o wykonaniu
        cursor.execute("INSERT INTO tracker (task_id, date_completed) VALUES (?, ?)", (task_id, date_str))

    conn.commit()
    conn.close()

def get_completed_tasks(date_str):
    """Zwraca listę ID zadań, które zostały wykonane w wybranym dniu."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT task_id FROM tracker WHERE date_completed = ?", (date_str,))
    # Pobranie wszystkich pasujących wierszy i wyodrębnienie z nich tylko pierwszej kolumny (identyfikatorów) do prostej listy
    results = [row[0] for row in cursor.fetchall()]
    conn.close()
    return results

def get_stats(goal_id=None):
    """Zbiera dane o liczbie wykonanych zadań w czasie do wyświetlenia na wykresie."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Bazowe zapytanie łączące historię wykonania (tracker) z nazwami zadań (tasks)
    base_query = '''
        SELECT t.date_completed, COUNT(*) 
        FROM tracker t
        JOIN tasks tsk ON t.task_id = tsk.id
        WHERE 1=1
    '''
    params = []

    # Jeśli użytkownik chce statystyki tylko dla jednego celu, filtrujemy wyniki
    if goal_id:
        base_query += " AND tsk.goal_id = ?"
        params.append(goal_id)
        
    # Grupowanie wyników po datach i ograniczenie do ostatnich 7 dni z danymi
    base_query += " GROUP BY t.date_completed ORDER BY t.date_completed LIMIT 7"
    
    # Wykonanie komendy z parametrami
    cursor.execute(base_query, params)
    results = cursor.fetchall()
    conn.close()
    return results

# Sprawdzenie, czy plik został uruchomiony bezpośrednio (a nie zaimportowany jako moduł)
if __name__ == "__main__":
    init_db() # Uruchomienie tworzenia bazy danych
    print("Baza danych gotowa do pracy.")