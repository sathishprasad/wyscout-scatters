 # -*- coding: utf-8 -*-
"""
Created on Tue Jul 20 19:34:51 2021
@author: Sathish
"""
import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt
import snowflake.connector
from matplotlib.font_manager import FontProperties

st.set_option('deprecation.showPyplotGlobalUse', False)





@st.cache(allow_output_mutation=True)
def connect(gender):
# Enter your Snowflake account information
    ACCOUNT = "uh37708.europe-west2.gcp"
    USER = "totalfootballanalysis"
    PASSWORD = "CrevillenteSNOWFLAKE2023"
    DATABASE = "WEBAPP"
    SCHEMA = "XGOLD"
    WAREHOUSE = "XGOLD"
# Connect to Snowflake using the connector library
    cnx = snowflake.connector.connect(
    user=USER,
    password=PASSWORD,
    account=ACCOUNT,
    warehouse=WAREHOUSE,
    database=DATABASE,
    schema=SCHEMA
    )

    if gender=='Men':
        data = pd.read_sql_query('SELECT * FROM MASTERDATA',cnx)
        data = data[data['Type of data']=='per 90']
        data['League'] = data['League Name']
        data['Position'] = data['Categorical position']
        data['Name'] = data['Player']
        data['Minutes'] = data['Minutes played']
        data['Age'] = data['Age'].fillna(0)
        data['Age'] = pd.to_numeric(data['Age'], errors='coerce')
    else:
        data = pd.read_sql_query("SELECT * FROM WOMENDATA",cnx)
        data['League'] = data['League Name']
        data['Position'] = data['Categorical position']
        data['Name'] = data['Player']
        data['Minutes'] = data['Minutes played']




   
    return data
      

definition = pd.read_excel("datadef.xlsx")
    

def create_scatter(player,data,metric1,metric2,pos,league,szn):
    font_normal2 = st.session_state['font_normal2']
    font_normal1 = st.session_state['font_normal1']
    plt.rcParams['axes.facecolor'] = st.session_state['bg']
    if st.session_state['font_normal2'] =='/PPTelegrafUltraBold.otf':
            plt.rcParams['font.family'] = st.session_state['font_normal2']
    elif st.session_state['font_normal2'] =='/Quicksand-Bold.ttf':
            plt.rcParams['font.family'] = st.session_state['font_normal2']
    fig = plt.figure(figsize=(16, 12))
    fig.set_facecolor(st.session_state['bg'])  # Replace '#16003B' with your desired background color
    
    title = metric1 +" vs "+metric2
    title2 = "All " + pos +"s from " + league +" - Season " + szn
    plt.suptitle(title,fontproperties=st.session_state['font_normal2'],color='white',fontsize=24,y=0.94)
    plt.title(title2,fontproperties=st.session_state['font_normal2'],color='white',fontsize=21,y=1)
    plt.xlabel(metric1,color='white',fontproperties=st.session_state['font_normal2'],fontsize=12)
    plt.ylabel(metric2,color='white',fontproperties=st.session_state['font_normal2'],fontsize=12)

    plt.grid(True, color='white', linestyle='--', linewidth=0.5)

    # Hide the top and right spines
    ax = plt.gca()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    ax.spines['left'].set_color('white')
    ax.spines['bottom'].set_color('white')

    tick_font = font_normal2

    # Set the axis tick labels to white color, adjust the font size, and rotate them by 45 degrees
    ax.tick_params(axis='x', labelcolor='white', labelsize=10)
    ax.tick_params(axis='y', labelcolor='white', labelsize=10)

    # Plot average lines

    average_goalpershot = np.mean(data[metric1])
    average_xgpershot = np.mean(data[metric2])
    plt.axvline(average_goalpershot, color='white', linestyle='--')
    plt.axhline(average_xgpershot, color='white', linestyle='--')



    data.reset_index(inplace=True,drop=True)

    for i in range(0,len(data)):
                    name = data['Name'][i]
                    x = data[metric1][i]
                    y = data[metric2][i]
                    if name==player:
                      sc = plt.scatter(x, y, s=400, c=st.session_state['h1'], marker='o', zorder=1,edgecolor=st.session_state['b'],linewidth=2,hatch='///',alpha=0.7)
                      plt.annotate(name, (x, y-0.009), fontsize=10, color='white', ha='center', va='top', fontproperties=st.session_state['font_normal2'])
                    else:
                      sc = plt.scatter(x, y, s=300, c=st.session_state['h2'], marker='o', zorder=0,alpha=0.1,edgecolor=st.session_state['h2'],linewidth=2,hatch='///')
                      if x>average_goalpershot and y>average_xgpershot:
                        plt.annotate(name, (x, y-0.009), fontsize=9, color='white', ha='center', va='top', fontproperties=st.session_state['font_normal2'],alpha=0.2)


    fdj_cropped = Image.open('smartscout.png')
    logo= Image.open('Logo.png')
    logo1 = Image.open('logo3.png')
    avid = Image.open('avid.png')
    gcfc = Image.open('gcfc.png')
    vs = Image.open('Virtual-Scout-White.png')

    new_size1 = (100, 130)
    new_size = (170, 170)
    new_size2= (150,30)# Adjust the size as needed
    fdj_cropped_resized = fdj_cropped.resize(new_size1)
    logo_resized = logo.resize(new_size)
    logo3_resized = logo1.resize(new_size1)
    avid_resized = avid.resize((120,35))
    gcfc_resized = gcfc.resize(new_size)
    vs_resized = vs.resize(new_size2)

    # Add the resized images to the plot
    if st.session_state['template'] == 'SS':
            plt.figimage(fdj_cropped_resized, xo=15, yo=1960,alpha=0.5)  # Adjust the coordinates (xo, yo) as needed
    if st.session_state['template'] == 'TFA':
            plt.figimage(logo_resized, xo=2450, yo=1960)
    if st.session_state['template'] == 'Minnesota':
            plt.figimage(logo3_resized, xo=2450, yo=1960)
    if st.session_state['template'] == 'Avid':
            plt.figimage(avid_resized, xo=2450, yo=1990)
    if st.session_state['template'] == 'Game Changer FA':
            plt.figimage(gcfc_resized, xo=2450, yo=1960)
    if st.session_state['template'] == 'Virtual Scout':
            plt.figimage(vs_resized, xo=2400, yo=1970)


    st.pyplot(fig)
    

