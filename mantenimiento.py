from pathlib import Path
import sqlite3


BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR /"data" / "proyectos.db"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()



seleccionar_opcion = int(input("""Seleccionar una opcion de mantenimiento: 
                               1 (modificar), 
                               2 (eliminar),
                               0 (salir): """))


while True:
    if seleccionar_opcion not in [1,2,0]:
        print("Opcion Incorrecta")
        seleccionar_opcion = int(input("""Seleccionar una opcion de mantenimiento: 
                               1 (modificar), 
                               2 (eliminar),
                               0 (salir): """))
        continue
    
    if seleccionar_opcion == 2:
        
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
                break
            else:
                print(f"⚠️ Atención: No se encontró ningún proyecto con el ID {id_a_eliminar}.")

        except sqlite3.OperationalError as e:
            print(f"❌ Error de SQL: {e}. ¿Seguro que la tabla se llama 'proyectos'?")
        
    elif seleccionar_opcion == 1:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tablas = cursor.fetchall()
        print(f"Tablas en la DB: {tablas}")

        #4. Pedimos el ID
        columna_modificar = input("Columna a modificar: ").lower()
        id_modificar = input("ID del proyecto a modificar: ")
        valor_a_modificar = input("Escribe la modificación, (si es tecnologias, escribir de nuevo las tecnologías)")
        
        try:
            cursor.execute(f"UPDATE proyectos SET {columna_modificar} = ? WHERE id = ?",(valor_a_modificar,id_modificar,))
            print("Valor modificado")
            conn.commit()
            break
            
        except sqlite3.OperationalError as e:
            print(f"❌ Error de SQL: {e}. ¿Seguro que la tabla se llama 'proyectos'? o ¿Es correcto el nombre de la columna?")
        
    elif seleccionar_opcion == 0:
        print("Mantenimiento cerrado")
        break
    

conn.close()
        
        