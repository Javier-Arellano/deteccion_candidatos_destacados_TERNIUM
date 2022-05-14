

'''
Realizado por:
   Javier Hernández Arellano
   IDM
   A01730548

Instituto Tecnológico y de Estudios Superiores de Monterrey - Campus Monterrey

05 de mayo de 2022
'''


from http.client import OK
from json import load
from zlib import DEF_BUF_SIZE
import streamlit as st
import pickle
import numpy as np
from sklearn.svm import SVC


# CARGAR EL MODELO
file_pkl='linear_svm.pkl'
archivo_entrada = open(file_pkl, 'rb')
svm = pickle.load(archivo_entrada)
archivo_entrada.close()


def convert_scores (lista):
        if (lista == "No se recomienda" or lista == "No presentó"):
            return 0
        elif (lista == "Recomendado" or lista == "A1" or lista == "A2"):
            return 1
        elif (lista == "Altamente Recomendado"  or lista == "B1" or lista == "B2"):
            return 2
        elif (lista == "C1" or lista == "C2"):
            return 3
        else:
          return lista



def show_predict_page():

    # pickle_in = open("linear_svm.pkl", "rb")
    # svm = pickle.load(pickle_in)


    st.title("Selección de candidatos Altamente Destacados - Ternium")

    st.write("""## 1. Ingrese los scores para cada actividad realizada:""")

    # st.write("""## --- Candidato: A01730548 ---""")

    st.write("""### Pruebas pymetrics""")
    
    Op_Calidad_str = ("No se recomienda","Recomendado","Altamente Recomendado")
    DIGI_SC_str =  ("No se recomienda","Recomendado","Altamente Recomendado")
    MTTO_DIMA_str = ("No se recomienda","Recomendado","Altamente Recomendado")
    Resto_Soft_str = ("No se recomienda","Recomendado","Altamente Recomendado")
    Comercial_plan_str = ("No se recomienda","Recomendado","Altamente Recomendado")
    Ingles_nvl = ("No presentó","A1","A2","B1","B2","C1","C2")
    ActGrupal_scores = ("No presentó",1,2,3,4,5) # SCORE ACTIVIDAD GRUPAL

    ## --- CHECKBOXES PARA QUE EL USUARIO LAS LLENE ---
    OPC_box = st.selectbox("Operaciones-Calidad:", Op_Calidad_str)
    Comercial_box = st.selectbox("Comercial-Planeamiento:", Comercial_plan_str)
    DIGI_box = st.selectbox("DIGI-SC:", DIGI_SC_str)
    MTTO_box = st.selectbox("MTTO-DIMA:", MTTO_DIMA_str)
    Soft_box = st.selectbox("Resto Soft skills:", Resto_Soft_str)
    
    OPC = convert_scores(OPC_box)
    com_plan = convert_scores(Comercial_box)
    DIGI = convert_scores(DIGI_box)
    MTTO = convert_scores(MTTO_box)
    soft = convert_scores(Soft_box)
    suma_pym = (OPC + com_plan + DIGI + MTTO + soft)

    def Apto():
        if suma_pym == 0:
          return 0
        elif suma_pym > 0:
          return 1
    def Destacado_pym():
      if suma_pym >= 4:
        return 1
      else:
        return 0

    apto = Apto()
    dest_pym = Destacado_pym()
    
    def res_pym():
      if apto == 0:
        return "No apto"
      elif ((apto == 1 and dest_pym == 0)):
        return "Apto"
      elif dest_pym == 1:
        return "Destacado"
    
    resumen_pym = res_pym()


    st.write("""### Competencias""")
    ActGrupal_box =  st.selectbox("Actividad Grupal:", ActGrupal_scores)
    ag = convert_scores(ActGrupal_box)
    def res_ag():
      if (ag == 0 or ag == 1):
        return "No apto"
      elif (ag == 2 or ag == 3):
        return "Apto"
      elif (ag == 4 or ag == 5):
        return "Destacado"

    resumen_ag = res_ag() 


    st.write("""### Idioma Inglés""")
    Ingles_box = st.selectbox("Nivel de Inglés:",Ingles_nvl)
    ingles = convert_scores(Ingles_box)
    # resumen_ing = ""
    def Destacado_ing():
      if ingles >= 2:
        return 1
      else:
        return 0
    def res_ing():
      if ingles == 0:
        return "No apto"
      elif ingles == 1:
        return "Apto"
      elif (ingles == 2 or ingles == 3):
        return "Destacado"
    
    dest_ing = Destacado_ing()
    resumen_ing = res_ing()

    pred_button = st.button("EVALUAR CANDIDATO")
    if pred_button :
      st.write("Resumen pruebas pymetrics: ", resumen_pym)
      st.write("Resumen competencias: ", resumen_ag)
      st.write("Resumen inglés: ", resumen_ing)

      classes = {0: 'NO es Altamente Recomendado', 1: 'SI Altamente Recomendado'}
      prediction = svm.predict([[ag, apto, OPC, DIGI, MTTO, com_plan, soft, dest_pym, ingles, dest_ing]])
      # prediction = svm.predict([[5,1,2,2,2,2,1,1,3,1]])
      st.subheader(f"El candidato {classes[prediction[0]]}")

    

