import instaloader
from itertools import islice
import json

CACHE_FILE = "post_cache.json"


def load_cache():
    try:
        with open(CACHE_FILE, 'r') as f:
            return set(json.load(f))
    except FileNotFoundError:
        return set()


def save_cache(cache):
    with open(CACHE_FILE, 'w') as f:
        json.dump(list(cache), f)


def get_instagram_posts(username, session_file):
    L = instaloader.Instaloader()

    # Load saved session
    try:
        L.load_session_from_file(username, session_file)
        print("Session loaded successfully.")
    except FileNotFoundError:
        print("Session not found, login required.")
        password = input("Password: ")

        try:
            L.context.log("Enter the two-factor authentication code:")
            two_factor_code = input("Two-factor code: ")
            L.context.login(username, password)
            L.context.two_factor_login(two_factor_code)
        except instaloader.exceptions.BadCredentialsException:
            print("Invalid username or password.")
            return
        except instaloader.exceptions.TwoFactorAuthRequiredException:
            L.context.log("Enter the two-factor authentication code:")
            two_factor_code = input("Two-factor code: ")
            L.context.two_factor_login(two_factor_code)
        except instaloader.exceptions.ConnectionException as e:
            print(f"Connection error: {e}")
            return

        L.save_session_to_file(session_file)
        print("Session saved.")

    try:
        profile = instaloader.Profile.from_username(L.context, username)
    except instaloader.exceptions.ProfileNotExistsException:
        print(f"Profile {username} does not exist.")
        return
    except instaloader.exceptions.ConnectionException as e:
        print(f"Connection error: {e}")
        return

    processed_posts = load_cache()
    new_posts = []

    for post in islice(profile.get_posts(), 3):
        if post.mediaid not in processed_posts:
            comments = "\n".join(
                [comment.text for comment in post.get_comments()])
            post_data = {
                "url": post.shortcode,
                "caption": post.caption,
                "likes": post.likes,
                "comments": comments,
                "timestamp": post.date_utc
            }
            new_posts.append(post_data)
            processed_posts.add(post.mediaid)

    # save_cache(processed_posts)

    return new_posts
