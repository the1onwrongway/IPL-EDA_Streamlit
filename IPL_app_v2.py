import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import itertools
import plotly.graph_objects as go
import seaborn as sns
custom_params = {"axes.spines.right": False, "axes.spines.top": False}


#Importing Database
data = pd.read_csv('ipl-done.csv')
match = pd.read_csv('matches_done.csv')
match =match.dropna(axis=0,subset=('winner', 'result'))
balls = pd.read_csv('balls-done.csv')
team_wickets_df = pd.read_csv('team_wickets.csv')
yoy_win = pd.read_csv('yoy_win.csv')
motm = pd.read_csv('motm.csv')
field = pd.read_csv('field.csv')
#Teamwise Matches Win
win =match[['winner']].groupby('winner')['winner'].count().sort_values(ascending=False).to_frame(name='Times')
#Teamwise Matches
win =match[['winner']].groupby('winner')['winner'].count().sort_values(ascending=False).to_frame(name='Times')
#Top 10 Cities with most matches
top_city = match[['city']].groupby('city')['city'].count().sort_values(ascending=False).head(10)
#Top 5 Batsman
top_5_batters = balls.groupby('batsman')['batsman_runs'].sum().sort_values(ascending = False).head(5)
#Top 5 MOTM
top_5_motm = match.groupby ('player_of_match')['id'].count().sort_values(ascending = False).head(5)
#Top 5 
valid_wickets = ['caught', 'bowled', 'lbw', 'stumped', 'caught and bowled']
wickets_df = data[data['dismissal_kind'].isin (valid_wickets)]
wickets_df = wickets_df.dropna(axis=0, subset=('dismissal_kind','bowling_team'))  
top_5_wicket = wickets_df.groupby('bowler')['dismissal_kind'].count().sort_values(ascending = False).head(5)
#Creating Players List
bat = sorted(data['batsman'].unique().tolist())
bat2 = sorted(data['non_striker'].unique().tolist())
bowl = sorted(data['bowler'].unique().tolist())
player = itertools.chain(bat,bat2,bowl)
players = list(player)
players = [*set(players)]
player_df = pd.read_csv('player_motm_pivot.csv')
#Overall Analysis
def load_overall_analysis():
    st.title('Overall Analysis')

    col1,col2 = st.columns(2)

    with col1:
        #Teamwise Wins
        st.subheader('Teamwise Wins')
        st.bar_chart(win)

    with col2:
            #Citywise Matches
            st.subheader('Top 10 City with Most Matches')
            fig41= go.Figure(data = [go.Pie(values=top_city.values, labels=top_city.index,textinfo='label+percent',insidetextorientation='radial', hole = .3)])
            fig41.update_layout(showlegend=False)
            st.plotly_chart(fig41,use_container_width=True,theme='streamlit') 



    col1,col2,col3 = st.columns(3)

    with col1:
        #Top 5 Batters
        st.subheader('Top 5 Batsman')
        st.bar_chart(top_5_batters)
    
    with col2:
        #Top 5 MOTM
        st.subheader('Top 5 MOTM')
        st.bar_chart(top_5_motm)

    with col3:
        #Top 5 Bowlers
        st.subheader('Top 5 Bowlers')
        st.bar_chart(top_5_wicket)

