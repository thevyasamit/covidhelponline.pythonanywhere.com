
from flask import Flask,render_template,request,redirect,url_for
from urllib.request import urlopen
import tweepy, json
import urllib.request
import ssl

ssl._create_default_https_context = ssl._create_unverified_context


app =Flask(__name__)

# def twitter():
data_global = []
consumer_key = "GET_IT_FROM_TWITTER_API"
consumer_secret = "GET_IT_FROM_TWITTER_API"
access_token = "GET_IT_FROM_TWITTER_API"
access_token_secret = "GET_IT_FROM_TWITTER_API"

auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,access_token_secret)
api = tweepy.API(auth)
hashtags = ' #CovidHelp #Verified #CovidIndia'
tweet_data = tweepy.Cursor(api.search ,since = '2021-04-11',q= hashtags , lang= "en", tweet_mode = "extended", wait_on_rate_limit = True, wait_on_rate_limit_notify = True).items(200)
tweet_list= [t for t in tweet_data]
data = []
for tweet in tweet_list:
    dict={
        'username' : tweet.user.screen_name,
        'location' : tweet.user.location,
        'text' : tweet.full_text,
        'url' : "https://twitter.com/"+str(tweet.user.screen_name)+"/status/"+str(tweet.id)
    }
    
    data_global.append(dict)

@app.route('/')
def home():
	url = "https://api.apify.com/v2/key-value-stores/toDWvRj1JpTXiM8FF/records/LATEST?disableRedirect=true"
	response = urlopen(url)
	json_data = json.loads(response.read())
	json_dataa = list(json_data)
	region_data = json_data.get('regionData')
	rajasthan_data = region_data[28]
	final_data = []
	state = rajasthan_data.get('region')
	final_data.append(state)
	active = rajasthan_data.get('activeCases')
	final_data.append(active)
	recovered = rajasthan_data.get('recovered')
	final_data.append(recovered)
	deaths = rajasthan_data.get('deceased')
	final_data.append(deaths)
	totalInfected = rajasthan_data.get('totalInfected')
	final_data.append(totalInfected)
	return render_template('home.html', data= final_data)

@app.route('/pageRedirect/', methods =['POST','GET'])
def pageRedirect():
	if request.method == 'GET' or 'POST':
		name = request.form.get('external')
		# print(name,'----fjshfs------')
		if name == 'Twitter Leads':
			#return render_template('twitter.html', data = data_global)
			return render_template('twitter.html', data = data_global)
		elif name == 'Facebook Leads':
			# print(name)
			return render_template('facebook.html')
		elif name == 'Cowin Portal':
			# print(name)
			return redirect('https://www.cowin.gov.in/')
	return ('Oh no!!')

if __name__ == '__main__':
    app.run(debug=True)