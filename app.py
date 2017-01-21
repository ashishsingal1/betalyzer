from flask import Flask, render_template
from bokeh.embed import components
from bokeh.charts import Line

import betalyzer

app = Flask(__name__)

@app.route('/')
def main():
    line = Line(betalyzer.df_betas)
    bokeh_script, bokeh_div = components(line)
    return render_template('index.html', dt_tickers=betalyzer.df_tickers.to_dict(orient='records'),
                           bokeh_script=bokeh_script, bokeh_div=bokeh_div)

if __name__ == '__main__':
    app.run(debug=True)