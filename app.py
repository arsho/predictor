from flask import Flask
from flask import Flask, render_template, request, jsonify, url_for, redirect, flash
from controller import get_initial_panels
app = Flask(__name__)


@app.route('/')
def index():
    panels = get_initial_panels()
    return render_template('index.html', panels=panels)