#Team Analysis
def load_team_aanalysis(selected_team):

    st.title("Team Analysis")  
    col1, col2, col3,col4 = st.columns(4)
    with col1:
            team_runs = balls[balls['batting_team'].str.contains(str(selected_team))].groupby('batting_team')['total_runs'].sum().sort_values(ascending=False).values[0]
            st.metric("Total Runs", int(team_runs))
        
    with col2:
            team_wickets= team_wickets_df[team_wickets_df['bowling_team'].str.contains(selected_team)].groupby('bowling_team')['is_wicket'].count().sort_values(ascending=False)
            st.metric('Total Wickets', int(team_wickets))
    
    with col3:
            winner = yoy_win[yoy_win['Team'].str.contains(selected_team)]['win'].values[0]
            st.metric('Title Wins', int(winner))

    with col4:
            runner_up = yoy_win[yoy_win['Team'].str.contains(selected_team)]['runner_up'].values[0]
            st.metric('Runners Up', int(runner_up))
    
    st.subheader('Key Stats')
    
    tab0 , tab1, tab2, tab3,tab4 = st.tabs(['Preffered Toss Decision','Batsman', 'Bowler','Fielder','MVP'])
    with tab0:
        win_prob = match[match['winner'].str.contains(selected_team)].groupby('toss_decision')['toss_winner'].count()
        st.subheader('Winning Chances')
        fig= go.Figure(data = [go.Pie(values=win_prob.values, labels=win_prob.index,textinfo='label+percent',insidetextorientation='radial', hole = .3)])
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig,use_container_width=True,theme='streamlit')

    with tab1:
        st.subheader('Top 10 Batsmans')
        team_batter = balls[balls['batting_team'].str.contains(selected_team)].groupby('batsman')['batsman_runs'].sum().sort_values(ascending=False).head(10)
        st.bar_chart(team_batter)

    with tab2:
        st.subheader('Top 10 Bowler')
        team_bowler = wickets_df[wickets_df['bowling_team'].str.contains(selected_team)].groupby('bowler')['is_wicket'].count().sort_values(ascending=False).head(10)
        st.bar_chart(team_bowler)

    with tab3:
        st.subheader('Top 10 Fielders')
        team_fielder = field[field['bowling_team'].str.contains(selected_team)].groupby('fielder')['id'].count().sort_values(ascending=False).head(10)
        st.bar_chart(team_fielder)

    with tab4:
        st.subheader('Top 10 MVP')
        team_motm = motm[motm['motm_team'].str.contains(selected_team)].groupby('player_of_match')['id'].count().sort_values(ascending=False).head(10)
        st.bar_chart(team_motm)

#Venue Analysis
def load_venue_analysis(selected_venue):
    
    st.title("Venue Analysis")
    col1, col2,col3 = st.columns(3)

    with col1:
        matches_here = match[match['city'].str.contains(selected_venue)].groupby('city')['id'].count().values[0]
        st.metric('Matches', int(matches_here))
    
    with col2:
        runs_here = data[data['city'].str.contains(selected_venue)].groupby('city')['total_runs'].sum()
        st.metric('Runs here',runs_here)
    
    with col3:
        wickets_here =team_wickets_df[team_wickets_df['city'].str.contains(selected_venue)].groupby('city')['is_wicket'].count()
        st.metric('Wickets here',wickets_here)


    tab1, tab2 = st.tabs(['Player','Team'])
    with tab1:
        col1 ,col2, col3 = st.columns(3)

        with col1:
            most_runs_by_player_at_venue  = data[data['city'].str.contains(selected_venue)].groupby('batsman')['batsman_runs'].sum().sort_values(ascending = False).head(5).to_frame(name='runs').reset_index()
            most_runs_by_player_at_venue = most_runs_by_player_at_venue.rename({'batsman':'Batsman', 'runs':'Runs'}, axis =1)
            st.subheader('Top 5 Scorers')
            st.write(most_runs_by_player_at_venue.to_html(index=False), unsafe_allow_html=True)
            #to_html is used to hide the index column

        with col2:
            try:
                most_wickets_by_player_at_venue= wickets_df[wickets_df['city'].str.contains(selected_venue)].groupby('bowler')['dismissal_kind'].count().sort_values(ascending = False).head(5).to_frame(name='Wickets').reset_index()      
                most_wickets_by_player_at_venue = most_wickets_by_player_at_venue.rename({'bowler':'Bowler'}, axis =1)
                st.subheader('Top 5 Wicket Takers')
                st.write(most_wickets_by_player_at_venue .to_html(index=False), unsafe_allow_html=True)
            except ValueError:
                st.error('Broke here')
        with col3:
            most_motm_at_venue = motm[motm['city'].str.contains(selected_venue)].groupby('player_of_match')['id'].count().sort_values(ascending = False).head(5).to_frame(name='MVP Awards').reset_index()
            most_motm_at_venue = most_motm_at_venue.rename({'player_of_match':'Player'}, axis =1)
            st.subheader('Top 5 MVPs')
            st.write(most_motm_at_venue .to_html(index=False), unsafe_allow_html=True)
    
    with tab2:
        col1 ,col2, col3 = st.columns(3)

        with col1:
            most_wins_by_team_at_venue =match[match['city'].str.contains(selected_venue)].groupby('winner')['id'].count().sort_values(ascending=False).to_frame(name='Wins').reset_index()
            st.subheader('Team Win %')
            fig101= go.Figure(data = [go.Pie(values=most_wins_by_team_at_venue.values, labels=most_wins_by_team_at_venue.index,textinfo='label+percent',insidetextorientation='radial', hole = .3)])
            fig101.update_layout(showlegend=False)
            st.plotly_chart(fig101,use_container_width=True,theme='streamlit')            

        with col2:
            st.subheader('Top 5 Wicket Takers')
            most_wicket_takers_at_venue= wickets_df[wickets_df['city'].str.contains(selected_venue)].groupby('bowler')['dismissal_kind'].count().sort_values(ascending = False).head(5).reset_index()
            #most_wicket_takers_at_venue = most_wicket_takers_at_venue.rename({'bowler':'Bowler'}, axis =1)
            st.bar_chart(most_wicket_takers_at_venue)

        with col3:
            most_motm_at_venue = motm[motm['city'].str.contains(selected_venue)].groupby('motm_team')['id'].count().sort_values(ascending = False).head(5).to_frame(name='MVP Awards Team').reset_index()
            st.subheader('Top 5 MVPs')
            st.bar_chart(most_motm_at_venue)

