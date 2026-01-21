from django.shortcuts import render, get_object_or_404
from django.http import Http404, JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json

# Static video data (no database)
VIDEOS = [
    {
        'id': 1,
        'title': 'Amazing Nature Documentary - 4K',
        'channel': 'Nature World',
        'channel_verified': True,
        'views': '2.5M views',
        'time': '3 days ago',
        'duration': '9:56',
        'thumbnail': '/static/images/thumbnails/nature_doc.png',
        'avatar': 'https://i.pravatar.cc/40?img=1',
        'video_url': 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4',
        'category': 'Nature',
    },
    {
        'id': 2,
        'title': 'Learn Python in 1 Hour - Full Course for Beginners',
        'channel': 'Code Master',
        'channel_verified': True,
        'views': '1.8M views',
        'time': '1 week ago',
        'duration': '10:53',
        'thumbnail': '/static/images/thumbnails/python_course.png',
        'avatar': 'https://i.pravatar.cc/40?img=2',
        'video_url': 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.mp4',
        'category': 'Learning',
        'channel': 'CodeWithMe',
    },
    {
        'id': 3,
        'title': 'Best Street Food in Istanbul 🇹🇷',
        'channel': 'Food Explorer',
        'channel_verified': False,
        'views': '890K views',
        'time': '2 days ago',
        'duration': '0:15',
        'thumbnail': '/static/images/thumbnails/istanbul_food.png',
        'avatar': 'https://i.pravatar.cc/40?img=3',
        'video_url': 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4',
        'category': 'Cooking',
    },
    {
        'id': 4,
        'title': 'Epic Gaming Moments Compilation #47',
        'channel': 'GameZone',
        'channel_verified': True,
        'views': '3.2M views',
        'time': '5 hours ago',
        'duration': '0:15',
        'thumbnail': '/static/images/thumbnails/gaming_moments.png',
        'avatar': 'https://i.pravatar.cc/40?img=4',
        'video_url': 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerEscapes.mp4',
        'category': 'Gaming',
        'channel': 'MrBeast',
    },
    {
        'id': 5,
        'title': 'How to Build a Modern House in Minecraft',
        'channel': 'BuildCraft',
        'channel_verified': False,
        'views': '567K views',
        'time': '4 days ago',
        'duration': '0:15',
        'thumbnail': '/static/images/thumbnails/minecraft_house.png',
        'avatar': 'https://i.pravatar.cc/40?img=5',
        'video_url': 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerFun.mp4',
        'category': 'Gaming',
    },
    {
        'id': 6,
        'title': '10 Life Hacks That Will Change Your Life',
        'channel': 'Life Tips',
        'channel_verified': True,
        'views': '4.1M views',
        'time': '1 month ago',
        'duration': '0:15',
        'thumbnail': '/static/images/thumbnails/life_hacks.png',
        'avatar': 'https://i.pravatar.cc/40?img=6',
        'video_url': 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerJoyrides.mp4',
        'category': 'Learning',
    },
    {
        'id': 7,
        'title': 'Relaxing Piano Music for Studying',
        'channel': 'Calm Vibes',
        'channel_verified': False,
        'views': '12M views',
        'time': '2 months ago',
        'duration': '14:48',
        'thumbnail': 'https://picsum.photos/seed/vid7/320/180',
        'avatar': 'https://i.pravatar.cc/40?img=7',
        'video_url': 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/Sintel.mp4',
        'category': 'Music',
    },
    {
        'id': 8,
        'title': 'Advanced CSS Animations Tutorial',
        'channel': 'Web Dev Pro',
        'channel_verified': True,
        'views': '234K views',
        'time': '6 days ago',
        'duration': '12:14',
        'thumbnail': 'https://picsum.photos/seed/vid8/320/180',
        'avatar': 'https://i.pravatar.cc/40?img=8',
        'video_url': 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/TearsOfSteel.mp4',
        'category': 'Learning',
        'channel': 'TechReview',
    },
    {
        'id': 9,
        'title': 'Street Rap Battle - Underground Kings 🎤',
        'channel': 'Urban Flow',
        'channel_verified': True,
        'views': '2.8M views',
        'time': '3 days ago',
        'duration': '0:15',
        'thumbnail': 'https://picsum.photos/seed/vid9/320/180',
        'avatar': 'https://i.pravatar.cc/40?img=9',
        'video_url': 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4',
        'category': 'Music',
    },
    {
        'id': 10,
        'title': 'Summer Hits 2024 Mix ☀️',
        'channel': 'Music Station',
        'channel_verified': True,
        'views': '5.6M views',
        'time': '1 week ago',
        'duration': '0:15',
        'thumbnail': 'https://picsum.photos/seed/vid10/320/180',
        'avatar': 'https://i.pravatar.cc/40?img=12',
        'video_url': 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerFun.mp4',
        'category': 'Music',
        'channel': 'PewDiePie',
    },
    {
        'id': 11,
        'title': 'Live Rock Concert - Full Show',
        'channel': 'Rock Legends',
        'channel_verified': True,
        'views': '890K views',
        'time': '2 weeks ago',
        'duration': '0:15',
        'thumbnail': 'https://picsum.photos/seed/vid11/320/180',
        'avatar': 'https://i.pravatar.cc/40?img=13',
        'video_url': 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerMeltdowns.mp4',
        'category': 'Music',
    },
]

