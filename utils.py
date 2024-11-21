import os
import logging
import time
import json
import gzip
import requests
import datetime
from urllib.parse import urlparse
import random

logging.basicConfig(
    filename='app.log', 
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)

post_prefix = 'posts'
post_like_minimum = 2000
threshold_percentage = 6


userAgents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0"
]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:132.0) Gecko/20100101 Firefox/132.0",
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
}

def count_posts(payload):
    try:
        posts = len(payload.get('posts'))
    except:
        posts = 0
        logging.log(f'No Posts found')
        pass
    return posts

def progress_posts(url):
    # This fails; returns <Response [403]>
    response = requests.get(url, headers=headers)
    # Some more code here...
    total_posts = 0
    status_code = response.status_code
    payload = response.json().get('data')
    next_cursor = payload.get('nextCursor')
    amount_of_posts = count_posts(payload)
    total_posts += amount_of_posts

    next_url = f'{url}?{next_cursor}'
    try:
        while(True):
            print(f'Total Posts: {total_posts}')
            last_next_cursor = next_cursor
            last_status_code = status_code
            last_amount_of_posts = amount_of_posts
            logging.info(f'Current NextURL: {next_url}')

            post_list = payload['posts']
            for post in post_list:
                post_id = post['id']
                creation_timestamp = post['creationTs']
                formatted_datetime = datetime.datetime.fromtimestamp(creation_timestamp, tz=datetime.timezone.utc).strftime('%Y-%m-%d')
                directory_path = create_directory(f'{post_prefix}/{formatted_datetime}')
                print("Post ID: ",post_id)
                post_upvotes = post['upVoteCount']
                print("Post Likes: ",post_upvotes)
                if post_upvotes >= post_like_minimum:
                    # comment_threshold = post_upvotes/100 * threshold_percentage
                    comment_threshold = 50
                    get_comments_from_http(post_id, comment_threshold, directory_path+'/'+post_id)


            response = requests.get(next_url, headers=headers)
            payload = response.json().get('data')
            amount_of_posts = count_posts(payload)
            total_posts += amount_of_posts
            next_cursor = payload.get('nextCursor')
            status_code = response.status_code
            next_url = f'{url}?{next_cursor}'
            
            if status_code != 200:
                logging.log(f'Failed to fetch data: {status_code}')
                break
            if count_posts(payload) == False:
                logging.log(f'Failed to fetch data: No more Posts found')
                break 
            if not next_cursor:
                logging.log(f'Failed to fetch data: No next_cursor found')
                break 
    except Exception as e:
        pass

    try:
        logging.log(f'Last Status Code: {last_status_code}')
        logging.log(f'Last next Cursor: {last_next_cursor}')
        logging.log(f'Total amount of posts: {last_amount_of_posts}')
        logging.log(f'Total posts found: {total_posts}')
    except:
        pass

    
def download_file(url, output_path):
    try:
        if os.path.exists(output_path):
            print(f"File already exists: {output_path}")
            return

        response = requests.get(url)
        
        if response.status_code == 200:
            parsed = urlparse(url)
            filename = os.path.basename(parsed.path)
            
            if os.path.isdir(output_path):
                output_path = os.path.join(output_path, filename)
            
            with open(output_path, 'wb') as f:
                f.write(response.content)
            
            print(f"File downloaded successfully: {output_path}")
        else:
            print(f"Failed to download file: {response.status_code}")
    
    except Exception as e:
        print(f"An error occurred: {e}")

def get_comments_from_http(post_id, comment_like_threshold, parent_directory):
    logging.info("get_comments_from_http()")
    request_address = f'https://comment-cdn.9gag.com/v2/cacheable/comment-list.json?appId=a_dd8f2b7d304a10edaf6f29517ea0ca4100a43d1b&count=100&type=hot&viewMode=list&postKey={post_id}&url=http://9gag.com/gag/{post_id}&origin=https://9gag.com'
    response = requests.get(url=request_address).json()
    
    max_iterations = 100
    iterations = 0
    
    for comment in response['payload']['comments']:
        comment_threshold = comment_like_threshold
        comment_like_count = comment['likeCount']
        comment_id = comment['commentId']
        
        if comment_like_count > comment_threshold:
            has_media = False
            if comment.get('media'):
                has_media = True

            if has_media:
                try:
                    gif_download_url = comment['media'][0]['imageMetaByType']['animated']['url']
                    if not gif_download_url.endswith('.mp4'):
                        gif_directory = create_directory(f'{parent_directory}/gif')
                        gif_path = f'{gif_directory}/{comment_id}.gif'
                        download_file(gif_download_url, gif_path)
                    
                    mp4_download_url = comment['media'][0]['imageMetaByType']['video']['url']
                    mp4_directory = create_directory(f'{parent_directory}/video')
                    mp4_path = f'{mp4_directory}/{comment_id}.mp4'
                    download_file(mp4_download_url, mp4_path)
                except:
                    jpg_download_url = comment['media'][0]['imageMetaByType']['image']['url']
                    jpg_directory = create_directory(f'{parent_directory}/image')
                    jpg_path = f'{jpg_directory}/{comment_id}.jpg'
                    download_file(jpg_download_url, jpg_path)

        iterations += 1
        if iterations >= max_iterations:
            break

def create_directory(file_path):
    if not os.path.exists(file_path):
        os.makedirs(file_path)
        logging.info(f"Directory '{file_path}' created successfully")
    else:
        logging.info(f"Directory '{file_path}' already exists")
    return file_path