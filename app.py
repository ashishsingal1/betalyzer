from flask import Flask, render_template
from bokeh.embed import components
from bokeh.charts import Line

import betalyzer

app = Flask(__name__)

def fmt(val, dec=2):
    """Allows us to format numbers by adding thousands and rounding without getting errors on NaN values"""
    try: result = ("{:,."+str(dec)+"f}").format(val)
    except: result = val
    return result

app.jinja_env.globals.update(fmt=fmt)

@app.route('/')
def main():
    # line = Line(betalyzer.df_betas)
    # bokeh_script, bokeh_div = components(line)
    # bokeh_script=bokeh_script, bokeh_div=bokeh_div
    return render_template('index.html', dt_tickers=betalyzer.df_tickers.to_dict(orient='records'),
                          )

if __name__ == '__main__':
    app.run(debug=True)