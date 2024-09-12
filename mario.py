n = int(input("Height: "))
def bricks(n):
    for i in range(1,n+1):
        print(" "*(n-i),"#"*i," ","#"*i)
bricks(n)