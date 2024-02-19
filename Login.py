# -*- coding: utf-8 -*-
"""
Created on Mon Jul 19 23:34:40 2021

@author: Sathish
"""

import streamlit as st
import Radar


#st.beta_set_page_title("Login page")
st.set_option('deprecation.showPyplotGlobalUse', False)
accounts = {
    'scout': 'scout',
    'test': 'test',
}


def is_logged_in():
    return 'valid_user' in st.session_state and st.session_state['valid_user']


def is_valid_account(username, password):
    return username in accounts.keys() and password == accounts[username]


def display_login():
    st.title("Login")
    form = st.form('form')
    username = form.text_input(label='Username', key='username')
    password = form.text_input(label='Password', type='password', key='password')
    if form.form_submit_button('Login'):
        if is_valid_account(username, password):
            st.session_state['valid_user'] = True
            st.experimental_rerun()
        else:
            form.error('Invalid credentials!')



def run():
    if not is_logged_in():
        display_login()
    else:
        Radar.goto()


run()
    








