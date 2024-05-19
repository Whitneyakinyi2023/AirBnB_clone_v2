#!/usr/bin/python3
"""
starts a Flask web application
"""

from flask import Flask, render_template
app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_world():
    """Outputs the script: Hello HBNB!"""
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def hello_hbnb():
    """returns HBNB only wothout hello"""
    return 'HBNB'


@app.route('/c/<text>', strict_slashes=False)
def c_text(text):
    """Returns assigned C text"""
    return 'C ' + text.replace('_', ' ')


@app.route('/python', strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python_text(text='is cool'):
    """Returns python text"""
    return 'Python ' + text.replace('_', ' ')


@app.route('/number/<int:n>', strict_slashes=False)
def number_integer(n):
    return "{:d} is a number".format(n)


@app.route('/number_template/<int:n>', strict_slashes=False)
def html_is_number(n):
    """display a HTML page:n is an integer"""
    return render_template('5-number.html', n=n)


@app.route('/number_odd_or_even/<int:n>', strict_slashes=False)
def Odd_or_Even(n):
    """displays web page if number is odd or even"""
    if n % 2 == 0:
        evenness = 'even'
    else:
        evenness = 'odd'
    return render_template('6-number_odd_or_even.html', n=n, evenness=evenness)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', debug=True)
