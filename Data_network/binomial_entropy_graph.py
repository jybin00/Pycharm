import matplotlib.pyplot as plt  # 그래프를 그리기 위한 라이브러리
import math  # 로그와 power계산을 위한 라이브러

p_value = [] # p값을 바꾸기 위해서 값을 담을 리스트 선언
for i in range(0, 105): # p 값을 0.024 ~ 0.969까지 0.009 간격으로 저장
    p_value.append(0.024 + i*0.009)


def b_entropy_p(n):  # 엔트로피 계산 함수
    number_p = [] # p값에 따라 달라지는 엔트로피 값을 담기 위한 리스트
    for p in p_value:
        value_hy = 0  # 엔트로피는 확률의 역수의 log2를 취한 확률변수값의 평균이기 때문에 더해줄 변수 설정
        for k in range(0, n):  # n 횟수가 변수로 설정됨.
            prob = math.factorial(n)/(math.factorial(n-k)*math.factorial(k))\
                   * pow(p, k)*pow(1-p, n-k)
            value_hy += prob * math.log2(1/prob)  # 계산한 값을 다 더해야 엔트로피가 되므로 다 더해줌.
        number_p.append(value_hy)  # 각 p에 따라 계산된 엔트로피를 리스트에 넣어줌.
    return number_p  # 리스트를 반환.


plt.plot(p_value, b_entropy_p(20), color='indigo', marker=',', label='n=20')
plt.plot(p_value, b_entropy_p(60), color='navy', marker=',', label='n=60')
plt.plot(p_value, b_entropy_p(100), color='blue', marker=',', label='n=100')
plt.plot(p_value, b_entropy_p(120), color='green', marker=',', label='n=120')
plt.plot(p_value, b_entropy_p(150), color='yellow', marker=',', label='n=150')
plt.plot(p_value, b_entropy_p(170), color='orange', marker=',', label='n=170')
plt.plot(p_value, b_entropy_p(200), color='red', marker=',', label='n=200')
plt.legend()
plt.xlabel('p')
plt.ylabel('H(Y)')
plt.show()

a = b_entropy_p(200)
b = p_value
for index1 in enumerate(b):
    print(index1)
for index in enumerate(a):
    print(index)
