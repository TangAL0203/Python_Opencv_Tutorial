#-*-coding:utf-8-*-
import cv2
import numpy as np
import os
import os.path as osp
import copy

# 计算两个bbx之间的IOU
# x1y1x2y2为True，输入bbx形式为x1y1x2y2
# x1y1x2y2为False，输入bbx形式为xywh
def bbox_iou(box1, box2, x1y1x2y2=True):
    if x1y1x2y2:
        mx = min(box1[0], box2[0])
        Mx = max(box1[2], box2[2])
        my = min(box1[1], box2[1])
        My = max(box1[3], box2[3])
        w1 = box1[2] - box1[0] # IOU-1的宽
        h1 = box1[3] - box1[1] # # IOU-1的高
        w2 = box2[2] - box2[0]
        h2 = box2[3] - box2[1]
    else:
        mx = min(box1[0]-box1[2]/2.0, box2[0]-box2[2]/2.0)
        Mx = max(box1[0]+box1[2]/2.0, box2[0]+box2[2]/2.0)
        my = min(box1[1]-box1[3]/2.0, box2[1]-box2[3]/2.0)
        My = max(box1[1]+box1[3]/2.0, box2[1]+box2[3]/2.0)
        w1 = box1[2]
        h1 = box1[3]
        w2 = box2[2]
        h2 = box2[3]
    uw = Mx - mx # 并集的宽
    uh = My - my # 并集的高
    cw = w1 + w2 - uw # 交集的宽
    ch = h1 + h2 - uh # 交集的高
    carea = 0
    if cw <= 0 or ch <= 0:
        return 0.0

    area1 = w1 * h1 # IOU-1的面积
    area2 = w2 * h2 # IOU-2的面积
    carea = cw * ch # 交集的面积
    uarea = float(area1) + float(area2) - float(carea) # 并集的面积
    return carea/uarea


# 传入bbx坐标格式为：x,y,w,h,confidence。2-D list
def nms(bbx_pre, nms_thresh, x1y1x2y2=True):
    if len(bbx_pre) ==0:
        return bbx_pre

    det_confs = np.zeros(len(bbx_pre))
    for i in range(len(bbx_pre)):
        det_confs[i] = 1 - bbx_pre[i][4]

    sortIds = np.argsort(det_confs)
    np.sort(det_confs)

    out_bbx = []
    for i in range(len(bbx_pre)):
        bbx_i = bbx_pre[sortIds[i]]
        if bbx_pre[i][4] > 0:
            out_bbx.append(bbx_i)
            for j in range(i+1, len(bbx_pre)):
                bbx_j = bbx_pre[sortIds[j]]
                if bbox_iou(bbx_i, bbx_j, x1y1x2y2) > nms_thresh:
                    print bbox_iou(bbx_i, bbx_j, x1y1x2y2)
                    bbx_j[4] = 0

    return out_bbx


def nms_show(img, bbx_pre, bbx_done, x1y1x2y2=True):
    H = img.shape[0]
    W = img.shape[1]
    b = np.zeros((H, 2*W), dtype='uint8')
    g = np.zeros((H, 2*W), dtype='uint8')
    r = np.zeros((H, 2*W), dtype='uint8')

    img_pre = img.copy()
    img_done = img.copy() # 深拷贝
    # img_pre = np.zeros(img.shape,np.uint8)
    # img_done = np.zeros(img.shape,np.uint8)
    # img_pre = copy.deepcopy(img) # 
    # img_done = copy.deepcopy(img) #
    print "len bbx_pre is: ", len(bbx_pre)
    print "len bbx_pre is: ", len(bbx_done)
    for i in range(len(bbx_pre)):
        if x1y1x2y2:
            pt1 = (int(max(bbx_pre[i][0],0)), int(max(bbx_pre[i][1],0)))
            pt2 = (int(min(bbx_pre[i][2],W)), int(min(bbx_pre[i][3],H)))
        else:
            pt1 = (int(max(bbx_pre[i][0]-bbx_pre[i][2]/2,0)), int(max(bbx_pre[i][1]-bbx_pre[i][3]/2,0)))
            pt2 = (int(min(bbx_pre[i][0]+bbx_pre[i][2]/2,W)), int(min(bbx_pre[i][1]+bbx_pre[i][3]/2,H)))
        img_pre = cv2.rectangle(img_pre, pt1, pt2, (0,255,0), thickness=1)

    for i in range(len(bbx_done)):
        if x1y1x2y2:
            pt1 = (int(max(bbx_done[i][0],0)), int(max(bbx_done[i][1],0)))
            pt2 = (int(min(bbx_done[i][2],W)), int(min(bbx_done[i][3],H)))
        else:
            pt1 = (int(max(bbx_done[i][0]-bbx_done[i][2]/2,0)), int(max(bbx_done[i][1]-bbx_done[i][3]/2,0)))
            pt2 = (int(min(bbx_done[i][0]+bbx_done[i][2]/2,W)), int(min(bbx_done[i][1]+bbx_done[i][3]/2,H)))
        img_done = cv2.rectangle(img_done, pt1, pt2, (0,255,0), thickness=1)
    cur_path = os.getcwd()
    pre_path = osp.join(cur_path, "img_pre.jpg")
    done_path = osp.join(cur_path, "img_done.jpg")
    merge_path = osp.join(cur_path, "merged.jpg")

    cv2.imwrite(pre_path, img_pre)
    cv2.imwrite(done_path, img_done)
    b[0:H,0:W]=img_pre[:,:,0]
    g[0:H,0:W]=img_pre[:,:,1]
    r[0:H,0:W]=img_pre[:,:,2]
    b[0:H,W:2*W]=img_done[:,:,0]
    g[0:H,W:2*W]=img_done[:,:,1]
    r[0:H,W:2*W]=img_done[:,:,2]
    merged = cv2.merge([b,g,r])
    cv2.imwrite(merge_path,merged)
    cv2.imshow("NMS处理前后图片对比", merged)
    cv2.waitKey(0)


