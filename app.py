from flask import Flask, render_template, request
import webview
from main import main, defend

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html', display='none')

@app.route('/result', methods=['POST'])
def result():
    w = int(request.form['width'])
    h = int(request.form['height'])
    shape = request.form['selected_shape']
    print(shape, h, w)
    if shape == "hexagon" and (h%2!=0 or h<4 or w<2):
        m = "For hexagonal grid the height needs to be even and at least 4 and the width at least 2! Try again."
        return render_template('index.html', display='inline-block', message=m)
    if shape == "triangle" and (h<2 or w<2):
        m = "For triangular grid the height and the width needs to be at least 2! Try again."
        return render_template('index.html', display='inline-block', message=m)
    plot_data = main(int(h), int(w), shape, (0,0))
    return render_template('result.html', h=h, w=w, shape=shape, plot_data=plot_data)

@app.route('/defend', methods=['POST'])
def attack():
    edge = request.form['edge']
    if defend(edge):
        return render_template('defend.html', edge=edge, display='none')
    else:
        m = "Invalid edge, try again!"
        return render_template('defend.html', edge=edge, display='inline-block', message=m)


#webview.create_window('Flask to exe', app)
 
if __name__ == '__main__':
    app.run(debug=True)
    #webview.start()