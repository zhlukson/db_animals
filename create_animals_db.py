import sqlite3

conection = sqlite3.Connection('animal_1.db')
cur = conection.cursor()

conection_1 = sqlite3.Connection('animal.db')
cur_1 = conection_1.cursor()

cur.execute('''
    CREATE TABLE colors (
    color_id INTEGER PRIMARY KEY AUTOINCREMENT,
    color_name VARCHAR(100) NOT NULL
    )
''')

cur.execute('''
    CREATE TABLE age_upon_outcome (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    age INTEGER NOT NULL,
    name VARCHAR(50) NOT NULL
    )
''')

cur.execute('''
    CREATE TABLE outcome_type (
    type_id INTEGER PRIMARY KEY AUTOINCREMENT,
    type VARCHAR(50)
    )
''')

cur.execute('''
    CREATE TABLE outcome_subtype (
    subtype_id INTEGER PRIMARY KEY AUTOINCREMENT,
    subtype VARCHAR(50)
    )
''')

cur.execute('''
    CREATE TABLE animal_type (
    type_id INTEGER PRIMARY KEY AUTOINCREMENT,
    type VARCHAR(50)
    )
''')

cur.execute('''
    CREATE TABLE animals (
    animal_id VARCHAR(10) PRIMARY KEY,
    animal_type INTEGER NOT NULL,
    name VARCHAR(100) NOT NULL,
    breed VARCHAR(100) NOT NULL,
    color_1 INTEGER NOT NULL,
    color_2 INTEGER,
    date_of_birth DATETIME NOT NULL,
    FOREIGN KEY (animal_type) REFERENCES animal_type (type_id) ON DELETE RESTRICT,
    FOREIGN KEY (color_1) REFERENCES colors (color_id) ON DELETE RESTRICT,
    FOREIGN KEY (color_2) REFERENCES colors (color_id) ON DELETE RESTRICT
    )
''')

cur.execute('''
    CREATE TABLE outcome (
    outcome_id INTEGER PRIMARY KEY AUTOINCREMENT,
    animal_id VARCHAR(10) NOT NULL,
    age_upon_outcome INTEGER NOT NULL,
    outcome_subtype INTEGER,
    outcome_type INTEGER,
    outcome_mounth INTEGER,
    outcome_year INTEGER,
    FOREIGN KEY (animal_id) REFERENCES animals (animal_id) ON DELETE RESTRICT,
    FOREIGN KEY (age_upon_outcome) REFERENCES age_upon_outcome (id) ON DELETE RESTRICT,
    FOREIGN KEY (outcome_subtype) REFERENCES outcome_subtype (subtype_id) ON DELETE RESTRICT,
    FOREIGN KEY (outcome_type) REFERENCES outcome_type (type_id) ON DELETE RESTRICT
    )
''')


cur.execute('''
    INSERT INTO animal_type (type) VALUES ("Cat")
''')

colors = {i[0] for i in cur_1.execute('''
    SELECT DISTINCT color1
    FROM animals
    WHERE color1 IS NOT NULL;
''').fetchall() + cur_1.execute('''
    SELECT DISTINCT color2
    FROM animals
    WHERE color2 IS NOT NULL;
''').fetchall()}

for i in colors:
    cur.execute(f'''
        INSERT INTO colors (color_name) VALUES ("{i}")
    ''')

outcome_type = [i[0] for i in cur_1.execute('''
    SELECT DISTINCT outcome_type
    FROM animals
    WHERE outcome_type IS NOT NULL;
''').fetchall()]

for i in outcome_type:
    cur.execute(f'''
        INSERT INTO outcome_type (type) VALUES ("{i}")
    ''')

outcome_subtype = [i[0] for i in cur_1.execute('''
    SELECT DISTINCT outcome_subtype
    FROM animals
    WHERE outcome_subtype IS NOT NULL;
''').fetchall()]

for i in outcome_subtype:
    cur.execute(f'''
        INSERT INTO outcome_subtype (subtype) VALUES ("{i}")
    ''')

anumals_id = {j: i for i, j in dict(cur.execute('''
    SELECT *
    FROM animal_type
''').fetchall()).items()}

colors_id = {j: i for i, j in dict(cur.execute('''
    SELECT *
    FROM colors
''').fetchall()).items()}

colors_id[None] = 'NULL'

animals = cur_1.execute('''
    SELECT DISTINCT animal_id, animal_type, name, breed, color1, color2, date_of_birth
    FROM animals;
''').fetchall()

for i in animals:
    if i[5] != 'NULL':
        cur.execute(f'''
            INSERT INTO animals VALUES
            ("{i[0]}", {anumals_id[i[1]]}, "{i[2]}", "{i[3]}", {colors_id[i[4]]}, {colors_id[i[5]]}, "{i[6]}")
        ''')
    else:
        cur.execute(f'''
                    INSERT INTO animals VALUES (animal_id, animal_type, name, breed, color_1, date_of_birth)
                    ("{i[0]}", {anumals_id[i[1]]}, "{i[2]}", "{i[3]}", {colors_id[i[4]]}, "{i[6]}")
                ''')

age_upon_outcome = [i[0].split() for i in cur_1.execute('''
    SELECT DISTINCT age_upon_outcome
    FROM animals;
''').fetchall()]

for i in age_upon_outcome:
    cur.execute(f'''
        INSERT INTO age_upon_outcome (age, name)
        VALUES ({i[0]}, "{i[1]}")
    ''')

age_upon_outcome_id = {f'{i[1]} {i[2]}': i[0] for i in cur.execute('''
    SELECT * 
    FROM age_upon_outcome;
''').fetchall()}

outcome_subtype_id = {i[1]: i[0] for i in cur.execute('''
    SELECT * 
    FROM outcome_subtype;
''').fetchall()}

outcome_type_id = {i[1]: i[0] for i in cur.execute('''
    SELECT * 
    FROM outcome_type;
''').fetchall()}

outcomes = cur_1.execute('''
    SELECT "index", animal_id, age_upon_outcome, outcome_subtype, outcome_type, outcome_month, outcome_year
    FROM animals
''').fetchall()

for i in outcomes:
    if i[4] is not None:
        if i[3] is not None:
            cur.execute(f'''
                INSERT INTO outcome 
                VALUES ({i[0]}, "{i[1]}", {age_upon_outcome_id[i[2]]}, {outcome_subtype_id[i[3]]}, {outcome_type_id[i[4]]}, {i[5]}, {i[6]})
                    ''')
        else:
            cur.execute(f'''
                        INSERT INTO outcome (outcome_id, animal_id, age_upon_outcome, outcome_type, outcome_mounth, outcome_year)
                        VALUES ({i[0]}, "{i[1]}", {age_upon_outcome_id[i[2]]}, {outcome_type_id[i[4]]}, {i[5]}, {i[6]})
                    ''')
    else:
        cur.execute(f'''
                            INSERT INTO outcome (outcome_id, animal_id, age_upon_outcome, outcome_mounth, outcome_year)
                            VALUES ({i[0]}, "{i[1]}", {age_upon_outcome_id[i[2]]}, {i[5]}, {i[6]})
                        ''')


conection.commit()