img_path = "./img_90.jpg"
nms_thresh = 0.11 # NMS中，IOU交叉阈值
bbx_pre = [[84.172638 ,106.537832 ,162.237806 ,221.750309 ,0.998269],
[85.312207 ,106.181487 ,162.555170 ,222.341964 ,0.996838],
[81.162164 ,109.113108 ,168.615503 ,227.748258 ,0.988828],
[81.926787 ,102.621827 ,167.628579 ,232.364514 ,0.985726],
[88.175046 ,107.468411 ,159.869893 ,216.414014 ,0.984214],
[88.723113 ,108.413581 ,159.728385 ,221.411278 ,0.950339],
[89.748586 ,106.909297 ,155.963475 ,215.989615 ,0.942903],
[88.833341 ,94.788945 ,159.271980 ,229.874861 ,0.904516],
[86.316651 ,102.067602 ,163.209425 ,231.787008 ,0.896630],
[88.181859 ,108.783625 ,160.029849 ,225.920762 ,0.865945],
[87.500219 ,108.326436 ,160.963574 ,213.578155 ,0.864276],
[89.471578 ,108.239519 ,161.550849 ,215.163461 ,0.809613],
[89.201115 ,103.817938 ,157.743689 ,222.333314 ,0.801652],
[86.553812 ,111.001731 ,172.245820 ,228.475271 ,0.681380],
[88.190029 ,104.304866 ,155.562882 ,216.796350 ,0.667186],
[92.335174 ,109.606010 ,159.540796 ,220.312243 ,0.660954],
[86.396774 ,109.389482 ,159.874517 ,217.542668 ,0.653883],
[91.274457 ,107.462483 ,158.593483 ,212.339471 ,0.576184],
[82.027756 ,108.175997 ,165.595196 ,219.599225 ,0.536470],
[92.362511 ,113.058704 ,163.566298 ,224.296296 ,0.403761],
[67.329631 ,69.178288 ,176.910433 ,260.896124 ,0.303227],
[91.792531 ,117.791516 ,154.158440 ,217.048752 ,0.294179],
[82.423747 ,114.281845 ,168.354342 ,213.312435 ,0.233041],
[95.573684 ,94.712515 ,154.462699 ,231.217025 ,0.212347],
[92.633500 ,107.750814 ,157.582183 ,213.420756 ,0.207760],
[60.885501 ,57.438232 ,195.922837 ,285.608308 ,0.199471],
[98.424733 ,112.635505 ,152.222700 ,236.463171 ,0.177404],
[71.623167 ,61.245561 ,170.669571 ,281.744921 ,0.109696],
[60.488824 ,99.744970 ,188.050500 ,277.076268 ,0.102856],
[95.321009 ,123.952737 ,162.680912 ,204.822332 ,0.087247],
[51.944497 ,93.985207 ,201.720872 ,291.293089 ,0.083664],
[99.936973 ,122.655192 ,151.807698 ,212.032002 ,0.079334],
[93.607872 ,105.452690 ,149.210064 ,201.205795 ,0.075551],
[51.231887 ,25.533436 ,262.210436 ,391.710247 ,0.058718],
[75.561846 ,96.779171 ,163.585305 ,228.582063 ,0.055949],
[92.288718 ,113.285123 ,147.031617 ,233.268835 ,0.055297],
[65.260066 ,85.704135 ,200.903260 ,223.746235 ,0.055154],
[91.915226 ,47.643194 ,204.793868 ,288.217896 ,0.055042],
[87.836852 ,121.189351 ,153.288224 ,211.192672 ,0.052557],
[72.225028 ,89.432399 ,165.465233 ,290.126999 ,0.051813],
[47.587420 ,20.541497 ,273.158087 ,406.272577 ,0.050756],
[92.808670 ,57.447566 ,193.997022 ,263.401763 ,0.047614],
[75.651721 ,91.419058 ,172.106951 ,232.700904 ,0.038388],
[91.248515 ,93.940502 ,151.130805 ,222.627995 ,0.037653],
[89.721211 ,78.015965 ,201.898767 ,230.403015 ,0.036929],
[54.309368 ,3.831053 ,246.853137 ,436.508113 ,0.032721],
[100.225418 ,117.320198 ,142.299192 ,142.773208 ,0.027546],
[90.960038 ,94.687946 ,212.794490 ,307.535313 ,0.025946],
[47.545298 ,123.831595 ,212.152702 ,248.161827 ,0.024733],
[82.519630 ,100.155770 ,147.112395 ,214.821050 ,0.023901],
[82.578430 ,94.544200 ,157.661882 ,217.793059 ,0.022251],
[87.191411 ,116.113244 ,117.224330 ,193.421508 ,0.02200]]

# circle(img, center, radius, color[, thickness[, lineType[, shift]]]) -> None
# thickness=-1：表示对封闭图像进行内部填满
# img = cv2.imread('1.jpg')
# cv2.circle(img, center=(0,0), radius=3, color=(0,0,255),thickness=-1)
# cv2.imshow('hh.jpg', img)
# cv2.waitKey(0)

if __name__ == "__main__":
    
    img =cv2.imread(img_path)
    bbx_done = nms(bbx_pre, nms_thresh, x1y1x2y2=True)
    nms_show(img, bbx_pre, bbx_done, x1y1x2y2=True)
