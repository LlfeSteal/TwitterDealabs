class ThreadBO:
    def __init__(self, thread_id, group_display_summary, title, expired, local, price_display, price_discount_display, next_best_price_display, short_uri, temperature_rating, are_shipping_costs_free, is_nsfw, image_uri):
        self.thread_id = thread_id
        self.summary = group_display_summary
        self.title = title
        self.expired = expired
        self.is_local = local
        self.price = price_display
        self.price_discount = price_discount_display
        self.old_price = next_best_price_display
        self.uri = short_uri
        self.temperature_rating = temperature_rating
        self.is_shipping_free = are_shipping_costs_free
        self.is_nsfw = is_nsfw
        self.image_uri = image_uri

    def thread_id(self):
        return self.thread_id

    def summary(self):
        return self.summary

    def title(self):
        return self.title

    def expired(self):
        return self.expired

    def is_local(self):
        return self.is_local

    def price(self):
        return self.price

    def price_discount(self):
        return self.price_discount

    def old_price(self):
        return self.old_price

    def uri(self):
        return self.uri

    def temperature_rating(self):
        return self.temperature_rating

    def is_shipping_free(self):
        return self.is_shipping_free

    def is_nsfw(self):
        return self.is_nsfw

    def image_uri(self):
        return self.image_uri
