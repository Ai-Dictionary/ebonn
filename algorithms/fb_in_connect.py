import requests
import time

FACEBOOK_ACCESS_TOKEN = "your_facebook_access_token"
LINKEDIN_ACCESS_TOKEN = "your_linkedin_access_token"
FACEBOOK_PAGE_ID = "your_facebook_page_id"
LINKEDIN_ORG_ID = "your_linkedin_organization_id"

def post_to_facebook(message):
    url = f"https://graph.facebook.com/{FACEBOOK_PAGE_ID}/feed"
    payload = {
        'message': message,
        'access_token': FACEBOOK_ACCESS_TOKEN
    }
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        print("Post successfully uploaded to Facebook!")
        return response.json().get("id")
    else:
        print(f"Failed to post on Facebook: {response.json()}")
        print(f"HTTP error! Status: {response.status_code}")
        return None

def post_to_linkedin(message):
    url = "https://api.linkedin.com/v2/ugcPosts"
    headers = {
        'Authorization': f'Bearer {LINKEDIN_ACCESS_TOKEN}',
        'X-Restli-Protocol-Version': '2.0.0',
        'Content-Type': 'application/json'
    }
    payload = {
        "author": f"urn:li:person:{LINKEDIN_ORG_ID}",
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {"text": message},
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"}
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 201:
        print("Post successfully uploaded to LinkedIn!")
        return response.json().get("id")
    else:
        print(f"Failed to post on LinkedIn: {response.json()}")
        return None

def track_facebook_post(post_id):
    url = f"https://graph.facebook.com/{post_id}/insights"
    params = {
        'access_token': FACEBOOK_ACCESS_TOKEN
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        metrics = response.json()
        print("Facebook post metrics:", metrics)
    else:
        print(f"Failed to fetch Facebook metrics: {response.json()}")

def track_linkedin_post(post_id):
    url = f"https://api.linkedin.com/v2/socialActions/{post_id}"
    headers = {
        'Authorization': f'Bearer {LINKEDIN_ACCESS_TOKEN}',
        'X-Restli-Protocol-Version': '2.0.0'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        metrics = response.json()
        print("LinkedIn post metrics:", metrics)
    else:
        print(f"Failed to fetch LinkedIn metrics: {response.json()}")

if __name__ == "__main__":
    # pass the post description here
    message = "Hello Viewers can you want to use cross platform enviroment in very low cost then contact AI DICTIONARY now."
    
    fb_post_id = post_to_facebook(message)
    
    li_post_id = post_to_linkedin(message)

    # we can store the post id for track it after some time later to disconnet the api
    
    time.sleep(60)
    
    if fb_post_id:
        track_facebook_post(fb_post_id)
    if li_post_id:
        track_linkedin_post(li_post_id)

    # discontinue with CTRL+C for terminate task

'''
1. Social media integration
2. Social media ADs run
3. Review analysis
4. Chat markating
5. Landing & Forms
6. Piplines
7. CRM
8. Automation ***
9. Tracking
10. Roles
11. Payment

!! Require but expensive
12. Database & Hosting 
'''