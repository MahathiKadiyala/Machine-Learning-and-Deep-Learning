# def sample(a,b):
#   return(a*b)
# c=sample(5,3)
# print(c)
# output: 15
#----------------------
# def sample(a,b):
#     print (a*b)
# c=sample(5,3)
# print(c)
# output:15 and none
# -------------------------
# def sample(a):
#     global b
#     b=10 #local
#     a=a*2
#     print('inside',a,b)
# a=10 #global
# print('before',a)
# sample(a)
# print('after',a,b)
# output:
# before 10
# inside 20 10
# after 10 10
# -----------------------
# def sample(a,b):
#     print(a+b)
# sample(b=10,a=0)
# output: 10
# ------------
# def sample(a,b,c=3):
#    print(a+b+c)
# sample(3,4,10)
# output: 17
# --------------------
# def sample(b,*a):
#     print(b,a)
# sample(7,8,8,6)
# def sample(**a):
#     print(a)
# Constructor doesnt require any call
# -------------------
# class Sample:
#     def __init__(self):
#         print('hi')
#     def display(self):
#         print('hello')
# s=Sample()
# s.display()
# d=Sample()
# d.display()
# -------------------------
# class Student:
#     def __init__(self,name,roll):
#         self.name=name
#         self.roll=roll
#     def details(self):
#         print('name:',self.name)
#         print('roll:',self.roll)
#     def details1(self,college):
#         print(self.name,self.roll,college)
# s1=Student('John',101)
# s2=Student('Alice',102)
# s2.details1('AU')
# s1.details()
# s2.details() 
# s1.details1('AU');
# ------------------------------------
# class Student:
#     college='AU' #class variable
#     def __init__(self,name,roll):
#         self.name=name #instance variable
#         self.roll=roll
#     def details(self):
#         print('name:',self.name)
#         print('roll:',self.roll)
#     def details1(self):
#         print(self.name,self.roll,self.college)
# s1=Student('John',101)
# s2=Student('Alice',102)
# s2.details1()
# s1.details()
# s2.details() 
# s1.details1();
# -----------------------------
# class variable
# class sample():
#     college = 'AUS' #class variable, college is common for all objects
#     def __init__(self, name,rnum):
#         self.name = name
#         self.roll = rnum
#     def show(self):
#         print(self.name,self.roll,self.college)
# s1 = sample('mahathi',84)
# s1.show()
# s2 = sample('sanju',21)
# s2.show()
#--------------------------------------
# instance variable
# class sample():
#     college = 'AUS'
#     def __init__(self, name,rnum,college):
#         self.name = name
#         self.roll = rnum
#         self.college = college #instance variable,each object can have different college name
#     def show(self):
#         print(self.name,self.roll,self.college)
# s1 = sample('anusha',220,'AUS')
# s1.show()
# s2 = sample('vijaya',221,'Acet')
# s2.show()
# --------------------------------------------
# Inheritance
# class Person:
#     def __init__(self,name,gender):
#         self.name=name
#         self.gender=gender
#     def details(self):
#         print(self.name,self.gender)
# class Student(Person):
#     def __init__(self,name,gender,rno,branch):
#         self.rno=rno
#         self.branch=branch
#         super().__init__(name,gender)
#     def details1(self):
#         print(self.name,self.gender,self.rno,self.branch)
# s1=Student('John','Male',123,'CSE')
# s1.details1() 
# -------------------------------
#encapsulation
class Bank():
    def __init__(self,name,balance=0):
        self.name=name
        self.balance=balance
    def deposit(self,amount):
        self.balance+=amount
        return 'Balance:',self.balance
    def withdraw(self,amount):
         if 0<amount<=self.balance:
            self.balance-=amount
            return 'Balance:',self.balance
         else:
            return 'Insufficient balance'
    def info(self):
        return self.name,self.balance
c1=Bank('ram')
print(c1.info())
print(c1.deposit(1000))
print(c1.info())
print(c1.withdraw(500))
print(c1.info())
# ---------------------------
#private
class Bank():
    def __init__(self,name,balance=0):
        self.name=name
        self.__balance=balance
    def deposit(self,amount):
        self.__balance+=amount
        return 'Balance:',self.__balance
    def withdraw(self,amount):
         if 0<amount<=self.__balance:
            self.__balance-=amount
            return 'Balance:',self.__balance
         else:
            return 'Insufficient balance'
    def info(self):
        return self.name,self.__balance
c1=Bank('ram')
print(c1.info())
print(c1.deposit(1000))
print(c1.info())
print(c1.withdraw(500))
print(c1.info())
print(c1.__balance) #
# c1._Bank__balance = 9999 
# print(c1.info())  



