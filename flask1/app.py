from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def get_data():
    df = pd.read_csv('./output.csv')
    data = df.to_dict(orient='records')
    return render_template('data.html',data=data)

if __name__ == '__main__':
    app.run(debug=True)