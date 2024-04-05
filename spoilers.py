import praw
import requests
import webbrowser

auth = requests.auth.HTTPBasicAuth('2a4XQHF_yPej48GS1zXZ-g', 'rOFpk4ciJ22IWM4J7YzjH9ad2FZlRA')

with open('pw.txt', 'r') as f:
    password = f.read()

data = {
    'grant_type': 'password',
    'username': 'Silly_Historian_350',
    'password': password
}

headers = {'User-Agent': 'MTGSpoilerAPI/0.0.1'}
res = requests.post('https://www.reddit.com/api/v1/access_token', auth=auth, data=data, headers=headers)
TOKEN = res.json()['access_token']

headers = {**headers, **{'Authorization': f'bearer {TOKEN}'}}
res = requests.get('https://oauth.reddit.com/api/v1/me', headers=headers).json()


reddit = praw.Reddit(
    client_id='2a4XQHF_yPej48GS1zXZ-g',
    client_secret='rOFpk4ciJ22IWM4J7YzjH9ad2FZlRA',
    user_agent='USER_AGENT',
)

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
    submission = reddit.submission(url=url)
    image = submission.preview['images'][0]['source']['url']
    return image

def get_title(url):
    submission = reddit.submission(url=url)
    return submission.title

def main():
    webbrowser.open(get_image('https://www.reddit.com/r/magicTCG/comments/1bvu1sw/otc_we_ride_at_dawn_most_wanted_the_command_zone/'))

if __name__ == '__main__':
    main()