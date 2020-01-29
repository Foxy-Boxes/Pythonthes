class Node:
    def __init__(self,name,parent=None,children=None,cup=None):
        self.__name=name
        self.__parent=parent
        if children is None:
            self.__children=[]
            if cup:
                self.__maxopen=cup
            else:
                self.__maxopen=-1
        else:
            self.__children=children
            self.set_maxopen()
        self.__cup=cup
    def set_maxopen(self):
        maxofchildren=0
        for child in self.__children:
            if child.get_maxopen() > maxofchildren:
                maxofchildren = child.get_maxopen()
            self.__maxopen = maxofchildren
    def add_parent(self, parent=None):
        self.__parent=parent
    def add_child(self, child=None):
        self.__children.append(child)
    def add_cup(self, cup):
        self.__maxopen=cup
        self.__cup=cup
    def has_parent(self):
        if self.__parent:
            return True
        return False
    def has_child(self):
        if self.__children:
            return True
        return False
    def get_parent(self):
        return self.__parent
    def get_cup(self):
        return cup
    def get_maxopen(self):
        return self.__maxopen
def get_datum(tree):
    return tree[0]
def children(tree):
    forest=tree[1:]
    if type(forest[0])==int:
        return []
    return tree[1:]
def nodify_tree(tree,lst):
    OutList=lst
    List=[]
    if tree != []:
        List.append(get_datum(tree))
        children_list=[]
        forest=children(tree)
        for e in forest:
            children_list.append(e[0])
        List.append(children_list)
        OutList.append(List)
        if forest != []:
            OutList=nodify_forest(forest,OutList)
    return OutList
def nodify_forest(forest,lst):
    if forest != []:
        OutList=lst
        for e in forest:
            OutList=nodify_tree(e,OutList)
        return OutList
    else:
        return lst
def get_cups(tree,result):
    a=result
    check=True
    if tree!=[]:
        for e in tree[1:]:
            if type(e)==list:
                if len(e)==2 and type(e[1])==int:
                    a.update({e[0]:e[1]})
                else:
                    a.update(get_cups(e,a))
        else:       
            return a
def trav(lst):
    out_lst=[lst[0][0]]
    for elem in lst:
        out_lst.extend(elem[1])
    return out_lst


def chalchiuhtlicue(tree):
    lst=nodify_tree(tree,[])
    if len(tree)==2 and type(tree[1])==int:
        outlst=[[]]*(tree[1]-1)+[[tree[0]]]
        return outlst
    Dict={}
    for elem in lst:
        Dict[elem[0]]=Node(elem[0])
    cups_dict=get_cups(tree,{})
    for key in cups_dict:
        Dict[key].add_cup(cups_dict[key])
    for elem in lst:
        for children in elem[1:]:
            for child in children:
                Dict[elem[0]].add_child(Dict[child])
                Dict[child].add_parent(elem[0])
    for elem in lst[::-1]:
        Dict[elem[0]].set_maxopen()
    priority=trav(lst)[::-1]
    lst_tosort=[]
    for elem in priority:
        lst_tosort.append((elem,Dict[elem].get_maxopen()))
    swap=True
    while swap:
        swap=False
        for i in range(len(lst_tosort)-1):
            if lst_tosort[i][1] > lst_tosort[i+1][1]:
                lst_tosort[i],lst_tosort[i+1]=lst_tosort[i+1],lst_tosort[i]
                swap=True
    lst_toclose=close2(lst_tosort,Dict)
    return process_closing(lst_toclose)
def process_closing(lst):
    pro_lst=[lst[0]]
    for i in range(1,len(lst)):
        if lst[i-1]!=lst[i]:
            pro_lst.append(lst[i])
    new_lst=[[]]*(pro_lst[-1][1]-1)+[[pro_lst[-1][0]]]
    for elem in pro_lst[:-1]:
        if len(new_lst[elem[1]-1])==0:
            new_lst[elem[1]-1]=[elem[0]]
        else:
            if elem[0] not in new_lst[elem[1]-1]:
                new_lst[elem[1]-1].append(elem[0])
    return new_lst
def close2(lst,Dict):
    lst_toclose=lst
    for i in range(len(lst_toclose)):
        condition=True
        while condition:
            parent=Dict[lst_toclose[i][0]].get_parent()
            if parent is not None:
                condition=(Dict[parent].get_maxopen()==lst_toclose[i][1])
                if condition:
                    lst_toclose[i]=(parent,lst_toclose[i][1])
            else:
                condition=False
    return lst_toclose
