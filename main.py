import flet as ft #Flet
import flet_charts as fch #Bibloteka do obsługi wykresów Flet
import database #Moduł obsługi bazy danych
import datetime #Biblioteka udostępniająca funkcje daty

# Mapowanie kategorii na ikony Flet (słownik klucz-wartość)
# Pozwala to łatwo zmieniać wygląd ikon w jednym miejscu
CATEGORY_ICONS = {
    "Zdrowie": ft.Icons.FAVORITE,
    "Nauka": ft.Icons.SCHOOL,
    "Praca": ft.Icons.WORK,
    "Finanse": ft.Icons.ATTACH_MONEY,
    "Inne": ft.Icons.STAR
}

def main(page: ft.Page):
    # --- KONFIGURACJA LOKALIZACJI ---
    # Robimy to, aby kalendarz miał tekst po polsku.
    page.locale_configuration = ft.LocaleConfiguration(
        supported_locales=[
            ft.Locale("pl", "PL"),  # Dodajemy polski
            ft.Locale("en", "US"),
        ],
        current_locale=ft.Locale("pl", "PL") # Ustawiamy polski jako aktywny
    )

    # --- KONFIGURACJA POCZĄTKOWA ---
    # Inicjalizacja bazy danych przy starcie aplikacji (tworzy tabele, jeśli nie istnieją)
    database.init_db()
    
    # Ustawienia wyglądu okna
    page.title = "Goal & Task Tracker"
    page.window_width = 400
    page.window_height = 800
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = ft.Colors.GREY_50
    page.padding = 40
    
    # Pobranie dzisiejszej daty do celów porównawczych
    today_str = datetime.date.today().isoformat()

    # Zmienna przechowująca ID celu, do którego aktualnie dodajemy zadanie
    current_goal_id_for_task = [None] 

    # --- ELEMENTY WSPÓŁDZIELONE ---
    # Główny kontener, który będzie przechowywał dynamiczną zawartość (Listę lub Wykres)
    body_container = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True, spacing=15)

    # --- DATE PICKER (Kalendarz) ---
    
    def change_date(e):
        """Obsługa wyboru daty z kalendarza."""
        if date_picker.value:
            # Formatujemy datę do stringa (RRRR-MM-DD) i wpisujemy w pole tekstowe formularza
            goal_deadline_display.value = date_picker.value.strftime("%Y-%m-%d")
            goal_deadline_display.update() # Odświeżenie tylko tego elementu

    # Komponent kalendarza
    date_picker = ft.DatePicker(
        on_change=change_date,
        confirm_text="Wybierz",
        cancel_text="Anuluj"
    )
    
    # Dodajemy kalendarz do nakładki strony (niewidoczny, dopóki nie wywołany)
    page.overlay.append(date_picker)
    
    # --- FORMULARZE MODALNE (WYSKAKUJĄCE OKNA) ---

    # 1. Dialog dodawania CELU
    # Definicja pól formularza
    goal_name_field = ft.TextField(label="Nazwa celu", hint_text="np. Schudnąć 5kg")
    goal_desc_field = ft.TextField(label="Opis", multiline=True, max_lines=3)
    goal_category_dd = ft.Dropdown(
        label="Kategoria",
        options=[ft.dropdown.Option(k) for k in CATEGORY_ICONS.keys()] # Generowanie opcji na podstawie słownika ikon
    )
    # Pole wyświetlające wybraną datę (read_only - użytkownik nie może wpisywać ręcznie)
    goal_deadline_display = ft.TextField(
        label="Deadline", 
        hint_text="Wybierz datę...", 
        read_only=True, 
        expand=True
    )
    # Przycisk otwierający kalendarz
    date_button = ft.IconButton(
    icon=ft.Icons.CALENDAR_MONTH, 
    icon_color=ft.Colors.TEAL_500,
    on_click=lambda _: (setattr(date_picker, "open", True), page.update())
    )

    def save_goal(e):
        """Logika zapisu nowego celu do bazy danych."""
        # Prosta walidacja - sprawdzamy czy nazwa została wpisana
        if goal_name_field.value:
            # Wywołanie funkcji dodania celu z modułu database.py
            database.add_goal(goal_name_field.value, goal_desc_field.value, goal_deadline_display.value, goal_category_dd.value)
            # Resetowanie pól formularza po zapisie
            goal_name_field.value = ""
            goal_desc_field.value = ""
            goal_deadline_display.value = ""
            goal_category_dd.value = None
            # Zamknięcie okna dialogowego i odświeżenie widoku
            add_goal_dialog.open = False
            page.update()
            render_dashboard()

    # Definicja okna dialogowego dla celu
    add_goal_dialog = ft.AlertDialog(
        modal=True, # Kliknięcie poza okno nie zamyka go
        title=ft.Text("Dodaj nowy Cel"),
        content=ft.Column([
            goal_name_field, 
            goal_category_dd,
            ft.Row([goal_deadline_display, date_button]), # Data i przycisk w jednym wierszu
            goal_desc_field
        ], height=300),
        actions=[
            ft.TextButton("Anuluj", on_click=lambda e: (setattr(add_goal_dialog, "open", False), page.update())),
            ft.Button("Zapisz", on_click=save_goal)
        ],
    )

    # 2. Dialog dodawania ZADANIA
    task_name_field = ft.TextField(label="Nazwa zadania", hint_text="np. Bieganie 5km")
    task_desc_field = ft.TextField(label="Opis zadania")

    def save_task(e):
        """Logika zapisu zadania przypisanego do konkretnego celu."""
        if task_name_field.value and current_goal_id_for_task[0]:
            database.add_task(
                current_goal_id_for_task[0], # ID celu pobrane przy kliknięciu
                task_name_field.value,
                task_desc_field.value,
            )
            # Reset pól
            task_name_field.value = ""
            task_desc_field.value = ""
            add_task_dialog.open = False
            # Odświeżenie
            page.update()
            render_dashboard()

    add_task_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Dodaj Zadanie do Celu"),
        content=ft.Column([task_name_field, task_desc_field], height=150),
        actions=[
            ft.TextButton("Anuluj", on_click=lambda e: (setattr(add_task_dialog, "open", False), page.update())), # Przycisk anulowania, który zamyka okno dialogowe poprzez zmianę jego stanu i odświeżenie strony
            ft.Button("Dodaj", on_click=save_task),
        ],
    )

    # Funkcje otwierające modale
    def open_add_goal_click(e):
        page.show_dialog(add_goal_dialog)


    def open_add_task_click(e):
        # e.control.data przechowuje ID celu, do którego kliknięto "Dodaj zadanie"
        #Zapisujemy to ID do zmiennej pomocniczej, aby wiedzieć gdzie dodać zadanie przy zapisie
        current_goal_id_for_task[0] = e.control.data 
        page.show_dialog(add_task_dialog)

    def toggle_task_change(e):
        """Obsługa kliknięcia checkboxa (zaznaczenie/odznaczenie zadania)."""
        task_id = e.control.data
        database.toggle_task(task_id, today_str) # Aktualizacja w bazie danych
        render_dashboard() # Przerysowanie widoku (aby zaktualizować kolory zadania)

    # --- WIDOKI ---

    def render_dashboard():
        """Widok główny: Lista Celów i ich Zadań."""
        # Czyszczenie kontenera przed narysowaniem nowych danych (odświeżanie)
        body_container.controls.clear()

        # Nagłówek z przyciskiem dodawania celu
        header = ft.Container(
            content=ft.Row([
                ft.Text("Twoje Cele", size=26, weight=ft.FontWeight.BOLD),
                ft.IconButton(ft.Icons.ADD_CIRCLE, icon_color=ft.Colors.TEAL_500, icon_size=40, on_click=open_add_goal_click) # Przycisk graficzny (ikona) wywołujący funkcję otwierającą formularz dodawania nowego celu
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            padding=20,
            bgcolor=ft.Colors.WHITE
        )
        body_container.controls.append(header)

        # Pobieranie danych: [(cel, [zadania]), (cel2, [zadania2])]
        data_structure = database.get_goals_with_tasks()
        completed_tasks = database.get_completed_tasks(today_str)

        # Obsługa przypadku, gdy baza jest pusta
        if not data_structure:
            body_container.controls.append(ft.Container(content=ft.Text("Brak celów. Dodaj pierwszy!", color=ft.Colors.GREY), padding=20))

        # Pętla główna: Tworzenie kart dla każdego celu
        for goal_data, tasks_list in data_structure:
            g_id, g_name, g_desc, g_deadline, g_category = goal_data
            
            # Dobieranie ikony na podstawie kategorii celu
            category_icon = CATEGORY_ICONS.get(g_category, ft.Icons.CIRCLE)
            
            # Lista kontrolek zadań dla tego konkretnego celu
            tasks_controls = []
            
            # Pętla wewnętrzna: Generowanie wierszy z zadaniami
            for task in tasks_list:
                t_id, t_name, t_desc = task
                is_done = t_id in completed_tasks
                
                # Wiersz pojedynczego zadania. Styl zależy od tego, czy zadanie jest wykonane (is_done)
                task_row = ft.Container(
                    content=ft.Row([
                       ft.Column([
                            ft.Text(t_name, size=15),
                            ft.Text(t_desc, size=10, color=ft.Colors.GREY_500) if t_desc else ft.Container()
                        ], spacing=0, expand=True),    
                        ft.Checkbox(value=is_done, data=t_id, on_change=toggle_task_change)
                    ]),
                    padding=8,
                    # Zmiana koloru tła jeśli zadanie jest zrobione
                    bgcolor=ft.Colors.TEAL_50 if is_done else ft.Colors.WHITE,
                    border_radius=8,
                    border=ft.Border.all(1, ft.Colors.GREY_100)
                )
                tasks_controls.append(task_row)

            # Przycisk "Dodaj zadanie" wewnątrz karty celu
            add_task_btn = ft.TextButton(
                "Dodaj zadanie", 
                icon=ft.Icons.ADD, 
                data=g_id, # Przekazujemy ID celu
                on_click=open_add_task_click
            )
            tasks_controls.append(add_task_btn)

            # Karta Celu (Grupa)
            goal_card = ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Row([
                            ft.Icon(category_icon, color=ft.Colors.TEAL_700), # Ikona kategorii przy nazwie celu
                            ft.Text(g_name, weight=ft.FontWeight.BOLD, size=18, color=ft.Colors.TEAL_900),
                        ]),
                        # Wyświetlanie terminu (jeśli istnieje)
                        ft.Container(
                            content=ft.Text(f"Do: {g_deadline}", size=11, color=ft.Colors.WHITE),
                            bgcolor=ft.Colors.RED_300 if g_deadline else ft.Colors.TRANSPARENT,
                            padding=5, border_radius=5
                        )
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ft.Text(g_desc, size=12, color=ft.Colors.GREY_600) if g_desc else ft.Container(),
                    ft.Divider(),
                    ft.Column(tasks_controls, spacing=5) # Wstawienie wygenerowanych wcześniej zadań
                ]),
                padding=15,
                margin=ft.Margin.symmetric(horizontal=15),
                bgcolor=ft.Colors.WHITE,
                border_radius=15,
                shadow=ft.BoxShadow(blur_radius=5, color=ft.Colors.GREY_300, offset=ft.Offset(0,2))
            )
            
            body_container.controls.append(goal_card)
        
        page.update()

    # --- ANALIZA (WYKRES) ---
    def render_stats_view(target_goal_id=None):
        """Widok Analizy: Generuje wykres słupkowy z możliwością filtrowania."""
        body_container.controls.clear()
        
        # Dropdown do wyboru celu
        all_goals = database.get_all_goals_simple()
        dropdown_options = [ft.dropdown.Option(key=None, text="Wszystkie cele")]
        for g_id, g_name in all_goals:
            dropdown_options.append(ft.dropdown.Option(key=str(g_id), text=g_name))

        def on_filter_change(e):
            """Obsługa zmiany wartości w filtrze."""
            val = e.control.value
            # Sprawdzamy, czy wartość istnieje i czy składa się tylko z cyfr
            # Zamiana stringa z dropdowna na int (ID celu) lub None
            if val and val.isdigit():
                new_id = int(val)
            else:
                new_id = None
            render_stats_view(new_id) # Przerysowanie wykresu z nowym filtrem

        filter_dropdown = ft.Dropdown(
            label="Filtruj wg celu",
            options=dropdown_options,
            value=str(target_goal_id) if target_goal_id else None,
            on_select=on_filter_change,
            bgcolor=ft.Colors.WHITE,
        )

        # Nagłówek sekcji analizy
        body_container.controls.append(
            ft.Container(
                content=ft.Column([
                    ft.Text("Analiza Postępów", size=24, weight=ft.FontWeight.BOLD),
                    filter_dropdown
                ]),
                padding=20,
                bgcolor=ft.Colors.WHITE
            )
        )

        # Pobranie danych do wykresu z bazy (z filtrem lub bez)
        stats = database.get_stats(target_goal_id)
        
        # Wyświetlenie tekstu jeśli nie ma statystyk
        if not stats:
            body_container.controls.append(ft.Container(content=ft.Text("Brak danych dla wybranego zakresu.", color=ft.Colors.GREY), padding=20))
            page.update()
            return

        # Budowanie wykresu
        chart_groups = []
        max_val = 0
        # Pętla iterująca po statystykach z bazy, służąca do wyznaczenia najwyższej wartości wykonanych zadań
        for i, (date_val, count) in enumerate(stats):
            # Porównanie aktualnej liczby z dotychczasowym maksimum w celu poprawnego skalowania wykresu
            if count > max_val: max_val = count
            # Tworzenie pojedynczego słupka
            chart_groups.append(
                fch.BarChartGroup(
                    x=i,
                    rods=[fch.BarChartRod(from_y=0, to_y=count, width=100, color=ft.Colors.TEAL_400, border_radius=4)]
                )
            )

        # Tworzenie etykiet osi X i Y
        labels_x = [fch.ChartAxisLabel(value=i, label=ft.Text(d[0][5:], size=10)) for i, d in enumerate(stats)]
        labels_y = []

        # Pętla generująca etykiety na osi pionowej wykresu od 0 do wartości maksymalnej (z marginesem +2)
        for value in range(int(max_val) + 2):
            labels_y.append(
                fch.ChartAxisLabel(
                    value=float(value), 
                    label=ft.Container(
                        ft.Text(str(value), size=12), 
                        padding=ft.padding.only(right=10, left=10)
                    )
                )
            )
        
        # Rysowanie wykresu
        chart = fch.BarChart(
            groups=chart_groups,
            left_axis=fch.ChartAxis(
                labels=labels_y,
                title=ft.Text("Zadania", size=14),
            ),
            bottom_axis=fch.ChartAxis(
                labels=labels_x,
                title=ft.Text("Data", size=14), 
            ),
            height=300,
            max_y=max_val + 2,
            interactive=True
        )

        body_container.controls.append(
            ft.Text(
                "Postęp wykonanych zadań z ostatnich 7 dni",
                size=16,
                weight=ft.FontWeight.BOLD,
                margin=ft.margin.only(left=15, top=20) # Dodaje margines, by wyrównać z kartą wykresu
            )
        )

        body_container.controls.append(
            ft.Container(content=chart, padding=20, bgcolor=ft.Colors.WHITE, border_radius=20, margin=15)
        )
        page.update()

    # --- NAWIGACJA (DOLNY PASEK) ---

    def on_nav_change(e):
        """Przełączanie widoków między Listą a Wykresem."""
        index = e.control.selected_index
        if index == 0:
            render_dashboard()
        elif index == 1:
            render_stats_view()

    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.CHECK_CIRCLE_OUTLINE, label="Cele i Zadania"),
            ft.NavigationBarDestination(icon=ft.Icons.BAR_CHART, label="Analiza"),
        ],
        on_change=on_nav_change,
        bgcolor=ft.Colors.WHITE
    )

    # Dodanie głównego kontenera do strony i pierwsze narysowanie widoku
    page.add(body_container)
    render_dashboard()

# Uruchomienie aplikacji
if __name__ == "__main__":
    ft.run(main)