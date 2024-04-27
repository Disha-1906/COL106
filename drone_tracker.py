class Empty(Exception):
    pass
class Stack:
    def __init__(self):
        self._data=[]    
    def __len__(self):
        return len(self._data)     
    def push(self,i):
        self._data.append(i)
    def top(self):
        if len(self._data)==0:
            raise Empty("Stack is already empty!")
        return self._data[-1]
    def pop(self):
        if len(self._data)==0:
            raise Empty("No element left to pop!")
        return self._data.pop()

def findPositionandDistance(P):

    # 4 Empty stacks have been declared. The final_num stack stores the product or the final number that has to be multiplied to the variable x,y or z. The num_tracker stack keeps a track of numbers whose product is to be pushed in final_num. The solve stack stores opening and closing brackets and variables (along with signs +,-) i.e +X,-X..etc in the order as they come in the string. The buffer stack stores buffer value especially in case when the closing bracket is followed by an integer.
    
    final_num = Stack()
    num_tracker = Stack()
    solve = Stack()
    buffer = Stack()

    # String has been traversed using while loop. 
    # If '+'or '-' are approached, then the sign along with th variable(X, Y or Z) is pushed into the solve stack. Furthermore, 1 is pushed in final_num if len(num_tracker) is 0 and if the sign is not following a closing bracket.
    # If a digit is approached then it is checked if the current digit is following an another digit or not. If it doesn't then the integral value of digit is stored in variable 'num'. If it follows a digit then the value of num is udpated accordingly. This helps in dealling with numbers having multiple digits.
    # If '(' is approached the value of num is pushed into num_tracker. If buffer stack has an element then num*buffr.pop() is pushed into final_num, if len(final_num)==0 num is pushed into fianl_num , else num*final_num.top() is pushed into final_num. Finally '(' is pushed into solve.
    # If ')' is approached the top of num_tracker is popped (since it is of no use now). If the ')' is not following another closing bracket the value of final_num.top()//num_tracker.pop() is stored in q. If '+' or '-' follows ')' q is directly pushed in final_num (because now this q will be required for further calculations). If a digit follow ')', then q is pushed into buffer (because now we will require the product of q and incoming digit for further calculations and therefore this product has to be pushed in final_num). Finally ')' is pushed into solve.

    i = 0
    while i<len(P):
        if P[i]=='+' or P[i]=='-':
            solve.push(P[i:i+2])
            if i==0:
                if len(num_tracker)==0:
                    final_num.push(1)
            else:
                if len(num_tracker)==0 and P[i-1]!=')':
                    final_num.push(1)
            i = i + 2
        elif P[i].isdigit():
            if  i==0:
                num = int(P[i])
            elif P[i-1].isdigit():
                num = num*10 + int(P[i])
            else:
                num = int(P[i])
            i = i + 1
        elif P[i]=='(':
            num_tracker.push(num)
            if len(buffer)!=0:
                final_num.push(num*int(buffer.pop()))
            elif len(final_num)==0:
                final_num.push(num)
            else:
                final_num.push(int(final_num.top())*num)
            solve.push(P[i])
            i = i + 1
        elif P[i]==')':
            if i == len(P)-1:
                if len(num_tracker)!=0:
                    num_tracker.pop()
            if P[i-1]==')' and len(num_tracker)!=0:
                q = q//num_tracker.pop()
                if P[i+1]=='+' or P[i+1]=='-':
                    final_num.push(q)
                if P[i+1].isdigit():
                    buffer.push(q)
            elif len(num_tracker)!=0:
                q = int(final_num.top())//int(num_tracker.pop())
                if P[i+1]=='+' or P[i+1]=='-':
                    final_num.push(q)
                if P[i+1].isdigit():
                    buffer.push(q)
            solve.push(P[i])
            i = i + 1

    # The values of x,y,z and dist which indicate the displacements along x,y,z directions and total distance respectively, have been initialised zero. A boolean variable r has been initialised False.

    x = 0
    y = 0
    z = 0
    dist = 0
    r = False

    # findA() is a helper function which helps in finding the value of a (the value by which a variable is incremented during every operation). The function has been defined to avoid repitition. The value stored by a is equal to the final_num.top() if the value of r is True or solve.top!=')' or  len(final_num)!=0 or final_num.top()!=1. This specially avouds popping of same element twice during function operation when the top value of final_num is 1 (once due to opening bracket and once due to variable). It returns the value of a.

    def findA():
        if len(solve)==0:
            a = final_num.pop()
        elif r == True:
            a = final_num.top()
        else:
            if solve.top()==')' and len(final_num)!=0:
                a = final_num.pop()
            elif final_num.top()==1:
                a = final_num.pop()
            else:
                a = final_num.top()
        return a

    # Finally, the value of each variable is calculated by running a while loop until thr solv stack becomes empty. Variable t has been assigned value solve.pop(). If t = ')' the value of r is updated only if final_num.top()==1 else the loop is continued. If t is equal to any signed variable then the value of a is obtained by calling findA() and corresponding value of variable and dist is updated. If t = '(' , the value of r is updated only if it is True and top of final_num is popped (since it is of no use now). The function returns a tuple containing final values of x,y,z and dist.
    
    while len(solve)!=0:
        t = solve.pop()    
        if t == ')':
            if final_num.top()==1:
                r = True
            continue
        if t == '+X':
            a = findA()
            x = x + a
            dist = dist + a
        if t == '-X':
            a = findA()
            x = x - a
            dist = dist + a
        if t == '+Y':
            a = findA()
            y = y + a
            dist = dist + a
        if t == '-Y':
            a = findA()
            y = y - a
            dist = dist + a
        if t == '+Z':
            a = findA()
            z = z + a
            dist = dist + a
        if t == '-Z':
            a = findA()
            z = z - a
            dist = dist + a
        if t == '(':
            if r==True:
                r == False
            final_num.pop()
    return([x, y, z, dist])

