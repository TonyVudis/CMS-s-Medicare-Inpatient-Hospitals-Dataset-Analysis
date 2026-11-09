from flask import Flask, render_template
from main import fig_bar, fig_scatter, medi_cov_correlation, medi_tot_correlation
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
                           fig_scatter=figure_to_image(fig_scatter),
                           medi_cov_correlation=medi_cov_correlation,
                           medi_tot_correlation=medi_tot_correlation,
                           discharge_insight="The region with the highest average discharges is the Midwest, while the lowest is the West.",
                           payment_insight="The region with the highest average total payment amount is the Northeast, while the lowest is the South.",
                           correlation_insight="There is a strong positive correlation between covered charges and Medicare payments, and a moderate positive correlation between Medicare payments and total payments."
                           )

if __name__ == '__main__':
    app.run(debug=True)