


def getmail():
    gm = 0
    hm = 0
    fm_list = []
    with open("/Users/craigvandeputte/pyscripts/working/addresses.csv") as add:
        for x in add:
            FirstMail = x.strip().split("@")
            fm_list.append(FirstMail[0]) 
            if FirstMail[1] == "gmail.com":
                gm+=1
            if FirstMail[1] == "hotmail.com":
                hm+=1 
        print("There are",gm,"gmail addresses")
        print("There are",hm,"hotmail addresses")
    return print(fm_list)

getmail()
        



