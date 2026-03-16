import sqlite3
from function.path import path_ubicacion
import streamlit as st





def modificar_proyecto(col,id_modificar,valor):
    DB_PATH= path_ubicacion()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

        #4. Pedimos el ID
    columna_modificar = col.lower()
    id_modificar = id_modificar
    valor_a_modificar = valor
        
    try:
        cursor.execute(f"UPDATE proyectos SET {columna_modificar} = ? WHERE id = ?",(valor_a_modificar,id_modificar,))
        st.success("Valor modificado")
        conn.commit()
            
    except sqlite3.OperationalError as e:
        st.warning(f"❌ Error de SQL: {e}. ¿Seguro que la tabla se llama 'proyectos'? o ¿Es correcto el nombre de la columna?")
    finally:
                try:
                    conn.close()
                except:
                    pass