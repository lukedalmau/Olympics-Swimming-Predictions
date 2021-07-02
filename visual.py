from datetime import datetime
import os
from swimmer import Swimmer
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

############           STYLING             ########################################

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

####################################################################################




##############        PERSISTENT DATA          #####################################

@st.cache(allow_output_mutation=True)
def EliminatedSwimmers():
    return {}


@st.cache(allow_output_mutation=True)
def AddedSwimmers():
    return {}


@st.cache(allow_output_mutation=True)
def Events():

    return []

###################################################################################


eliminated_swimmers = EliminatedSwimmers()

added_swimmers = AddedSwimmers()

events = Events()

if len(events)==0:
    events = [
        "M-800-FREESTYLE-LCM",
        "M-50-FREESTYLE-LCM",
        "M-400-MEDLEY-LCM",
        "M-400-FREESTYLE-LCM",
        "M-200-MEDLEY-LCM",
        "M-200-FREESTYLE-LCM",
        "M-200-BUTTERFLY-LCM",
        "M-200-BREASTSTROKE-LCM",
        "M-200-BACKSTROKE-LCM",
        "M-1500-FREESTYLE-LCM",
        "M-100-FREESTYLE-LCM",
        "M-100-BUTTERFLY-LCM",
        "M-100-BREASTSTROKE-LCM",
        "M-100-BACKSTROKE-LCM",
        "F-800-FREESTYLE-LCM",
        "F-50-FREESTYLE-LCM",
        "F-400-MEDLEY-LCM",
        "F-400-FREESTYLE-LCM",
        "F-200-MEDLEY-LCM",
        "F-200-FREESTYLE-LCM",
        "F-200-BUTTERFLY-LCM",
        "F-200-BREASTSTROKE-LCM",
        "F-200-BACKSTROKE-LCM",
        "F-1500-FREESTYLE-LCM",
        "F-100-FREESTYLE-LCM",
        "F-100-BUTTERFLY-LCM",
        "F-100-BREASTSTROKE-LCM",
        "F-100-BACKSTROKE-LCM"
    ]
    events.sort()


choice = st.sidebar.selectbox('Menu', ['Simulate', 'Modify current data'])




places = ["first", "second", "third"]

epoch = datetime(1970, 1, 1)

st.sidebar.subheader("Select the range of time you want the data")
from_date = st.sidebar.date_input(
    'Since:', value=epoch, min_value=epoch, max_value=datetime.today())
to_date = st.sidebar.date_input(
    'Until:', min_value=epoch, max_value=datetime.today())

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




if choice == 'Simulate':
    
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

                        if not any([predict_results_chckbx,full_predict_results_chckbx]):
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


    if st.checkbox('Show added swimmers'):
        st.table(added_swimmers)

    if st.checkbox('Show eliminated swimmers'):
        st.table(eliminated_swimmers)

    if st.button('Start Simulation'):
        clock = time.time()
        dfs = tournament_setup_deploy(
            amount,
            added_swimmers = added_swimmers,
            eliminated_swimmers = eliminated_swimmers,
            from_date = from_date,
            to_date = to_date)
        clock = time.time()-clock
        st.subheader(
            f"Done in {round(clock,1)} secs ~ {round(clock/60,1)} mins ~ {round(clock/(60**2),1)} h")
        for i, df in enumerate(dfs):

            df_predict = df.groupby(
                ['Event'], as_index=False).first().reset_index(drop=True)
            
            if i % 3 == 2:
                df_full_prediction = pd.concat([dfs[0], dfs[1], dfs[2]]).groupby(
                    ['Event', 'Name', 'Team Code', 'Team Name'], as_index=False).sum().sort_values(
                    by=['Event', 'Percent'], ascending=False).reset_index(drop=True)

            if predict_results_chckbx:
                st.subheader(
                    f"Amount of simulations: {amount} \n {head.capitalize()} {tail.capitalize()} Prediction")
                st.dataframe(df_predict)
            
            if full_predict_results_chckbx:
        
                if i % 3 == 2:
                    st.subheader(
                        f"Amount of simulations: {amount} \n Full Prediction")
                    st.dataframe(
                        df_full_prediction[['Event', 'Name', 'Percent', 'Team Code']])

            if not any([predict_results_chckbx, full_predict_results_chckbx]):
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

            if save_full_predict_chckbx:
        
                if i % 3 == 2:

                    full_predict_path = path+'/predictions/full_prediction'

                    if not os.path.isdir(full_predict_path):
                        os.mkdir(full_predict_path)

                    name = f'{amount}_full_prediction.csv'

                    newfull_predict_path = full_predict_path+'/'+name

                    if os.path.exists(newfull_predict_path):
                        df_full_prediction.to_csv(
                            newfull_predict_path, index=False)
                    else:
                        open(newfull_predict_path, 'x')
                        df_full_prediction.to_csv(
                            newfull_predict_path, index=False)