# ... (omitted code) ...

def explore(request, category):
    """View to display videos filtered by category."""
    filtered_videos = [v for v in VIDEOS if v.get('category') == category]
    
    context = {
        'videos': filtered_videos,
        'shorts': SHORTS[:6], # Show some shorts
        'categories': CATEGORIES,
        'subscriptions': get_current_subscriptions(request),
        'active_category': category,
    }
    return render(request, 'videos/home.html', context)


SHORTS = [
    {
        'id': 1,
        'title': 'Wait for it... 😂',
        'views': '15M views',
        'thumbnail': 'https://picsum.photos/seed/short1/180/320',
        'video_url': 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4',
        'channel': 'FunnyClips',
        'likes': '1.2M',
    },
    {
        'id': 2,
        'title': 'This cat is unbelievable!',
        'views': '8.2M views',
        'thumbnail': 'https://picsum.photos/seed/short2/180/320',
        'video_url': 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerEscapes.mp4',
        'channel': 'CatLovers',
        'likes': '890K',
    },
    {
        'id': 3,
        'title': 'Quick cooking tip 🍳',
        'views': '5.4M views',
        'thumbnail': 'https://picsum.photos/seed/short3/180/320',
        'video_url': 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerFun.mp4',
        'channel': 'ChefTips',
        'likes': '456K',
    },
    {
        'id': 4,
        'title': 'Mind-blowing magic trick!',
        'views': '22M views',
        'thumbnail': 'https://picsum.photos/seed/short4/180/320',
        'video_url': 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerJoyrides.mp4',
        'channel': 'MagicMaster',
        'likes': '2.1M',
    },
    {
        'id': 5,
        'title': 'Dance challenge accepted 💃',
        'views': '9.1M views',
        'thumbnail': 'https://picsum.photos/seed/short5/180/320',
        'video_url': 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerMeltdowns.mp4',
        'channel': 'DanceVibes',
        'likes': '1.5M',
    },
    {
        'id': 6,
        'title': 'POV: Monday morning',
        'views': '3.8M views',
        'thumbnail': 'https://picsum.photos/seed/short6/180/320',
        'video_url': 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/SubaruOutbackOnStreetAndDirt.mp4',
        'channel': 'DailyVibes',
        'likes': '345K',
    },
    {
        'id': 7,
        'title': 'Most satisfying cleaning video 🧹',
        'views': '12M views',
        'thumbnail': 'https://picsum.photos/seed/short7/180/320',
        'video_url': 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/TearsOfSteel.mp4',
        'channel': 'CleanFreak',
        'likes': '2.5M',
    },
    {
        'id': 8,
        'title': 'Coding in current year be like...',
        'views': '450K views',
        'thumbnail': 'https://picsum.photos/seed/short8/180/320',
        'video_url': 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/Sintel.mp4',
        'channel': 'DevHumor',
        'likes': '89K',
    },
    {
        'id': 9,
        'title': 'Secret travel spot revealed 🌏',
        'views': '1.1M views',
        'thumbnail': 'https://picsum.photos/seed/short9/180/320',
        'video_url': 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4',
        'channel': 'TravelGoals',
        'likes': '120K',
    },
    {
        'id': 10,
        'title': 'My dog trying to speak',
        'views': '18M views',
        'thumbnail': 'https://picsum.photos/seed/short10/180/320',
        'video_url': 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.mp4',
        'channel': 'DogParents',
        'likes': '3.1M',
    },
]

