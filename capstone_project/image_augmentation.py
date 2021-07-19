import PIL
import glob
import os
import re
from PIL import Image, ImageOps, ImageFilter
# edge enhance 후 그레이 스케일
for infile in glob.glob('/Users/yubeenjo/Desktop/Capstone/오토바이번호판/test/IMG_6876.jpg'):
    file, ext = os.path.splitext(infile)
    print("infile:"+infile)
    im = Image.open(infile)
    new_im = im.filter(ImageFilter.EDGE_ENHANCE_MORE)
    new_im2 = new_im.convert('L')
    new_im2.save(file+"eng.jpg")
    im.close()
# 라벨링 값 생성
for imfile in glob.glob('/Users/yubeenjo/Desktop/Capstone/오토바이번호판/test/IMG_6876.txt'):
    file, ext = os.path.splitext(imfile)
    print("infile:"+imfile)
    open_file = open(imfile, 'r')
    read_file = open_file.read()
    regex = re.compile('15')
    read_file = regex.sub('0', read_file)
    write_file = open(imfile, 'w')
    write_file.write(read_file)
    newfile = open(file+"eng.txt",'w')
    newfile.write(read_file)
    open_file.close()
    write_file.close()
    newfile.close()

print("그레이 스케일 증강 완료!")

# 좌우 반전
for infile in glob.glob('/Users/yubeenjo/Desktop/Capstone/오토바이번호판/test/IMG_6876.jpg'):
    file, ext = os.path.splitext(infile)
    print("infile:"+infile)
    im = Image.open(infile)
    new_im = ImageOps.mirror(im)
    new_im.save(file+"f.jpg")
    im.close()

for imfile in glob.glob('/Users/yubeenjo/Desktop/Capstone/오토바이번호판/test/IMG_6876.txt'):
    file, ext = os.path.splitext(imfile)
    print("infile:"+imfile)
    open_file = open(imfile, 'r')
    # read_file = open_file.read()
    # print(read_file)
    newfile = open(file + "f.txt", 'w')
    while True:
        line = open_file.readline()
        if not line: break
        print(line)
        regex = re.compile('15')
        change_number = regex.sub('0', line)
        print(change_number)
        new_line = (change_number[0:2] + str(round(1 - float(change_number[2:10]), 6)) + change_number[10:])
        newfile.write(new_line)
        print(new_line)
    newfile.close()
    # while True:
    #     line2 = open_file.readline()
    #     if not line2: break
    #     print(line2)
    #     new_line = (line[0:2] + str(1 - float(line[2:10])) + line[10:])
    #     print(new_line)
    # new_line=(read_file[0:2]+str(1-float(read_file[2:10]))+read_file[10:])
    # regex = re.compile('15')
    # read_file = regex.sub('0', read_file)
    # write_file = open(imfile, 'w')
    # write_file.write(read_file)
    # newfile = open(file+"f.txt", 'w')
    # newfile.write(new_line)
print("all done")

# 이미지 불러오기

# image1 = Image.open('/Users/yubeenjo/Desktop/Capstone/오토바이번호판/crop/268.jpg')
#
# image1.show()
#
# # 이미지 좌우대칭
# fill = ImageOps.mirror(image1)
# fill.show()
#
# filter_img = image1.filter(ImageFilter.CONTOUR)
# filter_img.show()
# filter_img2 = image1.filter(ImageFilter.EDGE_ENHANCE_MORE)
# filter_img2.show()
# filter_img4 = image1.filter(ImageFilter.EMBOSS)
# filter_img4.show("detail")
# gray = filter_img2.convert('L')
# gray.show()
# # filter_img3 = gray.filter(ImageFilter.FIND_EDGES)
# # filter_img3.show("detail")
# # filter_img3 = image1.filter(ImageFilter.SHARPEN)
# # filter_img3.show("detail")
# # filter_img3 = image1.filter(ImageFilter.SMOOTH)
# # filter_img3.show("detail")
# print(image1.size)