else:
    modify_choice = st.selectbox(
        'Options', ['--------','Add a Swimmer', 'Eliminate a Swimmer', 'Add an event', 'Eliminate an event'])
    if modify_choice == 'Add a Swimmer':
        swimmer_name = st.text_input('Name',value="LAST NAME, First Name")
        if len(swimmer_name)==0:
            st.warning('Please enter a name')
        else:
            swimmer_team_code = st.text_input('Team Code', value="CUB")

            swimmer_team_name = st.text_input(
                'Team Name', value="Cuba")

            swimmer_best_time = st.number_input(
                'Enter the best time of the swimmer\'s swim times (in seconds)', min_value=0.0, value=50.9,max_value=200*60*60.0)

            swimmer_mean = st.number_input(
                'Enter the mean of the swimmer\'s swim times (in seconds)',min_value = 0.0,value = 50.9, max_value=200*60*60.0 )

            swimmer_variance = st.number_input(
                'Enter the variance of the swimmer\'s swim times (in seconds)',min_value = 0.0,value = 0.0211234, max_value=100.0 )
            
            swimmer_event = st.selectbox('Select the event to add this swimmer',events)

            if st.button('Add'):
                try:

                    added_swimmers[swimmer_event].append(Swimmer(
                    
                        swimmer_name,
                        swimmer_best_time,
                        swimmer_mean,
                        swimmer_variance,
                        swimmer_team_code.upper(),
                        swimmer_team_name.capitalize()
                        )
                    )
                except KeyError:
                    added_swimmers[swimmer_event] = []
                    added_swimmers[swimmer_event].append(Swimmer(

                        swimmer_name,
                        swimmer_best_time,
                        swimmer_mean,
                        swimmer_variance,
                        swimmer_team_code.upper(),
                        swimmer_team_name.capitalize()
                    )
                    )
                st.info('Successfully added')

    if modify_choice == 'Eliminate a Swimmer' :
        swimmer_name_to_eliminate = st.text_input('Name', value="PHELPS, Michael")
        if len(swimmer_name_to_eliminate) == 0:
            st.warning('Please enter a name')
        else:
            eliminated_swimmer_event = st.selectbox(
                'Select the event to add this swimmer', events)

            if st.button("Eliminate"):
                try:

                    eliminated_swimmers[eliminated_swimmer_event].append(swimmer_name_to_eliminate)
                except KeyError:
                    eliminated_swimmers[eliminated_swimmer_event]=[]

                    eliminated_swimmers[eliminated_swimmer_event].append(
                        swimmer_name_to_eliminate)
                st.info('Successfully deleted')

    if modify_choice == 'Add an event' :
        event = st.text_input('Event name', value="M-400-FREESTYLE-LCM")
        if len(event) == 0:
            st.warning('Please enter an event')
        if st.button('Add'):
            events.append(event)
            st.info('Event successfully added')

    if modify_choice == 'Eliminate an event' :
        event2eliminate = st.selectbox('EVENTS TO SELECT',events)
        if st.button("Eliminate"):
            events.remove(event2eliminate)
            st.info('Event successfully deleted')
