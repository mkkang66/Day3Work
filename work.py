from flask import Flask,request

app = Flask(__name__)

app.env = 'development'
app.debug = True

@app.route('/')
def index():

   return "Welcome, Day3"

@app.route('/gugu/<num>')
def gugu(num):
   if not num.isnumeric():
      return "Not Number"

   gugu = []
   for i in range(1, 10):
      gugu.append(f"{num} x {i} = {i*int(num)}")

   return '<br>'.join(gugu)

# 과제2
# 사용자로부터 숫자를 N을 입력받은 후 1부터 N까지의 숫자 중 소수만 출력하세요.
# /prime?num=N
def isPrime(num):
   if num == 2 or num == 3: return True

   #n = num
   for k in range(2, num):
      if num % k == 0:
         return False
   return True

@app.route('/prime')
def sosu():
   num = request.args.get('num') 
   if not num.isnumeric():
      return "Not Number"
   
   if int(num) == 1:
      return "1 Is Not Prime"

   sosu = []
   for i in range(2, int(num)+1):
      rslt = isPrime(i)
      if rslt == True:
         sosu.append(f"{i} is Prime.")

   return '<br>'.join(sosu)

#과제3
# 사용자로부터 숫자를 N을 입력받아. N의 약수를 모두 출력하세요. 
# /common_factor?num=N

@app.route('/common_factor')
def factor():
   num = request.args.get('num') 
   if not num.isnumeric():
      return "Not Number"

   factor = []
   for i in range(1, int(num)+1):
      #rslt = isfactor(i)
      if int(num) % i == 0:
         factor.append(f"{i} is Divisor.")

   return '<br>'.join(factor)


# 과제4
# 사용자로부터 숫자를 N, M을 입력받아 N과 M의 최대공약수와 최소공배수를 출력하세요. 
# /commons?num1=N&num2=M
def getGCM(N, M):
   if N < M:
      t = M
      M = N
      N = t

   while M > 0:
      t = N % M 
      if t == 0:
         return str(M)
      N = M
      M = t

   return str(1)

#최소 공배수 구하기 : 두수곱의 값/최대공약수
def getLCM(N, M):
   lcm = N*M // int(getGCM(N, M))
   return str(lcm) 

@app.route('/commons') # commons?num1=N&num2=M
def commons():
   num1 = request.args.get('num1')
   num2 = request.args.get('num2')

   if not num1.isnumeric() or not num2.isnumeric():
      return "N or M Is Not Numeric"
   
   N = int(num1)
   M = int(num2)
   if not N or not M:
      return "N or M Is Zero" 
   
   gcd = getGCM(N, M)
   lcm = getLCM(N, M)
   return "최대공약수 : "+gcd+" 입니다.<br>"+"최소공배수 : "+lcm+" 입니다."

#과제5
# 사용자로부터 숫자를 N을 입력받아, 1, 5, 10, 25, 50의 숫자를 이용하여 최소 갯수로 N을 표현해보자 
# 예) 183 = 50 * 3 + 25 * 1 + 5 * 1 + 1 * 3 => 총 8개
# /coins?num=N
@app.route('/coins')
def coins():

   num = request.args.get('num') 
   if not num.isnumeric():
      return "Not Number"

   inum = int(num)
   list_num = [50,25,10,5,1]
   coin = {}

   # 입력숫자를 리스트의 큰수별로 나누어 나눈몫을 곱하고, 차례대로..
   for i in list_num:
      # 첫번째 수가 inum보다 작으면 
      if inum > i :
         M = inum // i
         N = inum % i
         coin[i] = M
         inum = N  

   prt = []
   for key, value in coin.items():
      prt.append(f"{key}원 * {value} ")
   return f'{num}원 = ' + ' + '.join(prt)

#과제6
# 주민등록번호를 입력받아 올바른 주민번호인지 검증하라.
# 주민번호 : ① ② ③ ④ ⑤ ⑥ - ⑦ ⑧ ⑨ ⑩ ⑪ ⑫ ⑬
# 합계 
# = 마지막수를 제외한 12자리의 숫자에 2,3,4,5,6,7,8,9,2,3,4,5 를 순서대로 곱산수의 합
# = ①×2 + ②×3 + ③×4 + ④×5 + ⑤×6 + ⑥×7 + ⑦×8 + ⑧×9 + ⑨×2 + ⑩×3 + ⑪×4 + ⑫×5
# 나머지 = 합계를 11로 나눈 나머지
# 검증코드 = 11 - 나머지
# 여기서 검증코드가 ⑬자리에 들어 갑니다.
# verify_jumin('101010-2020200')
# /jumin 
# with form post

@app.route('/jumin', methods=['get', 'post'])
def verify_jumin():
   # 폼 호출
   with open('./WEB/form.html', 'r', encoding='utf8') as f:
      template = f.read()

   juminNo = ''
   rslt = ''
   if request.method == 'POST':
      juminNo = request.form.get('number')
      
      for i in range(14):
         if not juminNo[i].isnumeric() and i != 6:
            return "Not Number"
      
      list_chk = [2, 3, 4, 5, 6, 7, 8, 9, 2, 3, 4, 5]
      list_num = []
      for i in range(14):
         if i != 6:
            list_num.append(int(juminNo[i]))

      sum = 0
      for j in range(12):
         sum += list_num[j] * list_chk[j]

      MM = sum % 11
      code = 11 - MM
      if code > 9:
         code -= 10

      rslt = '주민번호가 '+str((int(juminNo[-1]) == code))+' 입니다.'

   return template.format(result=rslt)

#과제7
# 원의 원주율을 구해보자
# /pi

#파이썬3.5.1
@app.route('/pi')
def pi():
   import random

   n=4000000000
   count=0
   for i in range(n):
      x=random.uniform(0,1.0)
      y=random.uniform(0,1.0)
      if (x**2+y**2)<=1:
         count=count+1

   pp = 4*count/n

   return f"파이값 = {pp}"

app.run()