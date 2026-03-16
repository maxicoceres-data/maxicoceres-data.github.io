import sqlite3
from function.path import path_ubicacion
import streamlit as st



def eliminar_proyecto(id_eliminar):
            DB_PATH= path_ubicacion()
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()      
            # cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            # tablas = cursor.fetchall()
            # st.wirte(f"Tablas en la DB: {tablas}")

            #4. Pedimos el ID
            id_a_eliminar = id_eliminar

            try:
                # 5. Ejecutamos con la coma (,) al final para que sea una tupla
                cursor.execute("DELETE FROM proyectos WHERE id = ?", (id_a_eliminar,))
            
                # 6. Verificamos si realmente se borró algo
                if cursor.rowcount > 0:
                    conn.commit()
                    st.success(f"✅ Éxito: Proyecto con ID {id_a_eliminar} eliminado.")
                    
                else:
                    st.warning(f"⚠️ Atención: No se encontró ningún proyecto con el ID {id_a_eliminar}.")

            except sqlite3.OperationalError as e:
                st.error(f"❌ Error de SQL: {e}. ¿Seguro que la tabla se llama 'proyectos'?")
            finally:
                try:
                    conn.close()
                except:
                    pass