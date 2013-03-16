'''
Created on 15 Mar 2013

@author: pap-x
'''

import Image, math, sys, operator

color_names = { 1: 'black', 2: 'white', 3: 'violet', 4: 'blue', 5: 'red', 6: 'green', 7: 'magenta', 8: 'cyan', 9: 'yellow', 10: 'orange', 11: 'lime', 12: 'purple', 	
             13: 'dark red', 14: 'dark green', 15: 'dark blue', 16: 'pink', 17: 'skin tone', 18: 'aquamarine', 19: 'sky blue', 20: 'brown', 21: 'dark green', 22: 'olive',
             23: 'nature green', 24: 'khaki', 25: 'dark yellow'}				#The main colors recognizable. More can be added
color_rgb = {1: (0,0,0), 2: (255,255,255), 3: (255,62,150), 4: (0,0,255), 5: (255,0,0), 6: (0,255,0), 
             7: (255, 0, 255), 8: (0,255,255), 9: (255,255,0), 10: (255,128,0), 11: (128,255,0), 12: (128,0,255), 
             13: (128,0,0), 14: (0,128,0), 15: (0,0,128), 16: (255,192,203), 17: (245,204,176), 18: (127,255,212), 19: (50,153,204), 20:(139,69,19), 21: (47,79,47), 
             22: (128,128,0), 23: (34,139,34), 24: (240,230,140), 25: (255,215,0)}		#RGB index of every color

def imResize(img, width, height):					#Resizes a large photo for faster processing
														
    if width > height :
        new_width = 500
        new_height = int((height/float(width)) * 500)
    else :
        new_height = 500
        new_width = int((width/float(height)) * 500)
    
    img = img.resize((new_width, new_height), Image.ANTIALIAS)
    return img

def calcDist3D(point1, point2):						#Calculates the distance between 2 points in a 3d space
    return float(math.sqrt((point1[0]-point2[0])**2+(point1[1]-point2[1])**2+(point1[2]-point2[2])**2))

try:
    im = Image.open('test.jpg')
except:
    print "Error opening image. Please try again"
    sys.exit()
    

width, height = im.size

if width > 500 or height > 500:
    print "Image too large. Resizing to 500px big side."
    im = imResize(im, width, height)

width, height = im.size
image_rgb = im.load()

color_dist = [[[0]*len(color_rgb) for _ in xrange(height)] for _ in xrange(width)]		#Creates a 3d list for the colors of every pixel



for i in range(width):							#Distance from main colors for every pixel
    for j in range(height):
        color_count = 1
        for color, rgb in sorted(color_rgb.items()):
            color_dist[i][j][color_count-1] = calcDist3D(image_rgb[i,j], rgb);
            color_count = color_count + 1

#************************FIRST METHOD******************************			
total_dist = {}

color_count=1
for color, rgb in sorted(color_rgb.items()):			#Total distance of every pixel from particular colors
    total=0
    for i in range(width):
        for j in range(height):
            total = total + color_dist[i][j][color_count-1]
    color_count = color_count + 1
    total_dist[color_names[color]] = total/(height*width)
      
sorted_total_dist = sorted(total_dist.iteritems(), key=operator.itemgetter(1))				#Sorts the list of main colors in ascenting order

print "The main colors of this image with the 1st method are " + sorted_total_dist[0][0] + ", " + sorted_total_dist[1][0] + " and " + sorted_total_dist[2][0]+"."

#***********************SECOND METHOD******************************
main_color = []
color_dict = {}

for color, rgb in sorted(color_rgb.items()):
    color_dict[color] = 0

for i in range(width):
    for j in range(height):
        color_dict[color_dist[i][j].index(min(color_dist[i][j]))+1] += 1		#Classifies the pixel as a color
           
sorted_total_dist = sorted(color_dict.iteritems(), key=operator.itemgetter(1))     
   
if color_names[sorted_total_dist[-1][0]]>30 and color_names[sorted_total_dist[-2][0]]>30 and color_names[sorted_total_dist[-3][0]]>30:
    print "The main colors of this image with the 2nd method are " + color_names[sorted_total_dist[-1][0]] + ", " + color_names[sorted_total_dist[-2][0]] + " and " + color_names[sorted_total_dist[-3][0]] + "."
else:
    print "The main color of this image with the 2nd method is " + color_names[sorted_total_dist[-1][0]] + "."      


            
