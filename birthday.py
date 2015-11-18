# Thanking everyone who wished me on my birthday
import requests
import json
import facebook
import simplejson

def get_posts(oauth_access_token):
	"""
		Returns dictionary of id, first names of people who posted on my wall
		between start and end time
	"""
	timestamp='1447851729 '
	limit='2'
	page_url = "https://graph.facebook.com/me/feed?access_token="+oauth_access_token+"&limit="+limit+"&since="+timestamp
	print(page_url)
	page = requests.get(page_url)
	result = page.text
	parsed_data = simplejson.loads(result)
	graph = facebook.GraphAPI(oauth_access_token)
	profile = graph.get_object("me")	
	for eachid in parsed_data['data']:
		id=eachid['id']
		from_name=eachid['from']['name']
		#print(id)
		if(from_name.split(' ')[0] != "Er"):
			print(from_name.split(' ')[0])
			graph.put_object(id, "comments", message="Thank you "+from_name.split(' ')[0]+"!")
			graph.put_object(id, "likes")
	print("Total posts received are "+str(len(parsed_data['data'])))
	return	
	
#graph.put_object("834102483289314_876433005722928", "comments", message="Reply")
#graph.put_object("834102483289314_876433005722928", "likes")
#834102483289314_876433005722928/comments?message=This+is+a+test+comment


if __name__ == '__main__':
	posts=[]
	oauth_access_token="CAACEdEose0cBAOGZChdeZCTmWFZC0vfMjZBMdDx4idn5NQ4WZAfLHR4B226zFATuVHM4XaIcRKApa9lqH1Qzo7YKie2K7mVyK2PCZCSksE2UFHnL5RIctC30h3ZB4yNZCW4AdOVZCcDSirE42TIZAksVPVvdiyWsmOxcA03cZCP7Xij8ZACftgYYgTFNWCHtexAfqoS1ZB4SUahZBjYwZDZD"
	#writeFile = open("results.txt", "w")
	#writeFile.write(get_posts(oauth_access_token))
	get_posts(oauth_access_token)
