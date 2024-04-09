import openai


class ChatGPTService:
    def __init__(self, api_key):
        self.api_key = api_key

    def get_post_hashtags(self, text):
        text_request = (
            "peux-tu me donner 3 hashtags twitter pour la description de ce produit, "
            "un seul mot par hashatag pour des utilisateurs français ? "
            "Ces hashtags  doivent être les meilleurs, les plus pertinents et correspondre "
            "à des catégories très recherchées de Twitter. "
            "{text} justes les Hastags aucun autre mot dans la réponse.")
        text_request = text_request.format(text=text)

        openai.api_key = self.api_key
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": text_request}]
        )

        return completion['choices'][0]['message']['content']
