# Config
from Config.ChatGPTConfig import ChatGptConfig
from Config.DealabsConfig import DealabsConfig
from Config.TwitterConfig import TwitterConfig

# Services
from Services.ChatGPTService import ChatGPTService
from Services.TwitterService import TwitterService
from Services.DealabsService import DealabsService
from Services.StorageService import StorageService

dealabsService = DealabsService()
storageService = StorageService()
chatgpt_service = ChatGPTService(ChatGptConfig.API_KEY)

stored_thread_ids = storageService.get_stored_thread_ids()


def filter_thread(thread):
    if thread.temperature_rating < DealabsConfig.MIN_TEMPERATURE:
        return False
    if thread.thread_id in stored_thread_ids:
        return False
    if thread.image_uri is None:
        return False
    if thread.is_nsfw:
        return False
    if thread.is_local:
        return False
    if thread.expired:
        return False
    return True


def get_threads_to_send():
    threads_to_send = []
    for page in range(1, 10):
        all_page_threads = dealabsService.get_threads(2, page, 50)
        page_selected_threads = list(filter(filter_thread, all_page_threads))
        nb_thread_to_take = DealabsConfig.MAX_THREAD_BY_HOUR - len(
            threads_to_send) if DealabsConfig.MAX_THREAD_BY_HOUR - len(
            threads_to_send) > 0 else 0
        threads_to_send.extend(page_selected_threads[:nb_thread_to_take])
        if len(threads_to_send) >= DealabsConfig.MAX_THREAD_BY_HOUR:
            break
    return threads_to_send


if __name__ == '__main__':
    threads = get_threads_to_send()
    print(len(threads))

    threads_ids = list(map(lambda obj: obj.thread_id, threads))

    index = 0
    total = len(threads)
    twitterSercice = TwitterService(
        storageService,
        chatgpt_service,
        TwitterConfig.API,
        TwitterConfig.API_SECRET,
        TwitterConfig.ACCESS,
        TwitterConfig.SECRET,
        TwitterConfig.CLIENT_ID,
        TwitterConfig.CLIENT_SECRET)

    for thread in threads:
        index = index + 1
        print("Traitement n°{index}/{total}".format(index=index, total=total))
        twitterSercice.create_tweets(list([thread]))
        # time.sleep(600)
