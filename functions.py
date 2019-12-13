def group (name,groupby):
    args=[]
    if (len(name)%groupby != 0):
        return name
    for i in range (0,len(name)-groupby+1,groupby):
        temp = []
        for j in range (0,groupby):
            temp.append(name[i+j])
        args.append(temp)
    return args