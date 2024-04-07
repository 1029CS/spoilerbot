import praw
import requests
import webbrowser
from dotenv import load_dotenv
import os

load_dotenv()

PASSWORD = os.getenv('REDDIT_PASSWORD')
REDDIT_TOKEN = os.getenv('REDDIT_TOKEN')   
REDDIT_SECRET = os.getenv('REDDIT_SECRET')
REDDIT_USERNAME = os.getenv('REDDIT_USERNAME')

auth = requests.auth.HTTPBasicAuth(REDDIT_TOKEN, REDDIT_SECRET)

data = {
    'grant_type': 'password',
    'username': REDDIT_USERNAME,
    'password': PASSWORD
}

headers = {'User-Agent': 'MTGSpoilerAPI/0.0.1'}
res = requests.post('https://www.reddit.com/api/v1/access_token', auth=auth, data=data, headers=headers)
TOKEN = res.json()['access_token']

headers = {**headers, **{'Authorization': f'bearer {TOKEN}'}}
res = requests.get('https://oauth.reddit.com/api/v1/me', headers=headers).json()


reddit = praw.Reddit(
    client_id=REDDIT_TOKEN,
    client_secret=REDDIT_SECRET,
    user_agent='USER_AGENT',
)

subreddit = reddit.subreddit('magicTCG')
#find posts that have the spoiler tag and contain an image, get the image url
def get_spoilers():
    spoilers = []
    for submission in subreddit.search('flair:spoiler', sort='new', time_filter='day'):
        if hasattr(submission, 'preview') == True:
            spoilers.append(submission.url)
    return spoilers

#find posts that have the spoiler tag and contain an image and return the reddit post
def get_spoilers_url():
    spoilers = []
    for submission in subreddit.search('flair:spoiler', sort='new', time_filter='day'):
        if hasattr(submission, 'preview') == True:
            spoilers.append('https://www.reddit.com' + submission.permalink)
    return spoilers


def determine_image_type(submission):
    if hasattr(submission, 'is_gallery'):
        return True
    return False

def get_gallery_images(url):
    submission = reddit.submission(url=url)
    images = []
    for item in sorted(submission.gallery_data['items'], key=lambda x: x['id']):
        media_id = item['media_id']
        meta = submission.media_metadata[media_id]
        if meta['e'] == 'Image':
            source = meta['s']
            images.append(source['u'])
            previews = meta['p']
            preview = sorted(previews, key=lambda p: -p['x'])[0]
            #images.append(preview['u'])
    
    return images

def get_image(url):
    try:
        submission = reddit.submission(url=url)
        image = submission.preview['images'][0]['source']['url']
        return image
    except Exception as e:
        print(f"Invalid URL: {url}")
        print(f"Error: {e}")

def get_title(url):
    submission = reddit.submission(url=url)
    return submission.title

# async def monitor_subreddit():
#     async for submission in subreddit.stream.submissions():
#         if submission.link_flair_text == 'Spoiler':
#             print(submission.url)

def main():
    #webbrowser.open(get_image('https://www.reddit.com/r/magicTCG/comments/1bvu1sw/otc_we_ride_at_dawn_most_wanted_the_command_zone/'))
    #detemine whether to use get_image or get_gallery_images, also check if there is a preview, if not go to the next submission, print the url of the submission
        # Call the function and store its result
    spoilers = get_spoilers_url()
    print(spoilers)

    # Check if the result is not None and print it
    # if spoilers is not None:
    #     for spoiler in spoilers:
    #         print(spoiler)
    # else:
    #     print("No spoilers found.")

    # Determine the image type for each spoiler
    # for spoiler in spoilers:
    #     submission = reddit.submission(url=spoiler)
    #     is_gallery = determine_image_type(submission)
    #     print(f"URL: {spoiler}, Is gallery: {is_gallery}")

if __name__ == '__main__':
    main()