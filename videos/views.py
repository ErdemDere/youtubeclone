from django.shortcuts import render, get_object_or_404
from django.http import Http404

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
        'thumbnail': 'https://picsum.photos/seed/vid1/320/180',
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
        'thumbnail': 'https://picsum.photos/seed/vid2/320/180',
        'avatar': 'https://i.pravatar.cc/40?img=2',
        'video_url': 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.mp4',
        'category': 'Learning',
    },
    {
        'id': 3,
        'title': 'Best Street Food in Istanbul 🇹🇷',
        'channel': 'Food Explorer',
        'channel_verified': False,
        'views': '890K views',
        'time': '2 days ago',
        'duration': '0:15',
        'thumbnail': 'https://picsum.photos/seed/delicious/320/180',
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
        'thumbnail': 'https://picsum.photos/seed/vid4/320/180',
        'avatar': 'https://i.pravatar.cc/40?img=4',
        'video_url': 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerEscapes.mp4',
        'category': 'Gaming',
    },
    {
        'id': 5,
        'title': 'How to Build a Modern House in Minecraft',
        'channel': 'BuildCraft',
        'channel_verified': False,
        'views': '567K views',
        'time': '4 days ago',
        'duration': '0:15',
        'thumbnail': 'https://picsum.photos/seed/vid5/320/180',
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
        'thumbnail': 'https://picsum.photos/seed/vid6/320/180',
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
        'subscriptions': SUBSCRIPTIONS,
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

SUBSCRIPTIONS = [
    {'name': 'MrBeast', 'avatar': 'https://i.pravatar.cc/32?img=10', 'live': False},
    {'name': 'PewDiePie', 'avatar': 'https://i.pravatar.cc/32?img=11', 'live': True},
    {'name': 'Markiplier', 'avatar': 'https://i.pravatar.cc/32?img=12', 'live': False},
    {'name': 'CodeWithMe', 'avatar': 'https://i.pravatar.cc/32?img=13', 'live': False},
    {'name': 'TechReview', 'avatar': 'https://i.pravatar.cc/32?img=14', 'live': False},
]

def home(request):
    context = {
        'videos': VIDEOS,
        'shorts': SHORTS,
        'categories': CATEGORIES,
        'subscriptions': SUBSCRIPTIONS,
    }
    return render(request, 'videos/home.html', context)

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
    
    # Get recommended videos (all videos except current)
    recommended = [v for v in VIDEOS if v['id'] != video_id]
    
    context = {
        'video': video,
        'recommended': recommended,
        'subscriptions': SUBSCRIPTIONS,
    }
    return render(request, 'videos/watch.html', context)

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
