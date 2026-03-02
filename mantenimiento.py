from pathlib import Path
import sqlite3


BASE_DIR = Path(__file__).resolve().parent
conn = sqlite3.connect(BASE_DIR /"data" / "proyectos.db")
cursor = conn.cursor()


cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tablas = cursor.fetchall()
print(f"Tablas en la DB: {tablas}")

#4. Pedimos el ID
id_a_eliminar = input("ID del proyecto a eliminar: ")

try:
    # 5. Ejecutamos con la coma (,) al final para que sea una tupla
    cursor.execute("DELETE FROM proyectos WHERE id = ?", (id_a_eliminar,))
    
    # 6. Verificamos si realmente se borró algo
    if cursor.rowcount > 0:
        conn.commit()
        print(f"✅ Éxito: Proyecto con ID {id_a_eliminar} eliminado.")
    else:
        print(f"⚠️ Atención: No se encontró ningún proyecto con el ID {id_a_eliminar}.")

except sqlite3.OperationalError as e:
    print(f"❌ Error de SQL: {e}. ¿Seguro que la tabla se llama 'proyectos'?")

finally:
    conn.close()