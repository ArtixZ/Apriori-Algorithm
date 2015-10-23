from __future__ import division
import re
import copy

def Apriori(Str):
    SupportTresh=float(raw_input('Please input support threshold(0-1):'))
    ConffidenceTresh=float(raw_input('Please input confidence treshold(0-1):'))
    ############
    with open(Str,'r') as f:
        TransactionList=f.readlines()
    NumOfTransaction=len(TransactionList)
    Transactions=[]
    Dict={}
    Elements=[]
    L=[]
    for line in TransactionList:
        RefinedLine=re.sub(r'T\d{1,5}',"",line).strip()
        ItemsOfLine=RefinedLine.split(',')
        Transactions.append(ItemsOfLine)
        for key in ItemsOfLine:
            if Dict.has_key(tuple([key])):
                Dict[tuple([key])]+=1
            else:
                Dict[tuple([key])]=1
    # print Transactions
    # print Dict
     ##############
    Keys=[]
    for key in Dict:
        if Dict[key]/NumOfTransaction<SupportTresh:
            Keys.append(key)
    for key in Keys:
        del Dict[key]
    L.append(Dict)

    for key in L[0]:
        Elements.append(key)
    ################ data import and cleaning. done
    # print L
    # print Elements
    # print Transactions
    k=0

    while(1):

        if L[k]:
            L.append({})
            for TupleKey in L[k]:
                for key in Elements:

                    if not set(list(key))&set(list(TupleKey)):
                        TempTuple=TupleKey+key
                        # print TempTuple
                        if TempTuple not in L[k+1]:
                            L[k+1][TempTuple]=0
            TempSetList=[]
            TempList=[]
            for key in L[k+1]:  #delect duplications: A,B=B,A
                if set(key) in TempSetList and key not in TempList:
                    TempList.append(key)
                elif set(key) not in TempSetList:
                    TempSetList.append(set(key))

            # print TempSetList
            # print L[k+1]
            # print TempList
            for key in TempList:
                del L[k+1][key]
            # print L[k+1]

            k+=1
            for TansLine in Transactions:
                for LKey in L[k]:
                    if set(list(LKey))<=set(TansLine):
                        L[k][LKey]+=1
            # print L[k]
            Keys=[]
            for key in L[k]:
                if L[k][key]/NumOfTransaction<SupportTresh:
                    Keys.append(key)
            for key in Keys:
                del L[k][key]
            # print k,L[k]
        else:
            break
    del L[k]
    # print L
    print '\nFrequent itemsets and frequence:'
    for key1 in L:
        for key2 in key1:
            print key2,':',key1[key2]
    print '\n*************************************************************************\n'
    # del L[0]
    # print L

    TempList=[]
    LL=[]
    TempSetList=[]
    for key1 in L:
        for key2 in key1:
            for key3 in key2:
                if (set(list(key2))-set(list(tuple([key3])))):
                    # print key2,key3
                    LL.append([[key3],list(set(list(key2))-set(list(tuple([key3]))))])
                    TempSetList.append(set(key3))
    # print LL
    for key1 in LL:
        if len(key1[1])>1:
            for key2 in key1[1]:
                tempkey=copy.deepcopy(key1)
                tempkey[0].append(key2)
                tempkey[1].remove(key2)
                if set(tempkey[0]) not in TempSetList:
                    LL.append(tempkey)
                    TempSetList.append(set(tempkey[0]))
    # print LL
    # print L
    print'Generated association rules(and their Support and Confidence):'
    for key1 in LL:
        for key2 in L:
            for key3 in key2:
                # print key2
                if set(list(key3))==set(key1[0]):
                    FirstInt=key2[key3]
                    # print(FirstInt)
                if set(list(key3))==set(key1[0]+key1[1]):
                    TotalInt=key2[key3]
                    # print(TotalInt)
        if TotalInt/FirstInt>=ConffidenceTresh:
            print key1[0],'-->',key1[1],'(',TotalInt/NumOfTransaction,TotalInt/FirstInt,')'
###########
while(1):
    print '\n==========================================================================================================\n'
    print '1  Amazon'
    print '2  Kmart'
    print '3  Nike'
    print '4  Walmart'
    print '5  Foot locker'
    Selection=raw_input('Please select a merchant you want to know(0 to exit):')
    if Selection=='1':
        Apriori('Amazon.txt')
    elif Selection=='2':
        Apriori('Kmart.txt')
    elif Selection=='3':
        Apriori('Nike.txt')
    elif Selection=='4':
        Apriori('Walmart.txt')
    elif Selection=='5':
        Apriori('Foot locker.txt')
    elif Selection=='0':
        break
    else:
        print'Wrong Number. Please select again.'