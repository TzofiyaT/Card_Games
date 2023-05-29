import sqlite3


class Score:
    def __init__(self, name):
        self.player_name = name
        self.hand_cards = ""
        self.score = "0"
        self.pile = ""
        self.deal = ""


def create_sql_file(file_name: str) -> bool:
    conn = sqlite3.connect(file_name)
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS score(
    id integer primary key,
    player_name text,
    hand_cards text,
    score integer,
    pile text,
    deal text);""")
    conn.commit()
    cursor.close()
    return True


def insert_to_sql_file(file_name: str, list_to_insert: Score) -> bool:
    conn = sqlite3.connect(file_name, check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO score "
                   "(player_name, hand_cards, score, pile, deal) VALUES (?,?,?,?,?)",
                   (list_to_insert.player_name, list_to_insert.hand_cards, list_to_insert.score,
                    list_to_insert.pile, list_to_insert.deal,))
    conn.commit()
    cursor.close()
    return True


def read_from_sql_file(file_name: str, choose):
    conn = sqlite3.connect(file_name)
    cursor = conn.cursor()
    cursor.execute(f"SELECT {choose} FROM score")
    data_table = cursor.fetchall()
    conn.commit()
    cursor.close()
    return data_table


def read_from_sql_file_by_others(file_name: str, choose, column, colunm_value):
    conn = sqlite3.connect(file_name)
    cursor = conn.cursor()
    cursor.execute(f"SELECT {choose} FROM score WHERE {column}=? ", (colunm_value,))
    data_table = cursor.fetchall()
    conn.commit()
    cursor.close()
    return data_table


def read_from_sql_file_by_two_conditions(file_name: str, column1, type1, column2, type2, data1, data2):
    conn = sqlite3.connect(file_name)
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM score WHERE {column1}{type1}? AND {column2}{type2}?", (data1, data2,))
    data_table = cursor.fetchall()
    conn.commit()
    cursor.close()
    return data_table


def update_sql_file_by_others(file_name: str, column_change, data_column_change, by_column, data_by_column):
    conn = sqlite3.connect(file_name)
    cursor = conn.cursor()
    cursor.execute(f"UPDATE score SET {column_change}=? WHERE {by_column}=? ", (data_column_change, data_by_column,))
    data_table = cursor.fetchall()
    conn.commit()
    cursor.close()
    return data_table


def delete_sql_file_by_others(file_name: str, by_column, data_by_column):
    conn = sqlite3.connect(file_name)
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM score WHERE {by_column}=? ", (data_by_column,))
    data_table = cursor.fetchall()
    conn.commit()
    cursor.close()
    return data_table


if __name__ == '__main__':
    pass