from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import current_user, login_required
from werkzeug.security import check_password_hash

from .forms import pokemonform
from ..models import pokemon
from ..services import findpokemon


poke = Blueprint('poke', __name__, template_folder='poke_templates')


@poke.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    form = pokemonform()
    if request.method == 'POST':
        if form.validate():
            pokemonname = form.pokemonname.data.lower()
            p_d = findpokemon(pokemonname)
            if 'keep' in request.form:
                name = p_d['Name']
                ability = p_d['Ability']
                front_shiny = p_d['Front_Shiny']
                base_atk = p_d['Base_ATK']
                base_hp = p_d['Base_HP']
                base_def = p_d['Base_DEF']
                pokemon_exists = pokemon.query.filter_by(name=name).first()
                if pokemon_exists:
                    flash('This Pokemon has already been caught!')
                else:
                    user_id = current_user.id
                    pokemon_count = pokemon.query.filter_by(user_id=user_id).count()
                    if pokemon_count < 6:
                        new = pokemon(name, ability, front_shiny, base_atk, base_hp, base_def, user_id)
                        new.savepokemon()
                        flash('Pokemon added to your collection:', p_d['Name'])
                    else:
                        flash('You have already caught 6 Pokemons. Release some to catch new ones!')
            elif 'discard' in request.form:
                # discard the found Pokemon
                flash('Pokemon released:', p_d['Name'])
            return render_template('search.html', form=form, p_d=p_d)
    return render_template('search.html', form=form)


@poke.route('/pokemon/roster')
@login_required
def roster():
    user_id = current_user.id
    pokemon_list = pokemon.query.filter_by(user_id=user_id).all()
    return render_template('roster.html', pokemon_list=pokemon_list)

@poke.route('/pokemon/release/<int:pokemon_id>', methods=['POST'])
@login_required
def release(pokemon_id):
    poke = pokemon.query.get(pokemon_id)  # renamed to 'poke'
    poke.deletepokemon()
    flash(f'Pokemon released: {poke.name}')
    return redirect(url_for('poke.roster'))


