import numpy as np
import cv2
import math

img_org = np.zeros((512,512), np.uint8)
cv2.circle(img_org,(256,256),30,255,-1)
img=img_org.copy()

start_end=[]
nodes_list=[]
distance_list=[]
point_dist=25


def gen_sample():
	
	
	#sample=np.random.randint(512,size=(2,))
	#sample=tuple(sample)
	while (True):
		sample=np.random.randint(512,size=(2,))		
		if (np.where(np.asarray(nodes_list)==tuple(sample))[0].shape[0]==0):
			# print "generated sample "
			
			break

	return tuple(sample)


def check_collision(sample,nearest_node):
	line_img=np.zeros((512,512), np.uint8)
	cv2.line(line_img,sample,nearest_node,255,1)
	collision=cv2.bitwise_and(img_org.copy(),line_img)
	# print "collision[0]= ",collision[0]
	# condition=np.where(collision==255)
	# cv2.imshow("collision",collision)
	# cv2.waitKey(1)
	# print "max collision : ",np.max(collision)
	if (np.max(collision)==255):
		# print "no collision"
		return True
	else:
		return False


def distance(pt1,pt2):
	#print pt1,pt2
	return math.sqrt((pt1[0]-pt2[0])**2+(pt1[1]-pt2[1])**2)


def gen_tree():
	nodes_list.append(start_end[0])
	while(True):
		
		sample=gen_sample()
		# print "sample ",sample
		distance_list_org=[distance(i,sample) for i in nodes_list]
		distance_list=np.sort([distance(i,sample) for i in nodes_list])
		# if(distance(new_pt,start_end[-1])==0):
		# 	break
		min_dist=distance_list[0]
		# print np.where(distance_list_org==min_dist)[0]
		index=np.where(distance_list_org==min_dist)[0][0]
		# print index
		nearest_node=nodes_list[index]
		# print "nearest node ",nearest_node
		condition=check_collision(sample,nearest_node)
		if(condition==False):

			
			ratio=point_dist/min_dist
			new_pt=(int((ratio*sample[0]+(1-ratio)*nearest_node[0])/(1)),int((ratio*sample[1]+(1-ratio)*nearest_node[1])/(1)))
			nodes_list.append(new_pt)
			
			#print "new pt"new_pt
			cv2.line(img,new_pt,nearest_node,255,1)
			cv2.imshow("path window",img)
			cv2.waitKey(1)
			if(distance(new_pt,start_end[-1]) < 20):
				print "st",start_end
				cv2.line(img,new_pt,start_end[-1],255,1)
				print "goal reached"
				cv2.imshow("path window",img)
			
				cv2.waitKey(0)
				break
			

def onmouse(event, x, y, flags, param):
	
	if event == cv2.EVENT_LBUTTONDOWN:
		start_end.append((x, y))
		img[y][x]=255
	if event == cv2.EVENT_RBUTTONDOWN:
		print start_end
		if (len(start_end))==2:
			gen_tree()



def purepursuit():
	cv2.namedWindow("path window")
	cv2.setMouseCallback("path window", onmouse)
	while (True):
		cv2.imshow("path window",img)

	
		if cv2.waitKey(5)==8:
			break 

purepursuit()

