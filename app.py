from flask import Flask, render_template, request
from flask_mysqldb import MySQL

# Activate virtualenv venv\Scripts\activate.bat

# To run app with new database-
# 1. /delete_tables
# 2. /create_tables
# 3. /alter_tables
# 4. /populate_tables

app = Flask(__name__)

app.config['MYSQL_USER'] = 'sql9376756'
app.config['MYSQL_PASSWORD'] = 'TVEnuAcM7v'
app.config['MYSQL_HOST'] = 'sql9.freemysqlhosting.net'
app.config['MYSQL_DB'] = 'sql9376756'

mysql = MySQL(app)


@app.route("/create_tables")
def create_tables():
    cur = mysql.connection.cursor()
    # Create Persons Table
    cur.execute('''CREATE TABLE Persons (personID INTEGER AUTO_INCREMENT NOT NULL, firstname VARCHAR(255),
                    lastname VARCHAR(255), house INTEGER, PRIMARY KEY (personID))''')
    # Create Houses Table
    cur.execute('''CREATE TABLE Houses (houseID INTEGER AUTO_INCREMENT, name VARCHAR(255),
                        sigil VARCHAR(255), PRIMARY KEY (houseID))''')
    # Create Battles Table
    cur.execute('''CREATE TABLE Battles (battleID INTEGER AUTO_INCREMENT NOT NULL, name VARCHAR(255),
                PRIMARY KEY (battleID))''')
    # Create Religions Table
    cur.execute('''CREATE TABLE Religions (religionID INTEGER AUTO_INCREMENT NOT NULL, name VARCHAR(255), 
                PRIMARY KEY (religionID))''')
    # Create Houses_Battles Table
    cur.execute('''CREATE TABLE Houses_Battles (hid INTEGER, bid INTEGER, PRIMARY KEY (hid, bid))''')
    # Create Houses_Religions Table
    cur.execute('''CREATE TABLE Houses_Religions (hid INTEGER, rid INTEGER, PRIMARY KEY (hid, rid))''')
    # Create constraints
    return "Tables created successfully!"


@app.route("/alter_tables")
def alter_tables():
    cur = mysql.connection.cursor()
    cur.execute("SET FOREIGN_KEY_CHECKS=0")
    cur.execute("ALTER TABLE Persons ADD FOREIGN KEY (house) REFERENCES Houses(houseID)")
    cur.execute("ALTER TABLE Houses_Battles ADD FOREIGN KEY (hid) REFERENCES Houses(houseID)")
    cur.execute("ALTER TABLE Houses_Battles ADD FOREIGN KEY (bid) REFERENCES Battles(battleID)")
    return "Tables altered successfully!"


@app.route("/populate_tables")
def populate_tables():
    cur = mysql.connection.cursor()
    # Houses
    cur.execute("INSERT INTO Houses(name, sigil) VALUES (%s,%s)", ("Stark", "Direwolf"))
    cur.execute("INSERT INTO Houses(name, sigil) VALUES (%s,%s)", ("Lannister", "Lion"))
    cur.execute("INSERT INTO Houses(name, sigil) VALUES (%s,%s)", ("Baratheon", "Stag"))
    cur.execute("INSERT INTO Houses(name, sigil) VALUES (%s,%s)", ("Targaryen", "Dragon"))

    # People
    cur.execute("INSERT INTO Persons(firstname, lastname, house) VALUES (%s,%s,%s)", ("Sansa", "Stark", 1))
    cur.execute("INSERT INTO Persons(firstname, lastname, house) VALUES (%s,%s,%s)", ("Theon", "Greyjoy", 1))
    cur.execute("INSERT INTO Persons(firstname, lastname, house) VALUES (%s,%s,%s)", ("Jaime", "Lannister", 2))
    cur.execute("INSERT INTO Persons(firstname, lastname, house) VALUES (%s,%s,%s)", ("Stannis", "Baratheon", 3))
    cur.execute("INSERT INTO Persons(firstname, lastname, house) VALUES (%s,%s,%s)", ("Daenarys", "Targaryen", 4))

    # Battles
    cur.execute("INSERT INTO Battles(name) VALUES (%s)", ["Blackwater Bay"])
    cur.execute("INSERT INTO Houses_Battles(hid, bid) VALUES (%s, %s)", (1, 1))
    cur.execute("INSERT INTO Houses_Battles(hid, bid) VALUES (%s, %s)", (2, 1))
    cur.execute("INSERT INTO Houses_Battles(hid, bid) VALUES (%s, %s)", (3, 1))

    cur.execute("INSERT INTO Battles(name) VALUES (%s)", ["Battle of the Bastards"])
    cur.execute("INSERT INTO Houses_Battles(hid, bid) VALUES (%s, %s)", (2, 2))
    cur.execute("INSERT INTO Houses_Battles(hid, bid) VALUES (%s, %s)", (3, 2))
    cur.execute("INSERT INTO Houses_Battles(hid, bid) VALUES (%s, %s)", (4, 2))

    mysql.connection.commit()
    cur.close()

    return "Populated Tables!"


