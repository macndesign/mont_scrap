from channels.routing import route
from scrap.consumers import extract

channel_routing = [
    route('extract', extract),
]
