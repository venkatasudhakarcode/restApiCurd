from db import get_connection

def get_student(student_id = None):
    conn = get_connection()
    if not conn:
        return None
    
    cursor = conn.cursor(dictionary=True)
    if student_id:
        cursor.execute("SELECT * FROM students WHERE id=%s",(student_id,))
        result = cursor.fetchone()
    else:
        cursor.execute("SELECT * FROM students")
        result = cursor.fetchall()
    
    conn.close()
    return result


    pass

def add_student(name, age):
    conn = get_connection()
    if not conn:
        return None
    
    cursor = conn.cursor()
    cursor.execute("INSERT INTO students(name,age) VALUES(%s, %s)",(name, age))

    conn.commit()
    conn.close()


def update_student(student_id, name):
    conn = get_connection()
    if not conn:
        return None
    
    cursor = conn.cursor()
    cursor.execute("update students set name=% where id=%s",(name, student_id))
    conn.commit()
    affectedrows = cursor.rowcount
    conn.close()
    return affectedrows

def delete_student(student_id):
    conn = get_connection()
    if not conn:
        return None
    cursor = conn.cursor()
    cursor.execute("DELETE from students WHERE id=%",(student_id,))
    conn.commit()
    affected = cursor.rowcount
    conn.close()
    return affected