@app.route("/delete_tables")
def delete_tables():
    cur = mysql.connection.cursor()
    cur.execute("SET FOREIGN_KEY_CHECKS=0")
    cur.execute("DROP TABLE Battles, Persons, Houses, Houses_Battles, Houses_Religions, Religions")
    return "Deleted database!"


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/people", methods=['GET', 'POST'])
def people():

    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        house = request.form['house']

        cur = mysql.connection.cursor()
        cur.execute("SET FOREIGN_KEY_CHECKS=0")
        cur.execute("INSERT INTO Persons(firstname, lastname, house) VALUES (%s,%s,%s)", (first_name, last_name, house))
        mysql.connection.commit()
        cur.close()
        return "successfully added person to database!"

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Persons")
    people_details = cur.fetchall()
    cur.execute("SELECT * FROM Houses")
    houses_details = cur.fetchall()
    return render_template('people.html', people_details=people_details, houses_details=houses_details)


@app.route('/update_person/<person_id>', methods=['POST', 'GET'])
def update_person(person_id):

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Houses")
    houses_details = cur.fetchall()

    cur.execute("""SELECT * FROM Persons WHERE personID=%s""", person_id)
    person_info = cur.fetchall()

    if request.method == 'POST':
        person_id = person_id
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        house = request.form['house']
        cur = mysql.connection.cursor()
        cur.execute("""
               UPDATE Persons
               SET firstname=%s, lastname=%s, house=%s
               WHERE personID=%s
            """, (first_name, last_name, house, person_id))
        mysql.connection.commit()
        return "Updated person successfully!"

    return render_template("update_person.html", houses_details=houses_details, person_info=person_info)


@app.route('/delete_person/<person_id>')
def delete_person(person_id):

    cur = mysql.connection.cursor()

    cur.execute("""DELETE FROM Persons WHERE personID=%s""", person_id)
    mysql.connection.commit()

    return "Person successfully deleted!"


@app.route("/search_results/<q>")
def search_results(q):

    if q:
        search_input = q

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Houses")
        houses_details = cur.fetchall()

        cur.execute("""SELECT * FROM Persons WHERE firstname LIKE %s OR lastname LIKE %s""",
                    ([search_input], [search_input]))
        people_details = cur.fetchall()
        print("details: ", people_details)

        return render_template("search_results.html", houses_details=houses_details, people_details=people_details)

    return render_template("search_results.html")


@app.route("/houses", methods=['GET', 'POST'])
def houses():
    if request.method == 'POST':
        name = request.form['name']
        sigil = request.form['sigil']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Houses(name, sigil) VALUES (%s,%s)", (name, sigil))
        mysql.connection.commit()
        cur.close()
        return "successfully added House to database!"

    cur = mysql.connection.cursor()
    houses_data = cur.execute("SELECT * FROM Houses")
    if houses_data > 0:
        houses_details = cur.fetchall()
        cur.execute("SELECT * FROM Persons")
        people_details = cur.fetchall()
        return render_template('houses.html', people_details=people_details, houses_details=houses_details)

    return render_template('houses.html')


@app.route("/battles", methods=['GET', 'POST'])
def battles():

    if request.method == 'POST':
        battle_name = request.form['battle_name']
        participant_1 = request.form['participant_1']
        participant_2 = request.form['participant_2']
        participant_3 = request.form['participant_3']
        participant_4 = request.form['participant_4']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Battles(name) VALUES (%s)", [battle_name])
        mysql.connection.commit()

        cur.execute("SELECT battleID from Battles WHERE name = %s", [battle_name])
        relevant_battle_id = cur.fetchall()

        cur.execute("INSERT INTO Houses_Battles(hid, bid) VALUES (%s, %s)", (participant_1, relevant_battle_id))
        cur.execute("INSERT INTO Houses_Battles(hid, bid) VALUES (%s, %s)", (participant_2, relevant_battle_id))
        cur.execute("INSERT INTO Houses_Battles(hid, bid) VALUES (%s, %s)", (participant_3, relevant_battle_id))
        cur.execute("INSERT INTO Houses_Battles(hid, bid) VALUES (%s, %s)", (participant_4, relevant_battle_id))
        mysql.connection.commit()

        return "successfully added battle to database!"

    cur = mysql.connection.cursor()
    cur.execute("""SELECT * FROM Battles""")
    battles_names = cur.fetchall()
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Houses")
    houses_details = cur.fetchall()

    return render_template('battles.html', houses_details=houses_details, battles_names=battles_names)


@app.route("/battles_info/<battle_id>")
def battle(battle_id):

    cur = mysql.connection.cursor()
    cur.execute("""SELECT battleID, name FROM Battles WHERE battleID = %s""", [battle_id])
    battle_name = cur.fetchall()
    cur.execute("""SELECT * FROM Houses
                    JOIN Houses_Battles ON Houses.houseID = Houses_Battles.hid
                   WHERE Houses_Battles.bid = %s""", [battle_id])
    indiv_battle_info = cur.fetchall()
    return render_template("battle.html", battle_name=battle_name, indiv_battle_info=indiv_battle_info)


@app.route("/remove_participant/<battle_id>/<house_id>")
def remove_battle_participant(battle_id, house_id):
    cur = mysql.connection.cursor()
    cur.execute("""SELECT battleID FROM Battles WHERE name = %s""", [battle_id])
    battle_id = cur.fetchall()
    cur.execute("DELETE FROM Houses_Battles WHERE (hid, bid) = (%s, %s)", (house_id, battle_id))
    mysql.connection.commit()
    return "Removed participant from battle!"


@app.route("/delete_battle/<battle_id>")
def delete_battle(battle_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM Battles WHERE battleID = %s", [battle_id])
    mysql.connection.commit()
    return "Deleted battle!"


@app.route("/religions")
def religions():
    return render_template('religions.html')


if __name__ == "__main__":
    app.run(debug=True)
