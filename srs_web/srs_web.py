from flask import Flask, url_for, request, redirect, render_template, send_file
from srs.scraper import main as scraper_main
from srs.scraper import isProductScraped
from srs.srs_local import main as srs_local_main
from srs.swnModel import swnModel
from srs import settings
import os

app = Flask(__name__)

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/scrape_reviews', methods=['GET', 'POST'])
def scrape_reviews():
	if request.method == 'POST':
		product_id = request.form["product_id"]
		print 'product_id is ' + product_id

		scrapeFlag = True
		if isProductScraped(product_id):
			print "scraped before for {0}".format(product_id)
			scrapeFlag = False
		
		srs_local_main(product_id, None, scrapeFlag)
		
		return product_id
	else:
		return render_template('home.html')

@app.route('/srs_result/<product_id>')
def showResultWithProductId(product_id): #B00HZE2PYI
	
	plot_folder = settings['sentiment_plot']
	plot_file = os.path.join(plot_folder, product_id + '_boxplot.png')
	
	return send_file(plot_file, mimetype='image/png')


if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0', port=80)