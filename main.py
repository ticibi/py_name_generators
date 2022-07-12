import streamlit as st
from random import choice, choices

PATH = 'data/'
GENERATORS = [
    'Techy Names',
    'Fantasy Names M',
    'Fantasy Names F',
    'Town Names',
    'Orc Names',
    'Random Names',
]
session_vars = [
    'debug',
    'selection',
    'favorites',
    'names',
    'data',
]
st.session_state.debug = False
st.session_state.selection = ''
st.session_state.names = []
st.session_state.favorites = {}
st.session_state.data = {}
st.session_state.include_spaces = True


def read_names(filename) -> dict:
    data = {}
    for group in ['prefix', 'middle', 'suffix', 'adjective']:
        try:
            with open(f'{PATH}{filename}/{group}.txt') as f:
                values = f.readlines()
                data[group] = values
        except Exception as e:
            pass
    return dict(data)

def get_names(selection: str) -> dict:
    if selection in st.session_state.data:
        print('data exists')
        name_data = st.session_state.data[selection]
    elif selection not in st.session_state.data:
        print('data doesnt exist')
        name_data = read_names(selection)
        st.session_state.data[selection] = name_data
    else:
        return {}
    return name_data


class Generator:
    def __init__(self):
        self.weighted_favorites = {}
    
    def generate_name(self):
        selection = st.session_state.selection.replace(' ', '')
        name_data = get_names(selection)
        try:
            prefix = choice(name_data['prefix']).strip()
        except:
            prefix = ''
        try:
            middle = choices(name_data['middle'])[0]
        except:
            middle = ''
        try:
            suffix = choice(name_data['suffix']).strip()
        except:
            suffix = ''
        try:
            adjective = ' ' + choice(name_data['adjective'])
        except:
            adjective = ''
        return prefix.capitalize() + adjective + middle + suffix

    def increment_weight(self, name):
        value = self.weighted_favorites.get(name)
        value += 1
        self.weighted_favorites[name] = value

    def favorite(self, name):
        if name in self.weighted_favorites:
            return
        self.weighted_favorites[name] = 1

    def remove_favorite(self, name):
        if not name in self.weighted_favorites.keys():
            return
        self.weighted_favorites.pop(name)

    def is_favorited(self, name) -> bool:
        return name in self.weighted_favorites.keys()


class App:
    def __init__(self, generator: Generator, debug=False):
        self._debug = debug
        st.session_state.debug = self._debug
        self.Generator = generator
        self.names_per_column = 10
        self.column_count = 3
        self.font_size = 20
        self.style = f'''
            style="color:dodgerblue; 
                cursor:pointer; 
                font-size:{self.font_size}px;" 
            align="center"
        '''

    def debug(self):
        if not self._debug:
            return
        st.write(st.session_state)
        
    def display_names(self):
        cols = st.columns((1, 1, 1))
        for col in cols:
            for _ in range(self.names_per_column):
                name = self.Generator.generate_name()
                st.session_state.names.append(name)
                if self.Generator.is_favorited(name):
                    name = f'⭐ {name}'
                col.markdown(f'<p {self.style}>{name}</p>', unsafe_allow_html=True)

    def main_page(self):
        selection = st.selectbox('Select a Generator', options=GENERATORS)
        st.session_state.selection = selection
        cols = st.columns((2, 1, 2))
        #value = cols[0].checkbox('Include spaces?', value=st.session_state.include_spaces)
        #st.session_state.include_spaces = value
        if cols[1].button('Generate Names'):
            self.display_names()


if __name__ == '__main__':
    Gen = Generator()
    app = App(Gen, debug=False)
    app.main_page()
    app.debug()
