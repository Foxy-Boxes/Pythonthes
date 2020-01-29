import sys, resource
resource.setrlimit(resource.RLIMIT_STACK, (2**29,-1))
sys.setrecursionlimit(10**6)
def checkthestars(lst):
    row_len=len(lst[0])
    where=[(row_len,len(lst))]
    for i,row in enumerate(lst):
        j_lst=[]
        if '-'*row_len !=row :
            for j,elem in enumerate(row):
                if elem == '*':
                    j_lst.append(j)
            where.append((i,j_lst))
    return where
def column_combine(lst1,lst2):
    if 1 in lst2:
        i=lst2.index(1)
        out_lst=lst1[:i]+ [1]+lst1[i+1:]
        return out_lst
    else:
        return lst1
def generation(where):
    generic_lst = [0]*where[0][1]
    out_lst=[generic_lst]*where[0][0]
    for t in where[1:]:
        column=generic_lst[:]
        column[t[0]]=1
        for j in t[1]:
            out_lst[j]=column_combine(out_lst[j],column)
    return out_lst
def rules(rule_lst):
    if rule_lst==[]:
        return []
    concerned_rule=rule_lst[0]
    rulesign=concerned_rule[1]
    ruleeffect=concerned_rule[3]
    rulenum=int(concerned_rule[2])
    if concerned_rule[0]=='*':
        if rulesign=='=':
            def f(a,b):
                if b==1:
                    if a==rulenum:
                        if ruleeffect =='*':
                            return 1
                        else:
                            return 0
                    else:
                        return -1
                else:
                    return -1
            return [f]+rules(rule_lst[1:])
        elif rulesign=='>': 
            def f(a,b):
                if b==1:
                    if a > rulenum:
                        if ruleeffect =='*':
                            return 1
                        else:
                            return 0
                    else:
                        return -1
                else:
                    return -1
            return [f]+rules(rule_lst[1:])
        else:
            def f(a,b):
                if b==1:
                    if a < rulenum:
                        if ruleeffect =='*':
                            return 1
                        else:
                            return 0
                    else:
                        return -1
                else:
                    return -1
            return [f]+rules(rule_lst[1:])
    else: 
        if rulesign=='=':
            def f(a,b):
                if b==0:
                    if a==rulenum:
                        if ruleeffect =='*':
                            return 1
                        else:
                            return 0
                    else:
                        return -1
                else:
                    return -1
            return [f]+rules(rule_lst[1:])
        elif rulesign=='>': 
            def f(a,b):
                if b==0:
                    if a > rulenum:
                        if ruleeffect =='*':
                            return 1
                        else:
                            return 0
                    else:
                        return -1
                else:
                    return -1
            return [f]+rules(rule_lst[1:])
        else:
            def f(a,b):
                if b==0:
                    if a < rulenum:
                        if ruleeffect =='*':
                            return 1
                        else:
                            return 0
                    else:
                        return -1
                else:
                    return -1
            return [f]+rules(rule_lst[1:])
def neighbour(gen):
    row_length=len(gen)
    generic_lst = [0]*row_length
    col_length=len(gen[0])
    out_lst = [generic_lst]*col_length
    for i,col in enumerate(gen):
        for j,elem in enumerate(col):
            if elem == 1:
                row = out_lst[j][:]
                row2 = out_lst[j][:]
                for col_index in range(j-1,j+2): 
                    if col_index >= 0 and col_index < col_length:
                        row = out_lst[col_index][:]
                        row2 = out_lst[col_index][:]
                        for row_index in range(i-1,i+2):
                            if row_index >= 0 and row_index < row_length:
                                row[row_index]+=1
                                if row_index==i:
                                    if i-1 >=0:
                                        row2[i-1]+=1
                                    if i+1 < row_length:
                                        row2[i+1]+=1
                            out_lst[col_index]=row
                            if col_index==j:
                                out_lst[j]=row2
    return out_lst
def applyrules(neighbour,gen,rule_lst):
    out_lst=[]
    for i,row in enumerate(neighbour):
        lst2=[]
        for j,elem in enumerate(row):
            lst=[]
            b=gen[j][i]
            for rule in rule_lst:
                lst.append(rule(elem,b))
            if lst==[-1]*len(rule_lst):
                lst2.append(b)
            elif 0 in lst:
                lst2.append(0)
            else:
                lst2.append(1)
        out_lst.append(lst2)
    return out_lst
def convert(lst):
    out_lst=[]
    for i,row in enumerate(lst):
        st=""
        for j,elem in enumerate(row):
            if elem == 0:
                st = st + '-'
            else:
                st = st + '*'
        out_lst.append(st)
    return out_lst
def printgen(lst):
    for i in lst:
        print i
def main():
    themap=sys.argv[1]
    rules_str=sys.argv[2]
    times=sys.argv[3]
    file1=open(themap,'r')
    map_lst=file1.read().split('\n')
    file1.close
    file2=open(rules_str,'r')
    rule_lst=file2.read().split('\n')
    file2.close
    if map_lst[-1]=="":
        map_lst=map_lst[:-1]
    if rule_lst[-1]=="":
        rule_lst=rule_lst[:-1]
    times = int(times)
    rules_functions=rules(rule_lst)
    def findthetargetgen(map_lst,rules_functions,times,the_next):
        if times ==0:
            return the_next
        else:
            gen=generation(checkthestars(map_lst))
            the_next=convert(applyrules(neighbour(gen),gen,rules_functions))
            return findthetargetgen(the_next,rules_functions,times-1,the_next)
    printgen(findthetargetgen(map_lst,rules_functions,times,map_lst))

main()    
