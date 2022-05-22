class position:
    x = 0
    y = 0

    def __init__(self,x,y) -> None:
        self.x = x
        self.y = y

    def print_pos(self):
        print(str(self.x)+','+str(self.y))

if __name__ == "__main__":
    pos = position(1,2)
    pos.print_pos()
    data = '0.1234'
    fdata = float(data)
    print(type(fdata))
    print(fdata)