#Player Analysis
def load_player_analysis(selected_player):
    st.title('Player Analysis')
    col1, col2,col3  = st.columns(3)
    with col1:
            try:
                total_runs_player = data[data['batsman'].str.contains(selected_player)].groupby('batsman')['batsman_runs'].sum().values[0]
                st.metric('Total Runs', total_runs_player )     
            except IndexError:
                st.error("No Runs")
            
    with col2:
            try: 
                total_motm_player = motm[motm['player_of_match'].str.contains(selected_player)].groupby('player_of_match')['id'].count().values[0]
                st.metric('Total MoTM Awards', total_motm_player)
            except IndexError:
                st.error('No MoTM Awards')
    with col3:
            try:
                total_wickets_player =wickets_df[wickets_df['bowler'].str.contains(selected_player)].groupby('bowler')['is_wicket'].count().values[0]
                st.metric('Total Wickets', total_wickets_player )
            except IndexError:
                st.error('No Wickets')
        
    tab1, tab2, tab3, tab4 = st.tabs(['Batsman', 'Bowler', 'MVP','Fielder'])

    with tab1:
        try:
            runs_against_team = balls[balls['batsman'].str.contains(selected_player)].groupby('bowling_team')['batsman_runs'].sum().sort_values(ascending = False)
            st.subheader('Runs Against Teams')
            st.line_chart(runs_against_team)
        except IndexError:
            st.error('No Runs')

        try:
            total_runs_player_yoy = data[data['batsman'].str.contains(selected_player)].groupby('year')['batsman_runs'].sum()
            st.subheader('Runs Over Years')
            st.bar_chart(total_runs_player_yoy)
        except IndexError:
            st.error('No Runs')

    with tab2:
        
        col1, col2 = st.columns(2)
        with col1:
            try:
                wickets_against_team  =wickets_df[wickets_df['bowler'].str.contains(selected_player)].groupby('batting_team')['is_wicket'].count().sort_values(ascending = True)
                st.subheader("Wickets against each team")
                st.line_chart(wickets_against_team)
            except IndexError:
                st.error('No Wickets')

        with col2:
            try:
                type_of_wicket =team_wickets_df[team_wickets_df['bowler'].str.contains(selected_player)].groupby('dismissal_kind')['is_wicket'].count().sort_values(ascending = True)
                st.subheader("All Wickets in their Overs")
                fig= go.Figure(data = [go.Pie(values=type_of_wicket.values, labels=type_of_wicket.index,textinfo='label+percent',insidetextorientation='radial', hole = .3)])
                fig.update_layout(showlegend=False)
                st.plotly_chart(fig,use_container_width=True,theme='streamlit') 
            except IndexError:
                st.error('No Wickets')

    with tab3:
        col1, col2 = st.columns(2)
        with col1:
            try:
                motm_against_opposition = motm[motm['player_of_match'].str.contains(selected_player)].groupby('non_motm_team')['id'].count()
                st.subheader("MVP against Each Team")
                fig44= go.Figure(data = [go.Pie(values=motm_against_opposition.values, labels=motm_against_opposition.index,textinfo='label+percent',insidetextorientation='radial', hole = .3)])
                fig44.update_layout(showlegend=False)
                st.plotly_chart(fig44,use_container_width=True,theme='streamlit')  
            except IndexError:
                st.error('No MVP Awards')


        with col2:
            try:
                motm_per_venue = motm[motm['player_of_match'].str.contains(selected_player)].groupby('city')['id'].count()
                st.subheader("MVP at Different Venues")
                fig45= go.Figure(data = [go.Pie(values=motm_per_venue.values, labels=motm_per_venue.index,textinfo='label+percent',insidetextorientation='radial', hole = .3)])
                fig45.update_layout(showlegend=False)
                st.plotly_chart(fig45,use_container_width=True,theme='streamlit')
            except IndexError:
                st.error('No MVP Awards')    
    with tab4:
        try:
            team_fielder = field[field['fielder'].str.contains(selected_player)]
            team_fielder = pd.crosstab([team_fielder['batting_team'],team_fielder['dismissal_kind']], team_fielder['id'].agg('count')).reset_index()

            team_fielder.columns.values[2]='Successful Attempts'
            team_fielder.columns.values[0]='Opposition Team'
            team_fielder.columns.values[1]='Field Impact'
            st.subheader('Fielding Impact')
            fig3,ax = plt.subplots(figsize = (8.27, 3) )
            sns.barplot(data =team_fielder, x=team_fielder['Opposition Team'],y=team_fielder['Successful Attempts'],
            hue=team_fielder['Field Impact'] ,ax =ax)
            st.pyplot(fig3)
            
        except IndexError:
            st.error('No contributions to mention')
        