CATEGORIES = [
    'All', 'Gaming', 'Music', 'Live', 'Cooking', 'Nature', 
    'Sports', 'News', 'Learning', 'Fashion', 'Comedy', 'Tech'
]

PLAYLISTS = [
    {
        'id': 'liked',
        'title': 'Liked videos',
        'video_count': 0, # Will be dynamic
        'thumbnail': '/static/images/thumbnails/nature_doc.png',
        'is_private': True,
        'description': 'Videos you have liked',
    },
    {
        'id': 'python',
        'title': 'Python Learning Path',
        'video_count': 3,
        'thumbnail': '/static/images/thumbnails/python_course.png',
        'is_private': False,
        'description': 'Master Python from zero to hero with these hand-picked tutorials.',
        'video_ids': [2, 8, 6] 
    },
    {
        'id': 'gaming',
        'title': 'Epic Gaming Moments',
        'video_count': 2,
        'thumbnail': '/static/images/thumbnails/gaming_moments.png',
        'is_private': False,
        'description': 'The absolute best gaming clips from across the platform.',
        'video_ids': [4, 5]
    },
    {
        'id': 'nature',
        'title': 'Nature & Relaxation',
        'video_count': 2,
        'thumbnail': 'https://picsum.photos/seed/vid7/320/180',
        'is_private': False,
        'description': 'Calm your mind with beautiful nature footage and soothing sounds.',
        'video_ids': [1, 7]
    }
]

SUBSCRIPTIONS = [
    {'name': 'MrBeast', 'avatar': 'https://i.pravatar.cc/32?img=10', 'live': False},
    {'name': 'PewDiePie', 'avatar': 'https://i.pravatar.cc/32?img=11', 'live': True},
    {'name': 'Markiplier', 'avatar': 'https://i.pravatar.cc/32?img=12', 'live': False},
    {'name': 'CodeWithMe', 'avatar': 'https://i.pravatar.cc/32?img=13', 'live': False},
    {'name': 'TechReview', 'avatar': 'https://i.pravatar.cc/32?img=14', 'live': False},
]

def get_current_subscriptions(request):
    """Helper to get merged list of default and session-based subscriptions."""
    session_subs = request.session.get('my_subscriptions', [])
    # Convert list of dicts to list of names for default check
    default_names = [s['name'] for s in SUBSCRIPTIONS]
    
    # Merge default and session ones (avoid duplicates)
    merged = list(SUBSCRIPTIONS)
    for sub in session_subs:
        if sub['name'] not in default_names:
            merged.append(sub)
    return merged

def home(request):
    context = {
        'videos': VIDEOS,
        'shorts': SHORTS,
        'categories': CATEGORIES,
        'subscriptions': get_current_subscriptions(request),
    }
    return render(request, 'videos/home.html', context)

def subscriptions(request):
    """View to display user subscriptions."""
    all_subs = get_current_subscriptions(request)
    subscribed_channels = [sub['name'] for sub in all_subs]
    subscribed_videos = [v for v in VIDEOS if v['channel'] in subscribed_channels]
    
    context = {
        'subscriptions': all_subs,
        'videos': subscribed_videos,
    }
    return render(request, 'videos/subscriptions.html', context)


def get_video_by_id(video_id):
    """Helper function to get video by ID from static data."""
    for video in VIDEOS:
        if video['id'] == video_id:
            return video
    return None



def watch(request, video_id):
    """View for watching a single video."""
    video = get_video_by_id(video_id)
    if video is None:
        raise Http404("Video not found")
    
    # Record watched video in session history
    history = request.session.get('history', [])
    if video_id not in history:
        history.append(video_id)
        request.session['history'] = history

    # Get recommended videos (all videos except current)
    recommended = [v for v in VIDEOS if v['id'] != video_id]
    
    context = {
        'video': video,
        'recommended': recommended,
        'subscriptions': get_current_subscriptions(request),
    }
    return render(request, 'videos/watch.html', context)


