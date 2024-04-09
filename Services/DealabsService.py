from dealabs import Dealabs

from BusinessObject.ThreadBO import ThreadBO


def convert_thread_to_bo(thread):
    return ThreadBO(
        thread_id=thread['thread_id'],
        group_display_summary=thread['group_display_summary'] if 'group_display_summary' in thread else None,
        title=thread['title'],
        expired=thread['expired'],
        local=thread['local'],
        price_display=thread['price_display'] if 'price_display' in thread else None,
        price_discount_display=thread['price_discount_display'] if 'price_discount_display' in thread else None,
        next_best_price_display=thread['next_best_price_display'] if 'next_best_price_display' in thread else None,
        short_uri=thread['short_uri'],
        temperature_rating=thread['temperature_rating'],
        are_shipping_costs_free=thread['are_shipping_costs_free'] if 'are_shipping_costs_free' in thread else False,
        is_nsfw=thread['is_nsfw'],
        image_uri=thread['image']['large_uri'] if 'image' in thread else None,
    )


def get_params(day, page, limit):
    return {
        "days": str(day),  # can be 1, 7 or 30 days
        "page": str(page),  # page number
        "limit": str(limit),  # article per page
    }


class DealabsService:
    def __init__(self):
        self.service = Dealabs()

    def get_threads(self, day, page, limit=50):
        threads = []
        deals = self.service.get_hot_deals(get_params(day, page, limit))
        for thread in deals['data']:
            threads.append(convert_thread_to_bo(thread))
        return threads