st.set_page_config(layout='wide', page_title='IPL Analysis')

st.sidebar.title("IPL Analysis")
st.sidebar.subheader('Prepared by [Milan Gabriel](https://bit.ly/the1onwrongway)')
opt = st.sidebar.selectbox('Select One',['--select any--','Overall Analysis','Team Analysis','Venue Analysis','Player Analysis'])

if opt == 'Overall Analysis':
    load_overall_analysis()


elif opt == 'Team Analysis':
    selected_team = st.sidebar.selectbox('Select Team',sorted(data['batting_team'].unique().tolist()))
    btn = st.sidebar.button('Find Team Details')
    
    if btn:
        load_team_aanalysis(selected_team)
 

elif opt == 'Venue Analysis':
    selected_venue = st.sidebar.selectbox('Select Venue',sorted(match['city'].unique().tolist()))
    btn1 = st.sidebar.button('Find Venue Details')
    
    if btn1:
        load_venue_analysis(selected_venue)

elif opt == '--select any--':
    st.title('IPL Analysis')
    st.subheader('Prepared by [Milan Gabriel](https://bit.ly/the1onwrongway)')
    st.write("[Email](mailto:the1onwrongway@gmail.com)","[Linkedin](https://www.linkedin.com/in/milan-gabriel/)" ,"[GitHub](https://github.com/the1onwrongway)")
    #st.write("check out this [link](https://share.streamlit.io/mesmith027/streamlit_webapps/main/MC_pi/streamlit_app.py)")




else:
    selected_player = st.sidebar.selectbox('Select Player',sorted(players))
    btn = st.sidebar.button('Find Player Details')
    if btn:
        load_player_analysis(selected_player)