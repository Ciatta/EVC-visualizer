from flask import Flask, render_template, request
from main import main, defend


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('1-index.html', display='none')

@app.route('/result', methods=['POST'])
def result():
    w = int(request.form['width'])
    h = int(request.form['height'])
    shape = request.form['selected_shape']
    if w>20 or h>20:
        m = "Please avoid grid bigger than 20x20"
        return render_template('1-index.html', display='inline-block', message=m)
    if shape == "hexagon" and (h%2!=0 or h<4 or w<2):
        m = "For hexagonal grid the height needs to be even and at least 4 and the width at least 2! Try again."
        return render_template('1-index.html', display='inline-block', message=m)
    if shape == "triangle" and (h<2 or w<2):
        m = "For triangular grid the height and the width needs to be at least 2! Try again."
        return render_template('1-index.html', display='inline-block', message=m)
    main(int(h), int(w), shape, (0,0))
    if shape=="hexagon": t = "Finite Hexagonal Grid"
    elif shape=="octagon": t = "Finite Octagonal Grid"
    elif shape=="triangle": t = "Finite Triangular Grid"
    elif shape=="square": t = "Finite Squared Grid"
    return render_template('2-result.html', h=h, w=w, title=t)

@app.route('/defend', methods=['POST'])
def attack():
    edge = request.form['edge']
    if defend(edge):
       
        return render_template('3-defend.html', edge=edge, display='none')
    else:
        m = "Invalid edge, try again!"
        return render_template('3-defend.html', edge=edge, display='inline-block', message=m)


if __name__ == '__main__':
    app.run()  

