from copy import deepcopy
class Board:
    def __init__(self,n):
        self.n=n
        self.matrix = []
        for i in range(self.n):
            temp=[]
            for j in range(self.n):
                temp.append(0)
            self.matrix.append(temp)
    def display(self):
        print("Matrix: ")
        for i in range(self.n):            
            for j in range(self.n):
                if(self.matrix[i][j]==0):
                    print("-",end=" ")
                else:
                    print("Q",end=" ")
            print()
    
    def IsFree(self,i,j):
        if(self.matrix[i][j]==1):
            return False
        
        for k in range(self.n):
            if(self.matrix[i][k]==1):
                return False
        for k in range(self.n):
            if(self.matrix[k][j]==1):
                return False

        k=1
        while(i+k<self.n and j+k<self.n):
            if(self.matrix[i+k][j+k]==1):
                return False
            k+=1
        k=1
        while(i-k>=0 and j-k>=0):
            if(self.matrix[i-k][j-k]==1):
                return False
            k+=1
        k=1
        while(i+k<self.n and j-k>=0):
            if(self.matrix[i+k][j-k]==1):
                return False
            k+=1
        k=1
        while(i-k>=0 and j+k<self.n):
            if(self.matrix[i-k][j+k]==1):
                return False
            k+=1
        return True
    
    def fill(self,i,j):
        if(i>=0 and j>=0 and i<self.n and j<=self.n and self.IsFree(i,j)):
            self.matrix[i][j]=1

    
    def empty(self,i,j):
        if(i>=0 and j>=0 and i<self.n and j<=self.n):
            self.matrix[i][j]=0
    
    def Solve(self):
        if(self.nQueen(0,self.n)):
            print("\n\n------------")
            self.display()
            return
        print("Not Solvable")
    
    def nQueen(self,x,n):
        if(x>=n):
            return True
        for i in range(self.n):
            if(self.IsFree(x,i)):
                self.fill(x,i)
                if(self.nQueen(x+1,n)):
                    return True
                self.empty(x,i)
        return False


board = Board(int(input("Enter n:")))
board.Solve()