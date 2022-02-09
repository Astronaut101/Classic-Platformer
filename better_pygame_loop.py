"""
Exploring better PyGame loops using the Standard Libraries available in Python 🕹☕🍜🚀

The following PyGame loop technique recipe gives a ton of functionality:
- You can manage your framerate independence in both animations and game logic by just setting some timers and letting the frames 
update at the appropriate times; stop worrying about doing math on the clock by yourself!
- Do you want to add networked multiplayer? No problem! Networking all happens inside the event loop, make whatever network requests you want, 
and never worry about blocking the game's drawing on a network request!
- Laptops now run much cooler while playing, and graphics don't have ugly tearing artifacts any more!

Using the PyGame Loop Recipe below, we will be able to see broader adoption (hopefully) of "Indie Game made in Python" and will no longer imply 
"runs hot and tears a lot when the screen is panning" 
"""


import asyncio
import time
from math import inf

from pygame.display import set_mode, flip
from pygame.constants import SCALED
from pygame.event import get

event_handler = ...
drawables = [...]

async def pygame_loop(framerate_limit=inf):
    loop = asyncio.get_event_loop()
    screen_surface = set_mode(size=(480, 255), flags=SCALED, vsync=1)
    next_frame_target = 0.0
    limit_frame_duration = (1.0 / framerate_limit)
    
    while True:
        
        if limit_frame_duration:
            # framerate limiter
            this_frame = time.time()
            delay = next_frame_target - this_frame
            if delay > 0: 
                await asyncio.sleep(delay)
            next_frame_target = this_frame + limit_frame_duration
            
        for drawable in drawables:
            drawable.draw(screen_surface)
        events_to_handle = list(get())
        events_handled = loop.create_task(handle_events(events_to_handle))
        await loop.run_in_executor(None, flip)
        # don't want to accidentally start drawing again until events are done
        await events_handled
        
async def handle_events(events_to_handle):
    # note that this must be an async def even tf it doesn't await.
    for event in events_to_handle:
        event_handler.handle_event(event)
        
asyncio.run(pygame_loop(120))