def create_league_scatter(player,data,metric1,metric2,pos,league,szn,player2):
    font_normal2 = st.session_state['font_normal2']
    font_normal1 = st.session_state['font_normal1']
    plt.rcParams['axes.facecolor'] = st.session_state['bg']
    if st.session_state['font_normal2'] =='/PPTelegrafUltraBold.otf':
            plt.rcParams['font.family'] = st.session_state['font_normal2']
    elif st.session_state['font_normal2'] =='/Quicksand-Bold.ttf':
            plt.rcParams['font.family'] = st.session_state['font_normal2']
    fig = plt.figure(figsize=(16, 12))
    fig.set_facecolor(st.session_state['bg'])  # Replace '#16003B' with your desired background color
    
    title = metric1 +" vs "+metric2
    title2 = "Season " + szn
    plt.suptitle(title,fontproperties=font_normal2,color='white',fontsize=24,y=0.94)
    plt.title(title2,fontproperties=font_normal2,color='white',fontsize=21,y=1)
    plt.xlabel(metric1,color='white',fontproperties=font_normal2,fontsize=12)
    plt.ylabel(metric2,color='white',fontproperties=font_normal2,fontsize=12)

    plt.grid(True, color='white', linestyle='--', linewidth=0.5)

    # Hide the top and right spines
    ax = plt.gca()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    ax.spines['left'].set_color('white')
    ax.spines['bottom'].set_color('white')

    tick_font = font_normal2

    # Set the axis tick labels to white color, adjust the font size, and rotate them by 45 degrees
    ax.tick_params(axis='x', labelcolor='white', labelsize=10)
    ax.tick_params(axis='y', labelcolor='white', labelsize=10)

    # Plot average lines

    average_goalpershot = np.mean(data[metric1])
    average_xgpershot = np.mean(data[metric2])
    plt.axvline(average_goalpershot, color='white', linestyle='--')
    plt.axhline(average_xgpershot, color='white', linestyle='--')



    data.reset_index(inplace=True,drop=True)

    for i in range(0,len(data)):
                    name = data['Name'][i]
                    x = data[metric1][i]
                    y = data[metric2][i]
                    if name==player:
                      sc = plt.scatter(x, y, s=400, c=st.session_state['h1'], marker='o', zorder=1,edgecolor=st.session_state['b'],linewidth=2,hatch='///',alpha=0.7)
                      plt.annotate(name, (x, y-0.009), fontsize=10, color='white', ha='center', va='top', fontproperties=font_normal2)
                    elif name in player2:
                        sc = plt.scatter(x, y, s=400, c=st.session_state['h3'], marker='o', zorder=1,edgecolor=st.session_state['b'],linewidth=2,hatch='///',alpha=0.7)
                        plt.annotate(name, (x, y-0.009), fontsize=10, color='white', ha='center', va='top', fontproperties=font_normal2)
                    else:
                        sc = plt.scatter(x, y, s=300, c=st.session_state['h2'], marker='o', zorder=0,alpha=0.1,edgecolor=st.session_state['h2'],linewidth=2,hatch='///')
                        if x>average_goalpershot and y>average_xgpershot:
                            plt.annotate(name, (x, y-0.009), fontsize=9, color='white', ha='center', va='top', fontproperties=st.session_state['font_normal2'],alpha=0.2)


    fdj_cropped = Image.open('smartscout.png')
    logo= Image.open('Logo.png')
    logo1 = Image.open('logo3.png')
    avid = Image.open('avid.png')
    gcfc = Image.open('gcfc.png')

    new_size1 = (100, 130)
    new_size = (170, 170)   # Adjust the size as needed
    fdj_cropped_resized = fdj_cropped.resize(new_size1)
    logo_resized = logo.resize(new_size)
    logo3_resized = logo1.resize(new_size1)
    avid_resized = avid.resize((120,35))
    gcfc_resized = gcfc.resize(new_size)

    # Add the resized images to the plot
    if st.session_state['template'] == 'SS':
            plt.figimage(fdj_cropped_resized, xo=15, yo=1960,alpha=0.5)  # Adjust the coordinates (xo, yo) as needed
    if st.session_state['template'] == 'TFA':
            plt.figimage(logo_resized, xo=2450, yo=1960)
    if st.session_state['template'] == 'Minnesota':
            plt.figimage(logo3_resized, xo=2450, yo=1960)
    if st.session_state['template'] == 'Avid':
            plt.figimage(avid_resized, xo=2450, yo=1990)
    if st.session_state['template'] == 'Game Changer FA':
            plt.figimage(gcfc_resized, xo=2450, yo=1960)
    
    st.pyplot(fig)
        
    
