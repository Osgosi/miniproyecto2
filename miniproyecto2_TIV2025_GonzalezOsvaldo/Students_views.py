# -*- coding: utf-8 -*-
"""
Created on Mon Jun 23 23:01:43 2025

@author: osgos
"""

#Carga de liberías necesarias para la aplicación.
import streamlit as st
import pandas as pd
import os
import plotly.express as px

class AppStudents:
    def __init__(self):
        try:
            path = os.path.join(os.getcwd(), "estudiantes.csv")
            st.session_state.df = pd.read_csv(path)
            st.session_state.estudiantes = st.session_state.df.to_dict(orient="records")
            st.success("Estudiantes recuperados exitosamente del archivo")
        except FileNotFoundError:
            st.session_state.estudiantes = []
            st.session_state.df = pd.DataFrame()
        
    def RegStudent_View(self):
        st.set_page_config(page_title='Nuevo registro', page_icon="🤓")
        
        st.title("Registro de nuevos alumnos")
        st.write("Por favor, complete los campos con la información solicitada:")
        with st.form("students_form"):
            name = st.text_input('Nombre completo',
                                 placeholder='Nombre completo del alumno')
            #Crear una lista de las carreras para reducir la instrucción en el SelectBox.
            career_list = ['Seleccione una carrera...', 'Ingenieria Industrial', 'Ingenieria Mecánica y Electrica', 'Ingenieria Mecatronica',
                           'Contabilidad', 'Nutricion', 'Psicologia', 'Derecho']
            career = st.selectbox('Licenciatura', career_list, index=0)
            #Para optimizar espacio, la edad y la pregunta de alumno regular separadas en columnas.
            col1, col2 = st.columns(2)
            with col1:
                age = st.slider('Edad', min_value=16, max_value=99, value=18)
            with col2:
                regular_std = st.checkbox('¿Es alumno regular?')
            btn_registrar = st.form_submit_button('Enviar formulario')
        
#Envío de información y validación de "no vacíos"
        if btn_registrar:
            if not name:  #Valida que el campo de Nombre NO esté vacío.
                st.warning("El campo nombre no puede estar vacío.")
            elif career == 'Seleccione una carrera...': #Como no es posible dejar por defecto vacío el Widget, se coloca una opción
                                                        #comparar que se ha elegido una Carrera válida.
                st.warning("Licenciatura inválida\nPor favor, seleccione una carrera.")
            elif age < 18: #Al iniciar en 16, el slider no tiene un valor "vacío", por lo que se hace una comparativa por edad del aspirante.
                st.error("El alummno que intentas registrar es menor de edad.") 
            else:
                with st.expander("Ocultar detalles de registro", expanded=True):
                    def show_resumen():
                        st.write("Datos del estudiante registrado:")
                        st.write(f"**Nombre:**  {name}")
                        st.write(f"**Carrera:** {career}")
                        st.write(f"**Edad:** {age}")
                        st.write(f"**Regular:** {'Si' if regular_std else 'No'}")
                        if st.button("Cerrar"):
                            st.rerun()    
                    nuevo = {
                            'Nombre': name,
                            'Carrera': career,
                            'Edad': age,
                            'Regular': regular_std}
                    
                    st.session_state.estudiantes.append(nuevo)
                    show_resumen()
                    #st.success('Estudiante registrado correctamente')
                    #Crear un diálogo para que muestre un resumen de alumno guardado.
                #st.dialog("Registro exitoso")
                    
                    
                    
                st.session_state.df = pd.DataFrame(st.session_state.estudiantes)
                    #Crear la variable path con la función getcwd para obtener la ruta de trabajo actual
                    #y la concatena con el archivo indicado.
                path = os.path.join(os.getcwd(), "estudiantes.csv")
                st.session_state.df.to_csv(path, index=False)

    def vista_consulta_alumnos(self):
        st.set_page_config(page_title="Consulta de registro de alumnos")
        col1, col2 = st.columns(2)
        with col1:
            st.title("Consulta de estudiantes registrados")
        with col2:
            with st.expander("Exportar datos a csv"):
                file_name = st.text_input("Indica el nombre de tu archivo")
                path = st.text_input("Indica la ruta para guardar tu archivo:")
                btn_export = st.button("Exportar a csv")
        
        if btn_export:
            if 'df' in st.session_state:
                df = st.session_state.df
                if file_name.strip() and path.strip():
                    fullPath = os.path.join(path, file_name)
                    try:
                        df.to_csv(fullPath, index=False)
                        st.success(f"Archivo guardado en: {fullPath}")
                    except Exception as e:
                            st.error(f"Error al guardar: {e}")
                else:
                    st.warning("Ambos campos deben estar llenos")    
                
            
        with st.expander("Mostrar tabla de alumnos registrados"):
             if not st.session_state.df.empty: #Valida que el archivo exista o no esté vacío.
                 st.dataframe(st.session_state.df)
             else:
                 st.warning("Aún no hay registro de estudiantes")
                 
              
        df = st.session_state.df
        if not df.empty: #Se crea un objeto para la variable de los datos y llamarla de forma más fácil.
            Fcareer = ['Seleccione una carrera...', 'Ingenieria Industrial', 'Ingenieria Mecánica y Electrica', 'Ingenieria Mecatronica',
                           'Contabilidad', 'Nutricion', 'Psicologia', 'Derecho']
            with st.expander("Seleccione las carreras a graficar"):
                selection = st.multiselect("Selecciona las carreras", Fcareer, default=Fcareer)
            #Botón para guardar los datos.
            
            Std_Count = df['Carrera'].isin(selection)
            df_filter = df[Std_Count]
            #Condción para contar alumos y alimentar el gráfico.
            count = df_filter['Carrera'].value_counts().reset_index()
            count.columns = ['Carrera', 'NumStd']
            #Gráfico con registro de alumnos por carrera.
            fig = px.bar(
                  count,
                  x="Carrera",
                  y="NumStd",
                  color="Carrera")
            #Formato de la gráfica para mejorar la presentación de los datos.
            fig.update_layout( #Presentación del título al centro.
                  title={"text": 'Cantidad de alumnos inscritos',
                                "x": 0.5,
                                "xanchor": 'center',
                                "yanchor": 'top'})
            fig.update_layout( #Cambio de nombre de 
                  yaxis_title="Número de alumnos inscritos")
            fig.update_yaxes(tickmode='linear')
            st.plotly_chart(fig)
        else:
            "No hay registro de alumnos"
        
            
   
        

    def run(self):
        st.sidebar.title("Menu")
        opcion = st.sidebar.selectbox('Ir a:', ["Registro", "Consulta"])
        if opcion == 'Registro':
            self.RegStudent_View()
        elif opcion == 'Consulta':
            self.vista_consulta_alumnos()

#Mandar llamar la aplicación para ejecutarse.        
App = AppStudents()
App.run()