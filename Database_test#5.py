import psycopg2

def create_database():
    conn = psycopg2.connect(database="database_test5", user="postgres", password="")
    with conn.cursor() as cur:
        cur.execute("""
        create table client_nsm (
        client_id int PRIMARY KEY,
        name VARCHAR(40) UNIQUE,
        sername VARCHAR(40) UNIQUE,
        male VARCHAR(70) UNIQUE
        );
        """)

        cur.execute("""
            create table number (
            number_id serial PRIMARY KEY,
            number VARCHAR(40) UNIQUE
            );
            """)

        cur.execute("""
                create table client_number (
                number_id int references number(number_id),
                client_id int references client_nsm(client_id),
                primary key(number_id, client_id)
                );
                """)

        conn.commit()
    conn.close()
    return


def add_data_to_database(client_id, name, sername, email, number = 0):

    conn = psycopg2.connect(database="database_test5", user="postgres", password="")
    with conn.cursor() as cur:
        cur.execute(f"""
            insert into client_nsm(client_id, name, sername, male)
            values
            ({client_id},'{name}', '{sername}', '{email}');          
            """)
        if number != 0:
            cur.execute(f"""
            insert into number(number)
            values
            ('{number}') returning number_id;
            """)
            number_id = cur.fetchone()
            cur.execute(f"""
            insert into client_number(number_id, client_id)
            values
            ({number_id[0]}, {client_id});
            """)
    conn.commit()
    return


#add_data_to_database(1, "mike", "mAdi", "mDas", 895)


def add_number(client_id, number):
    conn = psycopg2.connect(database="database_test5", user="postgres", password="")
    with conn.cursor() as cur:
        cur.execute(f"""
            select  * FROM client_nsm;            
            """)
        id_list = []
        for client_id_list in cur.fetchall():
            id_list.append(client_id_list[0])
        if client_id in id_list:
            cur.execute(f"""
                insert into number(number)
                values
                ({number}) returning number_id;          
                """)
            number_id = cur.fetchone()
            cur.execute(f"""
                insert into client_number(number_id, client_id)
                values
                ({number_id[0]}, {client_id});
                """)
        else:
            return print('Нет такого id')
    conn.commit()
    return

#add_number(1, 98818914)

def change_client_data():
    id = input('Введите id ')
    dict_of_change = eval(input('Введите данные подлежащие изменению в виде: {name: "новое значение", sername: "новое значение", male: "новое значение"} '))
    conn = psycopg2.connect(database="database_test5", user="postgres", password="")
    with conn.cursor() as cur:
        for change_data in dict_of_change:
            cur.execute(f"""
            UPDATE client_nsm SET {change_data}=%s WHERE client_id=%s;
            """, (dict_of_change.get(change_data), id))
    conn.commit()
    return

#change_client_data()


def delete_number(client_id):
    conn = psycopg2.connect(database="database_test5", user="postgres", password="")
    with conn.cursor() as cur:
        cur.execute("""
        DELETE FROM client_number WHERE client_id=%s returning number_id;        
        """, (f'{client_id}'))
        numbers_id = cur.fetchall()
        for number_id in numbers_id:
            cur.execute("""
            DELETE FROM number WHERE number_id=%s;
            """, (number_id))
    conn.commit()
    return
#delete_number(1)


def delete_client(client_id):
    conn = psycopg2.connect(database="database_test5", user="postgres", password="")
    with conn.cursor() as cur:
        cur.execute("""
        DELETE FROM client_number WHERE client_id=%s returning number_id;        
        """, (f'{client_id}'))
        numbers_id = cur.fetchall()
        cur.execute("""
        DELETE FROM client_nsm WHERE client_id=%s;        
        """, (f'{client_id}'))
        for number_id in numbers_id:
            cur.execute("""
            DELETE FROM number WHERE number_id=%s;
            """, (number_id))
    conn.commit()
    return
#delete_client(1)

def search_client():
    clients_info = eval(input('Введите данные для поиска в виде: {"name": "search_name"} '))
    conn = psycopg2.connect(database="database_test5", user="postgres", password="")
    with conn.cursor() as cur:
        for client_info in clients_info:
            if type(clients_info.get(client_info)) == str:
                cur.execute(f"""
                SELECT client_id FROM client_nsm WHERE {client_info}=%s;
                """, (f'{clients_info.get(client_info)}',))
                conn.commit()
                return print(cur.fetchone()[0])
            else:
                cur.execute(f"""
                SELECT number_id FROM number WHERE {client_info}=%s;
                """, (f'{clients_info.get(client_info)}',))
                number_id = cur.fetchone()[0]

                cur.execute(f"""
                SELECT client_id FROM client_number WHERE number_id=%s;
                """, (number_id,))
                conn.commit()
                return print(cur.fetchone()[0])

search_client()

