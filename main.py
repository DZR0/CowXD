from jenkins_old_farm import JenkinsWife, JenkinsJr
import logging
from utils import *

def main():
    try:
        home_url = 'https://9gag.com/v1/feed-posts/type/home'
        progress_posts(home_url)
    except Exception as e:
        print(e)
        print('Home ended...')
        pass
    try:
        top_url = 'https://9gag.com/v1/group-posts/type/top'
        print('Top ended...')
        progress_posts(top_url)
    except Exception as e:
        print(e)
        pass
    print('Done!')
    
main()