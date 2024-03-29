# 앱키 : 	128c2166d789c9f1a2ae79a9e5dfcc22
# 실행하기 : $ python ocr_test.py C:\Users\user\Desktop\2021_KU_capstone_design\OCR\text.jpg 128c2166d789c9f1a2ae79a9e5dfcc22

import json

import cv2
import requests
import sys

LIMIT_PX = 1024
LIMIT_BYTE = 1024*1024  # 1MB
LIMIT_BOX = 40


def kakao_ocr_resize(image_path: str):
    """
    ocr detect/recognize api helper
    ocr api의 제약사항이 넘어서는 이미지는 요청 이전에 전처리가 필요.

    pixel 제약사항 초과: resize
    용량 제약사항 초과  : 다른 포맷으로 압축, 이미지 분할 등의 처리 필요. (예제에서 제공하지 않음)

    :param image_path: 이미지파일 경로
    :return:
    """
    image = cv2.imread(image_path)
    height, width, _ = image.shape

    if LIMIT_PX < height or LIMIT_PX < width:
        ratio = float(LIMIT_PX) / max(height, width)
        image = cv2.resize(image, None, fx=ratio, fy=ratio)
        height, width, _ = height, width, _ = image.shape

        # api 사용전에 이미지가 resize된 경우, recognize시 resize된 결과를 사용해야함.
        image_path = "{}_resized.jpg".format(image_path)
        cv2.imwrite(image_path, image)

        return image_path
    return None


def kakao_ocr(image_path: str, appkey: str):
    """
    OCR api request example
    :param image_path: 이미지파일 경로
    :param appkey: 카카오 앱 REST API 키
    """
    API_URL = 'https://dapi.kakao.com/v2/vision/text/ocr'

    headers = {'Authorization': 'KakaoAK {}'.format(appkey)}

    image = cv2.imread(image_path)
    jpeg_image = cv2.imencode(".jpg", image)[1]
    data = jpeg_image.tobytes()


    return requests.post(API_URL, headers=headers, files={"image": data})


def main():
    # 이미지 경로 지정
    image_path = '/Users/yubeenjo/Desktop/thresh.jpg'
    # kakao Developers에서 API 키
    appkey = '128c2166d789c9f1a2ae79a9e5dfcc22'

    resize_impath = kakao_ocr_resize(image_path)
    if resize_impath is not None:
        image_path = resize_impath
        print("원본 대신 리사이즈된 이미지를 사용합니다.")

    output = kakao_ocr(image_path, appkey).json()
    print("[OCR] output:\n{}\n".format(json.dumps(output, sort_keys=True, indent=2, ensure_ascii=False)))
    temp = output['result']

    try :
        word0 = str(temp[0])
        word1 = str(temp[1])
        word2 = str(temp[2])
        word3 = str(temp[3])

        city = word0[word0.find('w') + 10:len(word0) - 2]
        province = word1[word1.find('w') + 10:len(word1) - 3]
        hangul = word2[word2.find('w') + 10:len(word2) - 2]
        num = word3[word3.find('w') + 10:len(word3) - 3]

        out1 = city + province
        out2 = hangul + num

        print(out1)
        print(out2)

    except IndexError :
        word0 = str(temp[0])
        word1 = str(temp[1])
        # word2 = str(temp[2])
        # word3 = str(temp[3])

        city = word0[word0.find('w') + 10:len(word0) - 2]
        province = word1[word1.find('w') + 10:len(word1) - 3]
        # hangul = word2[word2.find('w') + 10:len(word2) - 2]
        # num = word3[word3.find('w') + 10:len(word3) - 3]

        out1 = city + province
        # out2 = hangul + num

        # print(word0[word0.find('w') + 10:len(word0) - 3])
        # print(word1[word1.find('w') + 9:len(word1) - 2])
        # print(word2[word2.find('w') + 9:len(word2) - 2])
        # print(word3[word3.find('w') + 9:len(word3) - 2])

        print(out1)
        # print(out2)


if __name__ == "__main__":
    main()