def create_player_scatter(player,data,metric1,metric2,pos,league,szn,player2):
    font_normal2 = st.session_state['font_normal2']
    font_normal1 = st.session_state['font_normal1']
    plt.rcParams['axes.facecolor'] = st.session_state['bg']
    if st.session_state['font_normal2'] =='/PPTelegrafUltraBold.otf':
            plt.rcParams['font.family'] = st.session_state['font_normal2']
    elif st.session_state['font_normal2'] =='/Quicksand-Bold.ttf':
            plt.rcParams['font.family'] = st.session_state['font_normal2']
    fig = plt.figure(figsize=(16, 12))
    fig.set_facecolor(st.session_state['bg'])  # Replace '#16003B' with your desired background color
    
    title = metric1 +" vs "+metric2
    title2 = "All " + pos +"s from " + league +" - Season " + szn
    plt.suptitle(title,fontproperties=font_normal2,color='white',fontsize=24,y=0.94)
    plt.title(title2,fontproperties=font_normal2,color='white',fontsize=21,y=1)
    plt.xlabel(metric1,color='white',fontproperties=font_normal2,fontsize=12)
    plt.ylabel(metric2,color='white',fontproperties=font_normal2,fontsize=12)

    plt.grid(True, color='white', linestyle='--', linewidth=0.5)

    # Hide the top and right spines
    ax = plt.gca()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    ax.spines['left'].set_color('white')
    ax.spines['bottom'].set_color('white')

    tick_font = font_normal2

    # Set the axis tick labels to white color, adjust the font size, and rotate them by 45 degrees
    ax.tick_params(axis='x', labelcolor='white', labelsize=10)
    ax.tick_params(axis='y', labelcolor='white', labelsize=10)

    # Plot average lines

    average_goalpershot = np.mean(data[metric1])
    average_xgpershot = np.mean(data[metric2])
    plt.axvline(average_goalpershot, color='white', linestyle='--')
    plt.axhline(average_xgpershot, color='white', linestyle='--')



    data.reset_index(inplace=True,drop=True)

    for i in range(0,len(data)):
                    name = data['Name'][i]
                    x = data[metric1][i]
                    y = data[metric2][i]
                    if name==player:
                      sc = plt.scatter(x, y, s=400, c=st.session_state['h1'], marker='o', zorder=1,edgecolor=st.session_state['b'],linewidth=2,hatch='///',alpha=0.7)
                      plt.annotate(name, (x, y-0.009), fontsize=10, color='white', ha='center', va='top', fontproperties=font_normal2)
                    elif name in player2:
                        sc = plt.scatter(x, y, s=400, c=st.session_state['h3'], marker='o', zorder=1,edgecolor=st.session_state['b'],linewidth=2,hatch='///',alpha=0.7)
                        plt.annotate(name, (x, y-0.009), fontsize=10, color='white', ha='center', va='top', fontproperties=font_normal2)
                    else:
                      sc = plt.scatter(x, y, s=300, c=st.session_state['h2'], marker='o', zorder=0,alpha=0.1,edgecolor=st.session_state['h2'],linewidth=2,hatch='///')
                      if x>average_goalpershot and y>average_xgpershot:
                            plt.annotate(name, (x, y-0.009), fontsize=9, color='white', ha='center', va='top', fontproperties=st.session_state['font_normal2'],alpha=0.2)


    fdj_cropped = Image.open('smartscout.png')
    logo= Image.open('Logo.png')
    logo1 = Image.open('logo3.png')
    avid = Image.open('avid.png')
    gcfc = Image.open('gcfc.png')

    new_size1 = (100, 130)
    new_size = (170, 170)   # Adjust the size as needed
    fdj_cropped_resized = fdj_cropped.resize(new_size1)
    logo_resized = logo.resize(new_size)
    logo3_resized = logo1.resize(new_size1)
    avid_resized = avid.resize((120,35))
    gcfc_resized = gcfc.resize(new_size)

    # Add the resized images to the plot
    if st.session_state['template'] == 'SS':
            plt.figimage(fdj_cropped_resized, xo=15, yo=1960,alpha=0.5)  # Adjust the coordinates (xo, yo) as needed
    if st.session_state['template'] == 'TFA':
            plt.figimage(logo_resized, xo=2450, yo=1960)
    if st.session_state['template'] == 'Minnesota':
            plt.figimage(logo3_resized, xo=2450, yo=1960)
    if st.session_state['template'] == 'Avid':
            plt.figimage(avid_resized, xo=2450, yo=1990)
    if st.session_state['template'] == 'Game Changer FA':
            plt.figimage(gcfc_resized, xo=2450, yo=1960)
    
    st.pyplot(fig)
    
