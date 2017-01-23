from flask import Flask, render_template, request
from bokeh.embed import components
from bokeh.charts import Line, Bar, Scatter

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
    # check recalculation request
    if 'recalculate' in request.args:
        if request.args.get('recalculate') == 'True':
            betalyzer.recalculate()

    # build sector betas bar chart
    sector_betas = betalyzer.df_tickers.groupby('sector')['beta'].mean()
    bk_sector_betas = Bar(sector_betas,  plot_width=550, plot_height=400)
    bk_sector_betas_script, bk_sector_betas_div = components(bk_sector_betas)

    # build market cap betas bar chart
    mktcap_betas = betalyzer.df_tickers.groupby('market_cap_decile')['beta'].mean()
    bk_mc_betas = Bar(mktcap_betas, plot_width=550, plot_height=400)
    bk_mc_betas_script, bk_mc_betas_div = components(bk_mc_betas)

    # build market cap scatter plot
    scatter = Scatter(betalyzer.df_tickers, x='market_cap_log', y='beta', plot_width=550, plot_height=400)
    scatter_script, scatter_div = components(scatter)

    # build line plot for top three stocks
    top_tickers = betalyzer.df_tickers['ticker'].head(3)
    bk_history = Line(betalyzer.df_betas[top_tickers], plot_width=550, plot_height=400)
    bk_history_script, bk_history_div = components(bk_history)
    return render_template('main.html', dt_tickers=betalyzer.df_tickers.to_dict(orient='records'),
        bk_sector_betas_script=bk_sector_betas_script, bk_sector_betas_div=bk_sector_betas_div,
        bk_mc_betas_script=bk_mc_betas_script, bk_mc_betas_div=bk_mc_betas_div,
        scatter_script=scatter_script, scatter_div=scatter_div,
        bk_history_script=bk_history_script, bk_history_div=bk_history_div)

@app.route('/ticker/<ticker>')
def ticker(ticker):
    line = Line(betalyzer.df_betas[ticker], plot_width=800, plot_height=600)
    bokeh_script, bokeh_div = components(line)
    return render_template('ticker.html', ticker=ticker, bokeh_script=bokeh_script, bokeh_div=bokeh_div)

if __name__ == '__main__':
    app.run(debug=True)