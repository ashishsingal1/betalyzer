from flask import Flask, render_template, request, url_for, redirect

app = Flask(__name__)

@app.route('/')
def main():
	return render_template('index.html')

if __name__ == '__main__':
	app.run(debug=True)