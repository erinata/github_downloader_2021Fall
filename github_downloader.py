import json
import requests
import pandas

f = open("token", "r")
token = f.read()
f.close()

f = open("username", "r")
username = f.read()
f.close()


github_session = requests.Session()
github_session.auth = (username, token)


access_point = "https://api.github.com"

# # Check Rate Limit
rate_limit_url = access_point + "/rate_limit"
result = json.loads(github_session.get(rate_limit_url).text)
# print(result)


user_url = access_point + "/users/aarlt"
result = json.loads(github_session.get(user_url).text)
# print(result)

followers_url = result['followers_url']
result = json.loads(github_session.get(followers_url).text)


followers = [ item['login'] for item in result ]


df = pandas.DataFrame()

for follower in followers:
	user_url = access_point + "/users/" + follower
	result = json.loads(github_session.get(user_url).text)
	df = df.append({
	'follower_id' : follower,
	'repos_count' : result['public_repos'],
	'followers_count' : result['followers'],
	'following_count' : result['following'],
	'created_at' : result['created_at'],
	'updated_at' : result['updated_at']
	}, ignore_index = True)

df.to_csv("follower_dataset.csv")