def create_team_scatter(player,data,metric1,metric2,pos,league,szn):
        font_normal2 = st.session_state['font_normal2']
        font_normal1 = st.session_state['font_normal1']
        plt.rcParams['axes.facecolor'] = st.session_state['bg']
        if st.session_state['font_normal2'] =='/PPTelegrafUltraBold.otf':
            plt.rcParams['font.family'] = st.session_state['font_normal2']
        elif st.session_state['font_normal2'] =='/Quicksand-Bold.ttf':
            plt.rcParams['font.family'] = st.session_state['font_normal2']
        fig = plt.figure(figsize=(16, 12))
        fig.set_facecolor(st.session_state['bg'])  # Replace '#16003B' with your desired background color
        
        if 'All' in pos:
            pos = 'Positions'
        
        title = metric1 +" vs "+metric2
        title2 = league +" - Season " + szn
        plt.suptitle(title,fontproperties=font_normal2,color='white',fontsize=24,y=0.94)
        plt.title(title2,fontproperties=font_normal2,color='white',fontsize=21,y=1)
        plt.xlabel(metric1,color='white',fontproperties=font_normal2,fontsize=12)
        plt.ylabel(metric2,color='white',fontproperties=font_normal2,fontsize=12)

        plt.grid(True, color='white', linestyle='--', linewidth=0.5)

        # Hide the top and right spines
        ax = plt.gca()
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        ax.spines['left'].set_color('white')
        ax.spines['bottom'].set_color('white')

        tick_font = font_normal2

        # Set the axis tick labels to white color, adjust the font size, and rotate them by 45 degrees
        ax.tick_params(axis='x', labelcolor='white', labelsize=10)
        ax.tick_params(axis='y', labelcolor='white', labelsize=10)

        # Plot average lines

        average_goalpershot = np.mean(data[metric1])
        average_xgpershot = np.mean(data[metric2])
        plt.axvline(average_goalpershot, color='white', linestyle='--')
        plt.axhline(average_xgpershot, color='white', linestyle='--')



        data.reset_index(inplace=True,drop=True)

        for i in range(0,len(data)):
                        name = data['Team'][i]
                        player_name = data['Name'][i]
                        x = data[metric1][i]
                        y = data[metric2][i]
                        if name==player:
                          sc = plt.scatter(x, y, s=400, c=st.session_state['h1'], marker='o', zorder=1,edgecolor=st.session_state['b'],linewidth=2,hatch='///',alpha=0.7)
                          plt.annotate(player_name, (x, y-0.009), fontsize=10, color='white', ha='center', va='top', fontproperties=font_normal2)
                        else:
                          sc = plt.scatter(x, y, s=300, c=st.session_state['h2'], marker='o', zorder=0,alpha=0.1,edgecolor=st.session_state['h2'],linewidth=2,hatch='///')
                          if x>average_goalpershot and y>average_xgpershot:
                            plt.annotate(name, (x, y-0.009), fontsize=9, color='white', ha='center', va='top', fontproperties=st.session_state['font_normal2'],alpha=0.2)


        fdj_cropped = Image.open('smartscout.png')
        logo= Image.open('Logo.png')
        logo1 = Image.open('logo3.png')
        avid = Image.open('avid.png')
        gcfc = Image.open('gcfc.png')

        new_size1 = (100, 130)
        new_size = (170, 170)   # Adjust the size as needed
        fdj_cropped_resized = fdj_cropped.resize(new_size1)
        logo_resized = logo.resize(new_size)
        logo3_resized = logo1.resize(new_size1)
        avid_resized = avid.resize((120,35))
        gcfc_resized = gcfc.resize(new_size)

        # Add the resized images to the plot
        if st.session_state['template'] == 'SS':
                plt.figimage(fdj_cropped_resized, xo=15, yo=1960,alpha=0.5)  # Adjust the coordinates (xo, yo) as needed
        if st.session_state['template'] == 'TFA':
                plt.figimage(logo_resized, xo=2450, yo=1960)
        if st.session_state['template'] == 'Minnesota':
                plt.figimage(logo3_resized, xo=2450, yo=1960)
        if st.session_state['template'] == 'Avid':
                plt.figimage(avid_resized, xo=2450, yo=1990)
        if st.session_state['template'] == 'Game Changer FA':
                plt.figimage(gcfc_resized, xo=2450, yo=1960)
        
        st.pyplot(fig)
    



            
