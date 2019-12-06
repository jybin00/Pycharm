print("postfix 계산기")  # postfix 계산기 2018170921 조유빈


def is_digit(string):  # 음수 입력을 받기 위한 함수
    try:
        tmp = float(string)
        return True
    except ValueError:
        return False


def op(operand):  # operand 사이의 우선 순위 계산을 위한 함수
    j = 0  # j 초기화
    if operand in '^':  # 제곱 기호면 3 출력
        j = 3
    elif operand in ('*', '/'):  # 곱하기 나누기면 2 출력
        j = 2
    elif operand in ('+', '-'):  # 더하기 뻬기면 1 출력
        j = 1
    elif operand in ('(', ')'):  # 괄호면 0 출력
        j = 0
    return j


def top(stack):  # stack의 최상단에 있는 값을 출력하기 위한 함수
    j = 0
    j = op(stack[-1])
    return j


def calc(num2, num1, operand):  # 계산을 위한 함수
    if operand == '+':
        return num1 + num2
    elif operand == '-':
        return num1 - num2
    elif operand == '*':
        return num1 * num2
    elif operand == '/':
        return num1 / num2
    else:
        return pow(num1, num2)


flag = 1
while flag != 0:  # 무한 루프
    print("수식을 입력해주세요")
    formula = []  # 수식을 입력 받는 list
    formula = list(input().split())
    print("입력된 수식 : ", end=' ')
    for i in range(len(formula)):  # 입력된 수식 출력
        print(formula[i], end=' ')
    print(" ")
    stack_num = []  # 수식 중에서 숫자를 저장하는 stack
    stack_operand = []  # 수식 중에서 연산자를 저장하는 stack
    stack_calc = []  # 계산한 값을 저장하는 stack

    for i in range(len(formula)):  # 입력 받은 수식의 길이 만큼 반복한다.
        carry = 0  # 제곱에 대해서는 'right associative'를 적용하기 위해서 필요한 변수
        if is_digit(formula[i]) == 1:  # 들어온 수식의 i번째 요소가 숫자이면
            stack_num.append(formula[i])  # 숫자용 stack에 넣는다.
            if i == (len(formula)-1):  # 만약 i가 끝이면,
                while True:
                    if len(stack_operand) == 0:  # 연산자 stack이 비어있지 않을 때
                        break
                    else:
                        stack_num.append(stack_operand.pop())  # 연산자 stack에 저장된 연산자를 숫자용 stack으로 옮긴다.

        elif len(stack_operand) == 0:  # 연산자 stack이 비어있으면 -> 초기에 top operation에 대해 out of range를 막기 위해
            stack_operand.append(formula[i])  # 무조건 연산자 stack에 연산자 넣기

        else:
            if formula[i] == '(' or top(stack_operand) < op(formula[i]):  # 수식 요소 중에서 '('나 top 보다 큰 요소가 있으면
                stack_operand.append(formula[i])  # 수식 stack에 넣는다.
            elif top(stack_operand) >= op(formula[i]):  # 만약 요소가 top 요소 보다 크거나 같으면
                while True:  # top 요소가 수식 요소보다 작아질 때까지 연사자 stack에 저장된 요소를 숫자 stack에 빼서 넣는다.
                    if formula[i] == '^':  # 만약에 제곱 연산자가 있으면 그냥 연산자 stack에 넣는다.
                        stack_operand.append((formula[i]))  # right associative를 위해!
                        carry = 1  # 반복문 탈출을 위한 장치
                        break
                    elif stack_operand[-1] == '(':  # 계속 숫자 스택에 넣다가 연산자 스택의 top이 '('이면 그냥 버린다.
                        stack_operand.pop()
                        break
                    else:  # 위 조건을 모두 만족하지 않으면 연산자 스택에 있는 요소를 숫자 요소에 넣는다.
                        stack_num.append(stack_operand.pop())
                        if len(stack_operand) == 0:  # 연산자 stack이 비어 있으면 멈춘다.
                            break
                        elif top(stack_operand) < op(formula[i]):  # 계속 옮기다가 수식 요소가 연산자 스택 요소보다 커지면 멈춘다.
                            break
                if i == (len(formula) - 1):  # 만약 i가 마지막이면 -> 위에 있는데 또 넣는 이유 ex) 1 + ( 2 + 3 )인 경우 괄호가
                    while True:  # 제일 마지막이여서 이 경우도 고려해줘야함.
                        if len(stack_operand) == 0:  # 만약 스택이 비어있으면 멈춘다.
                            break
                        else:
                            stack_num.append(stack_operand.pop())  # 그렇지 않으면 수식 스택에 있는 것을 숫자 스택을 옮긴다.
                elif formula[i] != ')' and carry == 0:  # 수식 요소가 ')'가 아니거나 캐리가 0 이면
                    stack_operand.append(formula[i])  # 수식 요소를 연산자 스택에 넣는다.
            elif formula[i] == ')':  # 수식 요소가 ')'이면
                while True:
                    stack_num.append(stack_operand.pop())  # 연산자 스택에 있는 연산자를 숫자 스택에 옮긴다.
                    if len(stack_operand) == 0:  # 연산자 스택이 비어 있으면 멈춘다.
                        break
                    elif stack_operand[-1] == '(':  # 연산자 스택의 탑이 '('이면 멈춘다.
                        break

    print("postfix notation", end=' ')
    for i in range(len(stack_num)):
        print(stack_num[i], end=' ')
    print("\n")
    print("계산 과정\n")

    for j in range(len(stack_num)):
        if is_digit(stack_num[j]) != 0:
            stack_calc.append(stack_num[j])
            print(stack_calc)
        else:
            print('%s %s %s =' % (stack_calc[-2], stack_num[j], stack_calc[-1]), end=' ')
            stack_calc.append(calc(float(stack_calc.pop()), float(stack_calc.pop()), stack_num[j]))
            print('%s\n' % (stack_calc[-1]))
            print(stack_calc)  #연산자가 나오면 스택에 들어 있는 숫자 2개를 꺼내어 계산한 후에 다시 넣는다.
    print('\n따라서 답은 %f\n' % float(stack_calc[-1]))