def history(request):
    """View to display watched video history."""
    history_ids = request.session.get('history', [])
    watched_videos = [v for v in VIDEOS if v['id'] in history_ids]
    context = {
        'videos': watched_videos,
        'subscriptions': get_current_subscriptions(request),
    }
    return render(request, 'videos/history.html', context)

def get_short_by_id(short_id):
    """Helper function to get short by ID from static data."""
    for short in SHORTS:
        if short['id'] == short_id:
            return short
    return None

def shorts(request, short_id):
    """View for watching a YouTube Short."""
    short = get_short_by_id(short_id)
    if short is None:
        raise Http404("Short not found")
    
    # Sort shorts by ID to ensure correct order
    all_shorts_sorted = sorted(SHORTS, key=lambda x: x['id'])
    
    context = {
        'current_short': short,
        'all_shorts': all_shorts_sorted,
    }
    return render(request, 'videos/shorts.html', context)


def liked_videos(request):
    """View to display liked videos."""
    liked_ids = request.session.get('liked_videos', [])
    # Preserve order of liking by iterating over liked_ids
    liked_list = []
    for vid_id in reversed(liked_ids):
        video = get_video_by_id(vid_id)
        if video:
            liked_list.append(video)
            
    context = {
        'videos': liked_list,
        'subscriptions': get_current_subscriptions(request),
    }
    return render(request, 'videos/liked_videos.html', context)


@csrf_exempt
@require_POST
def toggle_like(request):
    """AJAX view to toggle like state for a video."""
    try:
        data = json.loads(request.body)
        video_id = int(data.get('video_id'))
    except (ValueError, TypeError, json.JSONDecodeError):
        return JsonResponse({'status': 'error', 'message': 'Invalid data'}, status=400)

    liked_videos = request.session.get('liked_videos', [])
    
    if video_id in liked_videos:
        liked_videos.remove(video_id)
        action = 'unliked'
    else:
        liked_videos.append(video_id)
        action = 'liked'
        
    request.session['liked_videos'] = liked_videos
    request.session.modified = True
    
    return JsonResponse({'status': 'success', 'action': action})


@csrf_exempt
@require_POST
def toggle_subscription(request):
    """AJAX view to toggle channel subscription status."""
    try:
        data = json.loads(request.body)
        name = data.get('name')
        avatar = data.get('avatar')
    except (ValueError, TypeError, json.JSONDecodeError):
        return JsonResponse({'status': 'error', 'message': 'Invalid data'}, status=400)

    my_subs = request.session.get('my_subscriptions', [])
    
    # Check if already in session subs
    found_idx = -1
    for i, sub in enumerate(my_subs):
        if sub['name'] == name:
            found_idx = i
            break
            
    if found_idx != -1:
        my_subs.pop(found_idx)
        action = 'unsubscribed'
    else:
        my_subs.append({'name': name, 'avatar': avatar, 'live': False})
        action = 'subscribed'
        
    request.session['my_subscriptions'] = my_subs
    request.session.modified = True
    
    return JsonResponse({'status': 'success', 'action': action})

def playlists(request):
    """Gallery view of all playlists."""
    # Dynamic count for Liked videos
    liked_ids = request.session.get('liked_videos', [])
    
    updated_playlists = []
    for pl in PLAYLISTS:
        p_copy = dict(pl)
        if pl['id'] == 'liked':
            p_copy['video_count'] = len(liked_ids)
            # Update thumbnail if there are liked videos
            if liked_ids:
                last_liked = get_video_by_id(liked_ids[-1])
                if last_liked:
                    p_copy['thumbnail'] = last_liked['thumbnail']
        updated_playlists.append(p_copy)

    context = {
        'playlists': updated_playlists,
        'subscriptions': get_current_subscriptions(request),
    }
    return render(request, 'videos/playlists.html', context)

