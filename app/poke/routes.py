from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import current_user, login_required
from werkzeug.security import check_password_hash

from .forms import pokemonform, historyform
from ..models import pokemon, User
from ..services import findpokemon


poke = Blueprint('poke', __name__, template_folder='poke_templates')


@poke.route('/search', methods=['GET', 'POST'])
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


@poke.route('/pokemon/battle')
@login_required
def battle():
    user_id = current_user.id
    pokemon_list = pokemon.query.filter_by(user_id=user_id).all()
    users = User.query.all()
    userlist = []
    for u in users:
        dic = {}
        dic["username"] = u.username
        dic["id"] = u.id
        userlist.append(dic)
    print(userlist)
    return render_template('battle.html', pokemon_list=pokemon_list, userlist=userlist)



@poke.route('/pokemon/battle/<int:user_id> <int:enemy_id>')
@login_required
def battle_user(user_id, enemy_id):
    form = historyform()
    user = current_user  # get the current user object
    user_list = pokemon.query.filter_by(user_id=user_id).all()
    user_total = 0
    enemy_list = pokemon.query.filter_by(user_id=enemy_id).all()
    enemy_total = 0
    enemy = User.query.filter_by(id=enemy_id).first()
    for poke in user_list:
        user_total += poke.atks + poke.hps + poke.defs
    for poke in enemy_list:
        enemy_total += poke.atks + poke.hps + poke.defs
    if user_total > enemy_total:
        user.winner()
        enemy.loser()
        flash(f'You won! Your total is {user_total} and enemy total is {enemy_total}')
    elif user_total < enemy_total:
        user.loser()
        enemy.winner()
        flash(f'You lost! Your total is {user_total} and enemy total is {enemy_total}')
    else:
        flash(f'You drew! Your total is {user_total} and enemy total is {enemy_total}')
    record = f'You current record is {user.win} wins and {user.loss} losses'
    flash(record)
    return redirect(url_for('poke.battle_result', user_id=user.id, enemy_id=enemy_id))

@poke.route('/pokemon/battle/result/<int:user_id> <int:enemy_id>')
@login_required
def battle_result(user_id, enemy_id):
    user = User.query.get(user_id)
    enemy = User.query.get(enemy_id)
    user_list = pokemon.query.filter_by(user_id=user_id).all()
    enemy_list = pokemon.query.filter_by(user_id=enemy_id).all()
    return render_template('result.html', user=user, user_list=user_list, enemy=enemy, enemy_list=enemy_list)


@poke.route('/pokemon/release/<int:pokemon_id>', methods=['POST'])
@login_required
def release(pokemon_id):
    poke = pokemon.query.get(pokemon_id)  # renamed to 'poke'
    poke.deletepokemon()
    flash(f'Pokemon released: {poke.name}')
    return redirect(url_for('poke.battle'))