def scatter(data):
    with st.expander("See definition for columns"):      
        st.table(definition)
    option = ['Player','Team','Multiple players','Other league']
    highlight = st.sidebar.selectbox("Highlight",option)
    
    if highlight=='Player':
            szn = data['Season'].unique().tolist()
            season = st.sidebar.selectbox("Choose season",szn)
            data = data[data['Season']==season]
            
            league = data['League'].unique().tolist()
            player_league = st.sidebar.selectbox("Choose League",league)
            data = data[data['League']==player_league]
            
            pos = data['Position'].unique().tolist()
            player_pos = st.sidebar.selectbox("Choose position",pos)
            data = data[data['Position']==player_pos]
            
            df = data
            
            player = data['Name'].unique().tolist()
            player_name = st.sidebar.selectbox("Choose player",player)
            
            data = data[data['Name']==player_name]
            
            m1 = data.columns[data.notna().any()].tolist()
            m2 = data.columns[data.notna().any()].tolist()
            
            names_to_remove = ['Position','Name','Team','League','Season']
            
           # if player_pos =='CF/ST':
           #     opt = ['Finishing ability']
           #     template = st.sidebar.selectbox("Choose template",opt)
            #    if opt=='Finishing ability':
             #       metric1 = 'GOALPERSHOT'
              #      metric2 = 'XGPERSHOT'
        
            m1 = [item for item in m1 if item not in names_to_remove]
            m2 = [item for item in m2 if item not in names_to_remove]
            
            metric1 = st.sidebar.selectbox("Choose metric1",m1)
            metric2 = st.sidebar.selectbox("Choose metric2",m2)



            if st.session_state['gender']=='Men':
                min_age = min(df['Age'])

                max_age = max(df['Age'])

                min_age = int(min_age)
                max_age = int(max_age)

                age = st.sidebar.slider('Select a range of age',min_age, max_age, (min_age, max_age))

            temp = data[data['Name']==player_name]


            if st.session_state['gender']=='Men':
                        df.drop(df[df['Age'] <= age[0]].index, inplace = True)
                        df.drop(df[df['Age'] >= age[1]].index, inplace = True)

            df = pd.concat([df, temp], ignore_index=True)

            df = df[['Name','Team','Season','Position','League',metric1,metric2]]
            
            but = st.sidebar.button("Create scatter")
            
            if but:
                create_scatter(player_name,df,metric1,metric2,player_pos,player_league,season)

    if highlight=='Team':
            szn = data['Season'].unique().tolist()
            season = st.sidebar.selectbox("Choose season",szn)
            data = data[data['Season']==season]
            
            league = data['League'].unique().tolist()
            player_league = st.sidebar.selectbox("Choose League",league)
            data = data[data['League']==player_league]
            
            
            t = data['Position'].unique().tolist()
            
            t.append("All")
            
            pos = st.sidebar.multiselect('Current position',t,default='All')
            
            if 'All' not in pos:
                data = data[data['Position'].isin(pos)]         
            
            df = data
            
            player = data['Team'].unique().tolist()
            player_name = st.sidebar.selectbox("Choose Team",player)
            
            
            data = data[data['Team']==player_name]
            
            m1 = data.columns[data.notna().any()].tolist()
            m2 = data.columns[data.notna().any()].tolist()
            
            names_to_remove = ['PLAYER','Position','Name','Team','League','Season','Minutes']  # Replace with the names you want to remove
        
            m1 = [item for item in m1 if item not in names_to_remove]
            m2 = [item for item in m2 if item not in names_to_remove]
            
            metric1 = st.sidebar.selectbox("Choose metric1",m1)
            metric2 = st.sidebar.selectbox("Choose metric2",m2)

            if st.session_state['gender']=='Men':
                min_age = min(df['Age'])

                max_age = max(df['Age'])

                min_age = int(min_age)
                max_age = int(max_age)

                age = st.sidebar.slider('Select a range of age',min_age, max_age, (min_age, max_age))

            temp = data[data['Team']==player_name]

            if st.session_state['gender']=='Men':
                df.drop(df[df['Age'] <= age[0]].index, inplace = True)
                df.drop(df[df['Age'] >= age[1]].index, inplace = True)

            df = pd.concat([df, temp], ignore_index=True)
            
            df = df[['Team','Name','Season','Position','League',metric1,metric2]]    
    
            but = st.sidebar.button("Create scatter")
    
            if but:
                create_team_scatter(player_name,df,metric1,metric2,pos,player_league,season)
                
    if highlight=='Multiple players':
            szn = data['Season'].unique().tolist()
            season = st.sidebar.selectbox("Choose season",szn)
            data = data[data['Season']==season]
            
            league = data['League'].unique().tolist()
            player_league = st.sidebar.selectbox("Choose League",league)
            data = data[data['League']==player_league]
            
            pos = data['Position'].unique().tolist()
            player_pos = st.sidebar.selectbox("Choose position",pos)
            data = data[data['Position']==player_pos]
            
            df = data
            
            player = data['Name'].unique().tolist()
            player_name = st.sidebar.selectbox("Choose player",player)
            
            name2 = st.sidebar.multiselect("Choose players to compare", player)

            temp1 = data[data['Name'].isin(name2)]
            
            data = data[data['Name']==player_name]
            
            m1 = data.columns[data.notna().any()].tolist()
            m2 = data.columns[data.notna().any()].tolist()
            
            names_to_remove = ['PLAYER','Position','Name','Team','League','Season']  # Replace with the names you want to remove
        
            m1 = [item for item in m1 if item not in names_to_remove]
            m2 = [item for item in m2 if item not in names_to_remove]
            
            metric1 = st.sidebar.selectbox("Choose metric1",m1)
            metric2 = st.sidebar.selectbox("Choose metric2",m2)

            if st.session_state['gender']=='Men':
                min_age = min(df['Age'])

                max_age = max(df['Age'])

                min_age = int(min_age)
                max_age = int(max_age)

                age = st.sidebar.slider('Select a range of values',min_age, max_age, (min_age, max_age))

            temp = data[data['Name']==player_name]

            if st.session_state['gender']=='Men':
                        df.drop(df[df['Age'] <= age[0]].index, inplace = True)
                        df.drop(df[df['Age'] >= age[1]].index, inplace = True)

            df = pd.concat([df, temp], ignore_index=True)
            df = pd.concat([df, temp1], ignore_index=True)
            
            df = df[['Name','Team','Season','Position','League',metric1,metric2]]
            
            but = st.sidebar.button("Create scatter")
            
            if but:
                create_player_scatter(player_name,df,metric1,metric2,player_pos,player_league,season,name2)
                
                
    if highlight=='Other league':
            szn = data['Season'].unique().tolist()
            season = st.sidebar.selectbox("Choose season",szn)
            data = data[data['Season']==season]
            
            df = data
            
            league = data['League'].unique().tolist()
            player_league = st.sidebar.selectbox("Choose League",league)
            data = data[data['League']==player_league]
            
            pos = data['Position'].unique().tolist()
            player_pos = st.sidebar.selectbox("Choose position",pos)
            data = data[data['Position']==player_pos]
            
            player = data['Name'].unique().tolist()
            player_name = st.sidebar.selectbox("Choose player",player)
            
            player_league2 = st.sidebar.selectbox("Choose comparison leage",league)
            df = df[df['League']==player_league2]
            
            pos1 = df['Position'].unique().tolist()
            player_pos1 = st.sidebar.selectbox("Choose position2",pos1)
            df = df[df['Position']==player_pos1]
            
            player2 = df['Name'].unique().tolist()
            name2 = st.sidebar.multiselect("Choose players to compare", player2)
            
            x = data[data['Name']==player_name]
            y = df[df['Name'].isin(name2)]
            
            m1 = x.columns[x.notna().any()].tolist()
            m2 = x.columns[x.notna().any()].tolist()
            
            names_to_remove = ['PLAYER','Position','Name','Team','League','Season']  # Replace with the names you want to remove
        
            m1 = [item for item in m1 if item not in names_to_remove]
            m2 = [item for item in m2 if item not in names_to_remove]
            
            metric1 = st.sidebar.selectbox("Choose metric1",m1)
            metric2 = st.sidebar.selectbox("Choose metric2",m2)

            if st.session_state['gender']=='Men':
                min_age = min(df['Age'])

                max_age = max(df['Age'])

                min_age = int(min_age)
                max_age = int(max_age)

                age = st.sidebar.slider('Select a range of values',min_age, max_age, (min_age, max_age))

            #temp = data[data['Name']==player_name]


            
            df = pd.concat([data,df])

            if st.session_state['gender']=='Men':
                df.drop(df[df['Age'] <= age[0]].index, inplace = True)
                df.drop(df[df['Age'] >= age[1]].index, inplace = True)

            df = pd.concat([df,x])
            df = pd.concat([df,y])


            df = df[['Name','Team','Season','Position','League',metric1,metric2]]
            
            but = st.sidebar.button("Create scatter")
            
            if but:
                create_league_scatter(player_name,df,metric1,metric2,player_pos,player_league,season,name2)        
    
 
