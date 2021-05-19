def test(coords_string):
    f = open("coords", "w")
    for coord in coords_string:
        if coord != ",":
            f.write(coord + "\n")
    f.close()
    f = open("coords", "r")
    lines = f.readlines()
    hz = []
    for line in lines:
        hz.append(line)
    i = 0
    hz_tuples =[]
    while(i < 7):
        hz_tuples.append((hz[i][:-1], hz[i+1][:-1]))
        i += 2
    print(hz_tuples)
        
test("1,1,1,1,1,1,1,1")