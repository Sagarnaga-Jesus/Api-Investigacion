from flask import Flask, render_template, request, redirect, url_for, flash, session
from datetime import timedelta,datetime
import requests

app = Flask(__name__)
app.secret_key = '1z2x2c3v4b5n6m7,8.9-01a2s3d4fg5h6j7k8l9ñ0'
api='https://api.edamam.com/search?q='
api_key='4e3ee905fad68b6351d32297af2b44f7—'
api_id='1537e4cd'


@app.route('/')
def index():    
    return render_template('index.html')

@app.route('/buscar', methods=['POST'])
def buscar():
    alimento = request.form.get('name', '').strip().lower()
    
    if not alimento:
        flash('Por favor ingresa un nombre de Pokémon válido.', 'error')
        return redirect(url_for('base'))
    
    try:
        response = requests.get(f"{api}{alimento}&app_id={api_id}&app_key={api_key}&to=10")
        if response.status_code == 200:
            alimento_data = response.json()

            alimento_info = {
                'name': alimento_data['title'].title(),
                'id': alimento_data['id'],
                'height': alimento_data['height'] / 10,
                'weight': alimento_data['weight'] / 10,
                'imagen': alimento_data['sprites']['front_default'],
                'types': [t['type']['name'].title() for t in alimento_data['types']],
                'abilities': [a['ability']['name'].title() for a in alimento_data['abilities']],
            }
            
            return render_template('pokemon.html', alimentos=[alimento_info])
        else:
            flash(f'Pokémon "{alimento}" no encontrado.', 'error')
            return redirect(url_for('index'))
        
    except requests.exceptions.RequestException:
        flash('Error al conectar con la API de Pokémon. Inténtalo de nuevo más tarde.', 'error')
        return redirect(url_for('index')) 

if __name__ == '__main__':
    app.run(debug=True)