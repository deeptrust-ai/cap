import tweepy

from config import cap_token

print("cap token:", cap_token)
client = tweepy.Client(cap_token)
print("client", client)

client.create_tweet(text="I AM ALIVE", user_auth=False)
# print(client.get_me(user_auth=False))