def app():
    gender = st.sidebar.selectbox('Men or Women',['Men','Women'])
    st.session_state['gender'] = gender
    data = connect(gender)
    st.title("Viz generator")
    st.markdown("Choose appropriate filters from the menu bar on your left hand side.")
    cols = ['TFA','SS','BFM','Minnesota','Avid','Game Changer FA','IMAD','SISU','Virtual Scout','We Scout Strikers']
    template = st.sidebar.selectbox("Select colour template",cols)
    if template == 'TFA':
        st.session_state['template'] = 'TFA'
        st.session_state['bg'] = '#16003B'
        st.session_state['text'] = 'black'
        st.session_state['h1'] = '#f2e806'
        st.session_state['h2'] = '#f73c93'
        st.session_state['h3'] = '#00FFFF'
        st.session_state['c'] = st.session_state['h2']
        st.session_state['b'] = 'white'
        path = "PPTelegrafUltraBold.otf"
        st.session_state['font_normal2'] = FontProperties(fname=path)
        path1 = "PPTelegrafRegular.otf"
        st.session_state['font_normal1'] = FontProperties(fname=path1)

    elif template == 'SS':
        st.session_state['template'] = 'SS'
        st.session_state['bg'] = '#1C4F61'
        st.session_state['text'] = 'black'
        st.session_state['h1'] = '#26F594'
        st.session_state['h2'] = '#FFFFFF'
        st.session_state['h3'] = '#F6F558'
        st.session_state['c'] = st.session_state['h1']
        st.session_state['b'] = 'black'
        path = "Quicksand-Bold.ttf"
        st.session_state['font_normal2'] = FontProperties(fname=path)
        path1 = "Quicksand-SemiBold.ttf"
        st.session_state['font_normal1'] = FontProperties(fname=path1)

    elif template == 'BFM':
        st.session_state['template'] = 'BFM'
        st.session_state['bg'] = '#118B4A'
        st.session_state['text'] = 'black'
        st.session_state['h1'] = '#0074B3'
        st.session_state['h2'] = '#F5A623'
        st.session_state['h3'] = '#ffffff'
        st.session_state['c'] = st.session_state['h2']
        st.session_state['b'] = 'white'
        path = "PPTelegrafUltraBold.otf"
        st.session_state['font_normal2'] = FontProperties(fname=path)
        path1 = "PPTelegrafRegular.otf"
        st.session_state['font_normal1'] = FontProperties(fname=path1)
    elif template == 'Minnesota':
        st.session_state['template'] = 'Minnesota'
        st.session_state['bg'] = '#231F20'
        st.session_state['text'] = '#ffffff'
        st.session_state['h1'] = '#8CD2F4'
        st.session_state['h2'] = '#6e6e6e'
        st.session_state['h3'] = '#ffffff'
        st.session_state['c'] = st.session_state['h2']
        st.session_state['b'] = 'white'
        path = "PPTelegrafUltraBold.otf"
        st.session_state['font_normal2'] = FontProperties(fname=path)
        path1 = "PPTelegrafRegular.otf"
        st.session_state['font_normal1'] = FontProperties(fname=path1)
    elif template == 'Avid':
        st.session_state['template'] = 'Avid'
        st.session_state['bg'] = '#1b2530'
        st.session_state['text'] = '#ffffff'
        st.session_state['h1'] = '#b4945b'
        st.session_state['h2'] = '#b45b5d'
        st.session_state['h3'] = '#5ba8b4'
        st.session_state['c'] = st.session_state['h1']
        st.session_state['b'] = 'white'
        path = "PPTelegrafUltraBold.otf"
        st.session_state['font_normal2'] = FontProperties(fname=path)
        path1 = "PPTelegrafRegular.otf"
        st.session_state['font_normal1'] = FontProperties(fname=path1)
    elif template == 'Game Changer FA':
        st.session_state['template'] = 'Game Changer FA'
        st.session_state['bg'] = '#0c0c0c'
        st.session_state['text'] = '#ffffff'
        st.session_state['h1'] = '#2c248c'
        st.session_state['h2'] = '#db40e3'
        st.session_state['h3'] = '#dbe340'
        st.session_state['c'] = st.session_state['h1']
        st.session_state['b'] = 'white'
        path = "PPTelegrafUltraBold.otf"
        st.session_state['font_normal2'] = FontProperties(fname=path)
        path1 = "PPTelegrafRegular.otf"
        st.session_state['font_normal1'] = FontProperties(fname=path1)
    elif template == 'IMAD':
            st.session_state['template'] = 'IMAD'
            st.session_state['bg'] = '#14243b'
            st.session_state['text'] = '#ffffff'
            st.session_state['h1'] = '#f4d450'
            st.session_state['h2'] = '#ff5e57'
            st.session_state['h3'] = '#f73c93'
            st.session_state['c'] = st.session_state['h2']
            st.session_state['b'] = 'white'
            st.session_state['R1'] = st.session_state['h1']
            st.session_state['R2'] = st.session_state['h3']
            st.session_state['bg2'] = '#101824'
    elif template == 'SISU':
        st.session_state['template'] = 'SISU'
        st.session_state['bg'] = '#14243b'
        st.session_state['text'] = '#ffffff'
        st.session_state['h1'] = '#f4d450'
        st.session_state['h2'] = '#ff5e57'
        st.session_state['h3'] = '#ffffff'
        st.session_state['c'] = st.session_state['h2']
        st.session_state['b'] = 'white'
        st.session_state['R1'] = st.session_state['h1']
        st.session_state['R2'] = st.session_state['h3']
        st.session_state['bg2'] = '#101824'
    elif template == 'Virtual Scout':
        st.session_state['template'] = 'Virtual Scout'
        st.session_state['bg'] = '#171516'
        st.session_state['bg2'] = '#140f0f'
        st.session_state['text'] = '#ffffff'
        st.session_state['h1'] = '#f2e806'
        st.session_state['h2'] = '#f73c93'
        st.session_state['h3'] = '#FFFFFF'
        st.session_state['c'] = '#171616'
        st.session_state['b'] = 'white'
        path = "PPTelegrafUltraBold.otf"
        st.session_state['font_normal2'] = FontProperties(fname=path)
        path1 = "PPTelegrafRegular.otf"
        st.session_state['font_normal1'] = FontProperties(fname=path1)
    elif template == 'We Scout Strikers':
        st.session_state['template'] = 'We Scout Strikers'
        st.session_state['bg'] = '#040707'
        st.session_state['bg2'] = '#140f0f'
        st.session_state['text'] = '#ffffff'
        st.session_state['h1'] = '#ef5a8f'
        st.session_state['h2'] = '#fbb821'
        st.session_state['h3'] = '#ffffff'
        st.session_state['c'] = '#423e33'
        st.session_state['b'] = 'white'
        path = "PPTelegrafUltraBold.otf"
        st.session_state['font_normal2'] = FontProperties(fname=path)
        path1 = "PPTelegrafRegular.otf"
        st.session_state['font_normal1'] = FontProperties(fname=path1)

    viz = st.sidebar.selectbox('Choose visualisation',("Scatter plot","Nothing"))

    if viz=='Scatter plot':
        scatter(data)
    if st.sidebar.button('Sign out'):
        st.session_state['PageFour'] = False
        st.session_state['valid_user'] = False
        st.experimental_rerun()

 

def goto():
   app()
    
    
    

