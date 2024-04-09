import io

import requests
import tweepy

from BusinessObject.TwitterThread import TwitterThread

# Config
class TwitterService:
    def __init__(self, storage_service, chatgpt_service, api, api_secret, access, secret, client_id, client_secret):
        self.storage_service = storage_service
        self.chatgpt_service = chatgpt_service
        auth = tweepy.OAuthHandler(consumer_key=API, consumer_secret=API_SECRET, access_token=ACCESS, access_token_secret=SECRET)
        self.api = tweepy.API(auth)
        print(self.api.rate_limit_status())
        auth_v2 = tweepy.OAuth2UserHandler(
            client_id=CLIENT_ID,
            redirect_uri="https://localhost:8000",
            scope=["users.read", "tweet.write", "tweet.read", "offline.access"],
            client_secret=CLIENT_SECRET
        )

        token = self.__get_bearer_token(auth_v2)

        self.client = tweepy.Client(token, wait_on_rate_limit=True)

    def __get_bearer_token(self, auth_v2):
        refresh_token = self.storage_service.get_stored_token_value("refresh_token")
        if refresh_token is None or len(refresh_token) == 0:
            url = auth_v2.get_authorization_url()
            token_url = ""
            token_data = auth_v2.fetch_token(token_url)
        else:
            token_data = auth_v2.refresh_token('https://api.twitter.com/2/oauth2/token', refresh_token)
        token = token_data['access_token']
        refresh_token = token_data['refresh_token']
        self.storage_service.store_token("access_token", token)
        self.storage_service.store_token("refresh_token", refresh_token)
        return token

    def __create_twitter_thread_text(self, thread):
        text = "🔥" + thread.title + "\n\n💵"
        if thread.price is not None:
            text = text + thread.price
        else:
            text = text + "Gratuit"
            if thread.old_price is not None:
                text = text + " (-{old_price})".format(old_price=thread.old_price)
        if thread.price_discount is not None:
            text = text + " (-{price_discount})".format(price_discount=thread.price_discount)
        if thread.is_shipping_free:
            text = text + " - Livraison gratuite"
        text = text + "\n\n▶️" + thread.uri + "\n\n #BonPlan #bonplans #Dealabs"
        hashtags = self.chatgpt_service.get_post_hashtags(thread.title)
        text = text + "\n" + hashtags
        return text

    def __convert_to_twitter_thread(self, thread):
        text = self.__create_twitter_thread_text(thread)
        media_id = None
        if thread.image_uri is not None:
            image_file = self.__get_image_file_from_url(thread.image_uri)
            if image_file is not None:
                media_id = self.api.media_upload(filename=thread.uri, file=image_file).media_id
        return TwitterThread(text, media_id)

    def __get_image_file_from_url(self, url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            content = response.content
            file = io.BytesIO(content)
            return file
        return None

    def create_tweets(self, threads):
        for thread in threads:
            twitter_thread = self.__convert_to_twitter_thread(thread)
            media_ids = list([twitter_thread.media_id]) if twitter_thread.media_id is not None else None
            self.client.create_tweet(
                text=twitter_thread.text,
                media_ids=media_ids,
                user_auth=False)
            self.storage_service.store_thread_ids(list([thread.thread_id]))
