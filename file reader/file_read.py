from PIL import Image
      


a=[]
f = open('filetest.txt','r')
f_content=f.readline()
x=0
y=0
who=0
temp=-1
for i in range(len(f_content)-1):
    if f_content[i] !='[' and  f_content[i] !=']' :
        if   f_content[i] ==',' or  f_content[i] ==' ':
            if who==0 and  temp !=-1:
                temp=-1
                who=1
        else:
            temp=0
            if who==0:
                x=10*x+int(f_content[i])
            else:
                y=10*y+int(f_content[i])

a=[[0] * y] * x
print(x)
print(y)
value=0
f_content=f.readline()
x=0
y=0
min_value=-1
max_value=-1
while len(f_content)>0:
    for i in range(len(f_content)-1):
        if f_content[i] !='[' and  f_content[i] !=']' :
            if   f_content[i] ==',' or  f_content[i] ==' ':
                if temp !=-1:
                    temp=-1
                    a[x][y]=value
                    if min_value==-1 or value<min_value :
                        min_value=value
                    if max_value==-1 or value>max_value :
                        max_value=value
                    if value<0 :
                        print(value)
                    value=0
                    y=y+1
            else:
                temp=0
                value=10*value+int(f_content[i])
    
    
    temp=-1
    #print(x)
    #print(y)
    
    a[x][y]=value
    if min_value==-1 or value<min_value :
        min_value=value
    if max_value==-1 or value>max_value :
        max_value=value
    if value<0 :
        print(value)
    value=0
    y=0
    x=x+1
    f_content=f.readline()

f.close()

range_value=max_value-min_value

print(a)
print(a[0][0])
#print(min_value)
#print(max_value)
#print(range_value)
who=0
i=0
j=0

print("min val : " + str(min_value))

for i in range(0, len(a)):
    for j in range(0, len(a[i])):
        print(i, j, end=" - ")
        #print(a[i][j],end=' ')
        
        temp=a[i][j]-min_value
        #print("temp : " + str(temp))
        
        #if temp <0 :
            #print(a[i][j])
            #print('min_value '+ str(min_value))
        temp_float=float(temp/range_value)
        #print("temp_float : " + str(temp_float))
        
        #if temp_float <0 :
            #print('temp '+str(temp))
            #print('range_value '+str(range_value))
        temp_float=temp_float*255
        #print("temp_float : " + str(temp_float))
        #if temp_float <0 :
            #print('temp '+str(temp))
        
        a[i][j]=int(temp_float)
        #print("tqt" + str(a[i][j]), end=" ") 
        if a[i][j] >255 :
            a[i][j] = 255
        if a[i][j] < 0 :
            a[i][j] = 0
        #print(a[i][j], end=" ,")
    print( )
    


img = Image.new('RGB', (len(a), len(a[0])), color = (0, 0, 0))

for i in range(len(a)-1):
    for j in range(len(a[0])-1):
        value=a[i][j]
        #print(i)
        #print(j)
        #print(value)
        img.putpixel((i,j),(a[i][j],a[i][j],a[i][j]))
        
img.save('pil_color.png')
img.show()

