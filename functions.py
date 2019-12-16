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

def commafy (str_to_comma):
    res = ''
    for i in str_to_comma:
        res = res + i + ','
    res = res[:-1]
    return res
