import sqlite3, json

from flask import Flask

app = Flask("__name__")

@app.route('/<int:itemid>/')
def outcome(itemid):
    with sqlite3.Connection('animal_1.db') as conection:
        columns = ['animal_id', 'age_upon_outcome', 'outcome_type', 'outcome_subtype', 'outcome_month', 'outcome_year']

        cur = conection.cursor()
        query = f'''
            SELECT 
                outcome.animal_id,
                age_upon_outcome.age || ' ' || age_upon_outcome.name,
                outcome_type.type,
                outcome_subtype.subtype,
                outcome.outcome_mounth,
                outcome.outcome_year
            FROM outcome
            INNER JOIN outcome_type ON outcome.outcome_type = outcome_type.type_id
            INNER JOIN outcome_subtype ON outcome.outcome_subtype = outcome_subtype.subtype_id
            INNER JOIN age_upon_outcome ON outcome.age_upon_outcome = age_upon_outcome.id
            WHERE outcome_id = {itemid}
        '''
        if not cur.execute(query).fetchall():
            query = f'''
                        SELECT 
                            outcome.animal_id,
                            age_upon_outcome.age || ' ' || age_upon_outcome.name,
                            outcome_type.type,
                            outcome.outcome_mounth,
                            outcome.outcome_year
                        FROM outcome
                        INNER JOIN outcome_type ON outcome.outcome_type = outcome_type.type_id
                        INNER JOIN age_upon_outcome ON outcome.age_upon_outcome = age_upon_outcome.id
                        WHERE outcome_id = {itemid}
                    '''
            del columns[3]

        return json.dumps(dict(zip(columns, [i if i != 'null' else '---' for i in cur.execute(query).fetchall()[0]])))

app.run()

