import os
import time

from pandas.core.indexes.base import Index
from tournaments_setup_deploy import tournament_setup_deploy
import streamlit as st
import pandas as pd
import matplotlib as plt
import plotly.figure_factory as ff

import base64

'''
# GIA-OLYMPICS

# SWIMMING COMPETITION
'''


@st.cache(allow_output_mutation=True)
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()


def set_png_as_page_bg(png_file):
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = '''
    <style>
    body {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str

    st.markdown(page_bg_img, unsafe_allow_html=True)
    return


def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


def remote_css(url):
    st.markdown(f'<link href="{url}" rel="stylesheet">',
                unsafe_allow_html=True)


local_css("style.css")
remote_css('https://fonts.googleapis.com/icon?family=Material+Icons')


set_png_as_page_bg('tokyo_pool.png')

places=["first","second","third"]

amount = st.sidebar.number_input('Amount of simulations',min_value=1,value=100)
save_df_chckbx = st.sidebar.checkbox("Save Dataframes as CSV",value=True)
predict_results_chckbx = st.sidebar.checkbox("Predict Results", value=False)
save_predict_chckbx = st.sidebar.checkbox("Save prediction as CSV", value=False)


path = r"./csv"
if os.path.isdir(path):
    st.info("Found a csv folder... Try to load it")
    if st.button('Load data'):
        dfs = []
        for root,dirs,files in os.walk(path):
            for file in files:
                if file.endswith(".csv"):
                    simNum,filename = file.split("_")
                    
                    name,extension = filename.split('.')
                    
                    head,tail = name.split('-')

                    df = pd.read_csv(root+'/'+file)
                    
                    if predict_results_chckbx:
                        st.subheader(
                            f"Amount of simulations: {simNum} \n {head.capitalize()} {tail.capitalize()} Prediction")
                        st.dataframe(df.groupby(
                            ['Event'], as_index=False).first().reset_index(drop=True))
                    else:

                        st.subheader(
                            f"Amount of simulations: {simNum} \n {head.capitalize()} {tail.capitalize()}")
                        st.dataframe(df)
                        


if st.button('Start Simulation'):
    clock = time.time()
    dfs = tournament_setup_deploy(amount)
    clock=time.time()-clock
    st.subheader(
        f"Done in {round(clock,1)} secs ~ {round(clock/60,1)} mins ~ {round(clock/(60**2),1)} h")
    for i,df in enumerate(dfs):
        df_predict = df.groupby(
            ['Event'], as_index=False).first().reset_index(drop=True)

        if predict_results_chckbx:
            st.subheader(
                f"Amount of simulations: {simNum} \n {head.capitalize()} {tail.capitalize()} Prediction")
            st.dataframe(df_predict)

        else:
            st.subheader(f"{places[i].capitalize()} Place")
            st.dataframe(df)
        
        if save_df_chckbx:

            if not os.path.isdir(path):
                os.mkdir(path)

            name = f'{amount}_'+places[i]+'-place.csv'

            newpath = path+'/'+name

            if os.path.exists(newpath):
                df.to_csv(newpath,index = False)
            else:
                open(newpath,'x')
                df.to_csv(newpath, index=False)

        if save_predict_chckbx:
            predict_path=path+'/predictions'

            if not os.path.isdir(predict_path):
                os.mkdir(predict_path)

            name = f'{amount}_'+places[i]+'-place_prediction.csv'

            newpath = predict_path+'/'+name

            if os.path.exists(newpath):
                df.to_csv(newpath,index = False)
            else:
                open(newpath,'x')
                df.to_csv(newpath, index=False)
