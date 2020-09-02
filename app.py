from flask import Flask, render_template, request, redirect, url_for
import trello_items as trello
from viewmodel import ViewModel

app = Flask(__name__)
app.config.from_object('flask_config.Config')

@app.route('/')
def index():
    items = trello.get_items()
    item_view_model = ViewModel(items[0], items[1], items[2])
    return render_template('index.html', view_model=item_view_model)

@app.route('/add', methods=['POST'])
def add():
    name = request.form.get('new_item_name')
    description = request.form.get('new_item_description')
    trello.create_item(name, description)
    return redirect(url_for('index'))

@app.route('/start/<item_id>', methods=['POST'])
def start_item(item_id):
    trello.start_item(item_id)
    return redirect(url_for('index'))

@app.route('/complete/<item_id>', methods=['POST'])
def complete_item(item_id):
    trello.complete_item(item_id)
    return redirect(url_for('index'))

@app.route('/undo/<item_id>', methods=['POST'])
def undo_item(item_id):
    trello.undo_item(item_id)
    return redirect(url_for('index'))

@app.route('/stop/<item_id>', methods=['POST'])
def stop_item(item_id):
    trello.stop_item(item_id)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()
