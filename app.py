from flask import Flask, render_template, request, redirect, url_for
import trello_items as trello

app = Flask(__name__)
app.config.from_object('flask_config.Config')

@app.route('/')
def index():
    return render_template('index.html', items=trello.get_items())

@app.route('/add', methods=['POST'])
def add():
    name = request.form.get('new_item_name')
    description = request.form.get('new_item_description')
    trello.create_item(name, description)
    return redirect(url_for('index'))

@app.route('/mark/<item_id>', methods=['POST'])
def mark_item(item_id):
    trello.complete_item(item_id)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()
