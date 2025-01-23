import webbrowser
from threading import Timer
from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'secret_key'  # necesar pentru mesaje flash

USER_CREDENTIALS = {'username': 'admin', 'password': 'parola123'}

# Detalii conexiune la baza de date
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,       # Portul MySQL
    'database': 'TEMA_BD',  # Numele bazei tale de date
    'user': 'root',     # Utilizatorul bazei de date
    'password': ''      # Parola utilizatorului bazei de date (dacă există)     # Parola utilizatorului bazei de date (dacă există)
}

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username == USER_CREDENTIALS['username'] and password == USER_CREDENTIALS['password']:
            return redirect(url_for('tables'))
        else:
            flash("Username sau parolă incorectă. Încearcă din nou.")
            return redirect(url_for('login'))
    
    return render_template('login.html')

@app.route('/tables')
def tables():
    try:
        # Conectare la baza de date
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Obține denumirea tabelelor
        cursor.execute(
            "SHOW TABLES;"
        )
        tables = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        # Transformăm rezultatele într-o listă de string-uri
        table_names = [table[0] for table in tables]
        return render_template('tables.html', table_names=table_names)
    
    except Exception as e:
        return f"Eroare la conectarea la baza de date: {e}"

@app.route('/table/<table_name>')
def table_details(table_name):
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # Interogări pentru fiecare tabel cu chei externe
        if table_name == 'books':
            cursor.execute("""
                SELECT b.ID_carte, b.Titlu, b.Gen, b.Data_publicare, p.Nume AS Editura
                FROM Books b
                JOIN PublishingHouses p ON b.ID_editura = p.ID_editura;
            """)
        elif table_name == 'author_book':
            cursor.execute("""
                SELECT ab.ID_autor, a.Nume AS Autor_Nume, a.Prenume AS Autor_Prenume, ab.ID_carte, b.Titlu AS Cartea
                FROM Author_Book ab
                JOIN Authors a ON ab.ID_autor = a.ID_autor
                JOIN Books b ON ab.ID_carte = b.ID_carte;
            """)
        elif table_name == 'contracts':
            cursor.execute("""
                SELECT c.ID_contract, p.Nume AS Editura, a.Nume AS Autor_Nume, a.Prenume AS Autor_Prenume, c.Data_inceperi, c.Data_sfarsitului, c.Tip_contract
                FROM Contracts c
                JOIN PublishingHouses p ON c.ID_editura = p.ID_editura
                JOIN Authors a ON c.ID_autor = a.ID_autor;
            """)
        elif table_name == 'orders':
            cursor.execute("""
                SELECT o.ID_comanda, c.Nume AS Client, o.Data_emiterii, o.Total, o.Stare_comanda
                FROM Orders o
                JOIN Customers c ON o.ID_client = c.ID_client;
            """)
        elif table_name == 'order_details':
            cursor.execute("""
                SELECT od.ID_item, o.ID_comanda, b.Titlu AS Cartea, od.Cantitate, od.Pret_unitar
                FROM Order_Details od
                JOIN Orders o ON od.ID_comanda = o.ID_comanda
                JOIN Books b ON od.ID_carte = b.ID_carte;
            """)
        else:
            # Dacă tabelul nu conține chei externe
            cursor.execute(f"SELECT * FROM {table_name};")

        rows = cursor.fetchall()
        col_names = [desc[0] for desc in cursor.description]
        cursor.close()
        conn.close()

        return render_template('tables_details.html', table_name=table_name, col_names=col_names, rows=rows)

    except Exception as e:
        return f"Eroare la afișarea detaliilor tabelului: {e}"

@app.route('/interogari', methods=['GET', 'POST'])
def interogari():
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    data = {}  # Dicționar pentru stocarea tabelelor și a datelor lor
    interogare_rezultat = None
    interogare_erori = None

    if request.method == 'POST':
        action = request.form.get('action')
        table = request.form.get('table')
        
        try:
            if action == 'insert':
                # Gestionăm INSERT
                columns = request.form.get('columns').split(',')
                values = request.form.get('values').split(',')
                placeholders = ', '.join(['%s'] * len(values))
                query = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({placeholders})"
                cursor.execute(query, values)
                conn.commit()
                flash("Inserarea a fost realizată cu succes.")
            elif action == 'update':
                # Gestionăm UPDATE
                set_clause = request.form.get('set')
                where_clause = request.form.get('where')
                query = f"UPDATE {table} SET {set_clause} WHERE {where_clause}"
                cursor.execute(query)
                conn.commit()
                flash("Actualizarea a fost realizată cu succes.")
            elif action == 'delete':
                # Gestionăm DELETE
                where_clause = request.form.get('where')
                query = f"DELETE FROM {table} WHERE {where_clause}"
                cursor.execute(query)
                conn.commit()
                flash("Ștergerea a fost realizată cu succes.")
            elif action == 'query':
                # Executăm interogări SQL personalizate
                sql_query = request.form.get('sql_query')
                cursor.execute(sql_query)
                interogare_rezultat = cursor.fetchall()
                col_names = [desc[0] for desc in cursor.description]
                interogare_rezultat = {'columns': col_names, 'rows': interogare_rezultat}
        except Exception as e:
            interogare_erori = str(e)
            flash(f"A apărut o eroare: {e}")
    
    # Obține tabelele și primele 5 rânduri din fiecare
    try:
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        table_names = [table[0] for table in tables]
        
        for table_name in table_names:
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()
            col_names = [desc[0] for desc in cursor.description]
            data[table_name] = {'columns': col_names, 'rows': rows}
    except Exception as e:
        flash(f"A apărut o eroare la încărcarea tabelelor: {e}")

    cursor.close()
    conn.close()

    return render_template(
        'interogari.html',
        tables=data,
        interogare_rezultat=interogare_rezultat,
        interogare_erori=interogare_erori
    )

