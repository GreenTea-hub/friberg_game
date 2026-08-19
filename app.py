from flask import Flask, render_template, request, redirect, url_for, session
import game

app = Flask(__name__)
app.secret_key = 'dev-secret-key'

def get_target():
    """根据 session 里存的 id，从数据库找出目标选手"""
    players = game.get_all_players()
    for p in players:
        if p['id'] == session.get('target_id'):
            return p
    return None
@app.route('/')
def index():
    if 'target_id' not in session:
        players = game.get_all_players()
        target = game.pick_target(players)
        session['target_id'] = target['id']
        session['history'] = []
        session['over'] = False
    return render_template('game.html',history=session['history'],over=session['over'],message=None)

@app.route('/guess',methods=['POST'])
def guess():
    if session.get('over'):
        return redirect(url_for('index'))
    name = request.form.get('name','').strip()
    players = game.get_all_players()
    guess_player = game.find_player_by_name(players, name)
    if guess_player is None:
        return render_template('game.html',
                               history=session['history'],over=False,message='查无此人')
    target = get_target()
    result = game.compare(guess_player, target)
    history = session['history']
    history.append({'guess': dict(guess_player), 'result': result})
    session.modified = True

    if game.is_win(guess_player, target) or len(history) >= 8:
        session['over'] = True
        session['win'] = game.is_win(guess_player, target)
    return redirect(url_for('index'))

@app.route('/restart')
def restart():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