def playlist_detail(request, playlist_id):
    """Detailed view of a single playlist."""
    playlist = next((p for p in PLAYLISTS if p['id'] == playlist_id), None)
    if not playlist:
        raise Http404("Playlist not found")
    
    video_list = []
    
    if playlist['id'] == 'liked':
        liked_ids = request.session.get('liked_videos', [])
        for vid_id in reversed(liked_ids):
            video = get_video_by_id(vid_id)
            if video:
                video_list.append(video)
    else:
        for vid_id in playlist.get('video_ids', []):
            video = get_video_by_id(vid_id)
            if video:
                video_list.append(video)
                
    context = {
        'playlist': playlist,
        'videos': video_list,
        'subscriptions': get_current_subscriptions(request),
    }
    return render(request, 'videos/playlist_detail.html', context)


@csrf_exempt
@require_POST
def toggle_watch_later(request):
    """AJAX view to toggle watch later state for a video."""
    try:
        data = json.loads(request.body)
        video_id = int(data.get('video_id'))
    except (ValueError, TypeError, json.JSONDecodeError):
        return JsonResponse({'status': 'error', 'message': 'Invalid data'}, status=400)

    watch_later = request.session.get('watch_later', [])
    
    if video_id in watch_later:
        watch_later.remove(video_id)
        action = 'removed'
    else:
        watch_later.append(video_id)
        action = 'saved'
        
    request.session['watch_later'] = watch_later
    request.session.modified = True
    
    return JsonResponse({'status': 'success', 'action': action})


def watch_later(request):
    """View to display saved watch later videos."""
    watch_later_ids = request.session.get('watch_later', [])
    saved_list = []
    # Preserve order (most recent first)
    for vid_id in reversed(watch_later_ids):
        video = get_video_by_id(vid_id)
        if video:
            saved_list.append(video)
            
    context = {
        'videos': saved_list,
        'subscriptions': get_current_subscriptions(request),
    }
    return render(request, 'videos/watch_later.html', context)


def profile(request):
    """View to display user profile/channel page."""
    # Get user's content from session
    liked_ids = request.session.get('liked_videos', [])
    watch_later_ids = request.session.get('watch_later', [])
    history_ids = request.session.get('history', [])
    
    # Get videos for each category
    liked_videos = [get_video_by_id(vid_id) for vid_id in liked_ids if get_video_by_id(vid_id)]
    watch_later_videos = [get_video_by_id(vid_id) for vid_id in watch_later_ids if get_video_by_id(vid_id)]
    history_videos = [get_video_by_id(vid_id) for vid_id in history_ids if get_video_by_id(vid_id)]
    
    # Mock channel data (in a real app, this would come from User model)
    channel_data = {
        'name': 'My Channel',
        'handle': '@mychannel',
        'subscribers': '125K',
        'total_videos': len(VIDEOS),  # Mock: all available videos
        'total_views': '2.5M',
        'joined_date': 'Jan 15, 2024',
        'description': 'Welcome to my channel! I create content about gaming, music, and learning. Subscribe to stay updated with my latest videos!',
        'banner': 'https://picsum.photos/seed/banner/1600/400',
        'avatar': '/static/images/my_avatar.jpg',
    }
    
    # Statistics
    stats = {
        'videos_watched': len(history_ids),
        'videos_liked': len(liked_ids),
        'playlists_created': len([p for p in PLAYLISTS if p['id'] != 'liked']),
        'subscriptions_count': len(get_current_subscriptions(request)),
    }
    
    # Get user's playlists
    user_playlists = []
    for pl in PLAYLISTS:
        p_copy = dict(pl)
        if pl['id'] == 'liked':
            p_copy['video_count'] = len(liked_ids)
            if liked_ids:
                last_liked = get_video_by_id(liked_ids[-1])
                if last_liked:
                    p_copy['thumbnail'] = last_liked['thumbnail']
        user_playlists.append(p_copy)
    
    context = {
        'channel': channel_data,
        'stats': stats,
        'videos': VIDEOS[:6],  # Featured videos (first 6)
        'all_videos': VIDEOS,  # All videos for videos tab
        'liked_videos': liked_videos,
        'playlists': user_playlists,
        'subscriptions': get_current_subscriptions(request),
    }
    return render(request, 'videos/profile.html', context)