@app.route('/interogari_conditii', methods=['GET', 'POST'])
def interogari_conditii():
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor(dictionary=True)
    
    interogari = {
        # 5 interogări folosind JOIN
        "carti_si_edituri": {
            "titlu": "Cărți și editurile asociate",
            "sql": """
                SELECT b.Titlu, p.Nume AS Editura
                FROM Books b
                JOIN PublishingHouses p ON b.ID_editura = p.ID_editura
            """,
            "label": None,
            "placeholder": None,
        },
        "comenzi_si_clienti": {
            "titlu": "Comenzi și clienții aferenți",
            "sql": """
                SELECT o.ID_comanda, c.Nume AS Client
                FROM Orders o
                JOIN Customers c ON o.ID_client = c.ID_client
            """,
            "label": None,
            "placeholder": None,
        },
        "autori_si_carti": {
            "titlu": "Autori și cărți scrise de aceștia",
            "sql": """
                SELECT a.Nume AS Autor, b.Titlu AS Carte
                FROM Authors a
                JOIN Author_Book ab ON a.ID_autor = ab.ID_autor
                JOIN Books b ON ab.ID_carte = b.ID_carte
            """,
            "label": None,
            "placeholder": None,
        },
        "clienti_si_comenzi": {
            "titlu": "Clienți și comenzile lor",
            "sql": """
                SELECT c.Nume AS Client, o.ID_comanda
                FROM Customers c
                JOIN Orders o ON c.ID_client = o.ID_client
            """,
            "label": None,
            "placeholder": None,
        },
        "carti_si_comenzi": {
            "titlu": "Cărți și comenzile în care apar",
            "sql": """
                SELECT b.Titlu AS Carte, o.ID_comanda
                FROM Books b
                JOIN Order_Details od ON b.ID_carte = od.ID_carte
                JOIN Orders o ON od.ID_comanda = o.ID_comanda
            """,
            "label": None,
            "placeholder": None,
        },
        # 3 interogări folosind WHERE
        "carti_gen_specific": {
            "titlu": "Cărți dintr-un anumit gen",
            "sql": """
                SELECT Titlu, Gen
                FROM Books
                WHERE Gen LIKE %s
            """,
            "label": "Gen Carte:",
            "placeholder": "Ex: Ficțiune",
        },
        "comenzi_dupa_data": {
            "titlu": "Comenzi emise după o anumită dată",
            "sql": """
                SELECT ID_comanda, Data_emiterii
                FROM Orders
                WHERE Data_emiterii > %s
            """,
            "label": "Data minimă:",
            "placeholder": "Ex: 2023-01-01",
        },
        "clienti_cu_email": {
            "titlu": "Clienți cu un anumit domeniu de email",
            "sql": """
                SELECT Nume, Email
                FROM Customers
                WHERE Email LIKE %s
            """,
            "label": "Domeniu Email:",
            "placeholder": "Ex: %gmail.com",
        },
        # 2 interogări folosind HAVING
        "comenzi_valoare_medie": {
            "titlu": "Comenzi cu valoare peste media totală",
            "sql": """
                SELECT ID_comanda, Total
                FROM Orders
                GROUP BY ID_comanda, Total
                HAVING Total > (SELECT AVG(Total) FROM Orders)
            """,
            "label": None,
            "placeholder": None,
        },
        "clienți_minim_2_comenzi": {
            "titlu": "Clienți cu minim 2 comenzi",
            "sql": """
                SELECT c.Nume, COUNT(o.ID_comanda) AS Numar_Comenzi
                FROM Customers c
                JOIN Orders o ON c.ID_client = o.ID_client
                GROUP BY c.ID_client, c.Nume
                HAVING COUNT(o.ID_comanda) >= 2
            """,
            "label": None,
            "placeholder": None,
        },
    }

    rezultate = {}
    erori = []

    if request.method == 'POST':
        interogare_selectata = request.form.get('interogare')
        if interogare_selectata in interogari:
            query_info = interogari[interogare_selectata]
            param_value = request.form.get(interogare_selectata) or "%"
            try:
                if "HAVING" in query_info["sql"]:
                    cursor.execute(query_info["sql"], (int(param_value),))
                elif "WHERE" in query_info["sql"]:
                    cursor.execute(query_info["sql"], (param_value,))
                else:
                    cursor.execute(query_info["sql"])
                rezultate[interogare_selectata] = cursor.fetchall()
            except Exception as e:
                erori.append(f"Eroare la interogarea {interogare_selectata}: {e}")

    cursor.close()
    conn.close()

    return render_template('interogari_conditii.html', interogari=interogari, rezultate=rezultate, erori=erori)


# Funcție pentru a deschide browserul
def open_browser():
    webbrowser.open("http://127.0.0.1:5000/")

if __name__ == '__main__':
    Timer(1, open_browser).start()
    app.run(debug=True)
