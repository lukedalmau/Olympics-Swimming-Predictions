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

places = ["first", "second", "third"]



amount = st.sidebar.number_input(
    'Amount of simulations', min_value=1, value=100)
save_df_chckbx = st.sidebar.checkbox(
    "Save Dataframes of simulation as CSV", value=True)


predict_results_chckbx = st.sidebar.checkbox(
    "Predict Results by places", value=False)
save_predict_chckbx = st.sidebar.checkbox(
    "Save prediction as CSV", value=False)

    

full_predict_results_chckbx = st.sidebar.checkbox(
    "Full Prediction", value=False)
save_full_predict_chckbx = st.sidebar.checkbox(
    "Save full prediction as CSV", value=False)

path = r"./csv"
if os.path.isdir(path):
    st.info("Found a csv folder... Try to load it")
    st.info("Check Predict result before clicking Load data to show predictions of the loaded data instead")
    if st.button('Load data'):

        for root, dirs, files in os.walk(path):
            dfs = []
            for i, file in enumerate(files):
                if file.endswith("place.csv"):
                    simNum, filename = file.split("_")

                    name, extension = filename.split('.')

                    head, tail = name.split('-')

                    df = pd.read_csv(root+'/'+file)

                    dfs.append(df)

                    df_predict = df.groupby(
                        ['Event'], as_index=False).first().reset_index(drop=True)

                    if i % 3 == 2:
                        df_full_prediction = pd.concat([dfs.pop(), dfs.pop(), dfs.pop()]).groupby(['Event', 'Name', 'Team Code', 'Team Name'], as_index=False).sum().sort_values(
                            by=['Event', 'Percent'], ascending=False).reset_index(drop=True)

                    if predict_results_chckbx:
                        st.subheader(
                            f"Amount of simulations: {simNum} \n {head.capitalize()} {tail.capitalize()} Prediction")
                        st.dataframe(
                            df_predict[['Event', 'Name', 'Percent', 'Team Code']])

                    if full_predict_results_chckbx:

                        if i % 3 == 2:
                            st.subheader(
                                f"Amount of simulations: {simNum} \n Full Prediction")
                            st.dataframe(
                                df_full_prediction[['Event', 'Name', 'Percent', 'Team Code']])

                    else:
                        st.subheader(
                            f"Amount of simulations: {simNum} \n {head.capitalize()} {tail.capitalize()}")
                        st.dataframe(df)

                    if save_predict_chckbx:
                        predict_path = path+'/predictions'

                        if not os.path.isdir(predict_path):
                            os.mkdir(predict_path)

                        name = f'{simNum}_'+head+'-place_prediction.csv'

                        newpredict_path = predict_path+'/'+name

                        if os.path.exists(newpredict_path):
                            df_predict.to_csv(newpredict_path, index=False)
                        else:
                            open(newpredict_path, 'x')
                            df_predict.to_csv(newpredict_path, index=False)

                    if save_full_predict_chckbx:

                        if i % 3 == 2:

                            full_predict_path = path+'/predictions/full_prediction'

                            if not os.path.isdir(full_predict_path):
                                os.mkdir(full_predict_path)

                            name = f'{simNum}_full_prediction.csv'

                            newfull_predict_path = full_predict_path+'/'+name

                            if os.path.exists(newfull_predict_path):
                                df_full_prediction.to_csv(
                                    newfull_predict_path, index=False)
                            else:
                                open(newfull_predict_path, 'x')
                                df_full_prediction.to_csv(
                                    newfull_predict_path, index=False)


if st.button('Start Simulation'):
    clock = time.time()
    dfs = tournament_setup_deploy(amount)
    clock = time.time()-clock
    st.subheader(
        f"Done in {round(clock,1)} secs ~ {round(clock/60,1)} mins ~ {round(clock/(60**2),1)} h")
    for i, df in enumerate(dfs):
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
                df.to_csv(newpath, index=False)
            else:
                open(newpath, 'x')
                df.to_csv(newpath, index=False)

        if save_predict_chckbx:
            predict_path = path+'/predictions'

            if not os.path.isdir(predict_path):
                os.mkdir(predict_path)

            name = f'{amount}_'+places[i]+'-place_prediction.csv'

            newpath = predict_path+'/'+name

            if os.path.exists(newpath):
                df_predict.to_csv(newpath, index=False)
            else:
                open(newpath, 'x')
                df_predict.to_csv(newpath, index=False)
