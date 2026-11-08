from flask import Flask, render_template
from main import fig_bar, fig_scatter
from io import BytesIO
import base64

app = Flask(__name__)

def figure_to_image(figure):
    image = BytesIO()
    figure.savefig(image, format='png', bbox_inches='tight')
    image.seek(0)
    return base64.b64encode(image.read()).decode('utf-8')

@app.route('/')
def home():
    return render_template('index.html', 
                           fig_bar=figure_to_image(fig_bar), 
                           fig_scatter=figure_to_image(fig_scatter))

if __name__ == '__main__':
    app.run(debug=True)