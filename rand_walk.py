import sys

if len(sys.argv) < 2:
    print('please specify image or video mode')
    sys.exit()

DIMS = (int(sys.argv[2]), int(sys.argv[2]))
NUM_WALKS = int(sys.argv[3])
video_allowed = sys.argv[1]=="video"

import numpy as np
from PIL import Image
import cv2
from random import choice

SPEED = 500 #walks per frame
BRIGHTNESS = 10

pos = (DIMS[0]//2,DIMS[1]//2)
#options = [(-1,-1), (-1,0), (-1, 1), (0,-1), (0,1), (1,-1), (1,0), (1,1)] #diagonal included
options = [(-1,0), (1,0), (0,-1), (0,1)]

choice_function = choice

images = []
img = Image.new("RGB", DIMS)
lo = img.load()
for i in range(NUM_WALKS):
    try:
        lo[pos] = tuple([lo[pos][0]+BRIGHTNESS]*3)
    except IndexError:
        print('random walk exited boundaries of image, please try again')
        sys.exit()
    move = choice_function(options)
    pos = pos[0]+move[0], pos[1]+move[1]
    if i%SPEED == 0 and video_allowed:
        images.append(img.copy())

if not video_allowed:
    img.save('random_walk.png')
    sys.exit()

#video
fourcc = cv2.VideoWriter_fourcc(*'avc1')
video = cv2.VideoWriter("random_walk.mp4", cv2.VideoWriter_fourcc(*'mp4v'), 60, DIMS)
for img in images:
    video.write(cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR))

video.release()
