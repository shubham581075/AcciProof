import json

def new_data():
    n=int(input("Enter the no. of HUBs :"))
    hub_name=[]
    hub_coords=[]
    hub_contact=[]

    for x in range(n):
        hub_name.append(input("\nHUB "+str(x+1)+" Name: "))
        coords=[]
        y=input("HUB "+str(x+1)+" Lat. and Log. :")
        la,lo=tuple(y.split(","))
        coords.append(float(la))
        coords.append(float(lo))
        hub_coords.append(coords)
        hub_contact.append(input("HUB "+str(x+1)+" Contact: "))

    hub_coords = tuple(zip(hub_name,hub_coords,hub_contact))

    for l,n in enumerate(hub_coords,1): #TO SHOW
        print(l,":",n)

    with open("hub_coords.json", mode='w') as outfile: #TO WRITE DATA
        json.dump(hub_coords, outfile)
    print("Recorded Successfully\n")

    check()

def update_add(data1):

    n=int(input("\nEnter the no. of HUBs to add:"))
    hub_name=[]
    hub_coords=[]
    hub_contact=[]

    for x in range(n):
        hub_name.append(input("\nHUB "+str(x+1)+" Name: "))
        coords=[]
        y=input("HUB "+str(x+1)+" Lat. and Log. :")
        la,lo=tuple(y.split(","))
        coords.append(float(la))
        coords.append(float(lo))
        hub_coords.append(coords)
        hub_contact.append(input("HUB "+str(x+1)+" Contact: "))

        hub_coords_new = list(zip(hub_name,hub_coords,hub_contact))
        data1.extend(hub_coords_new)

        for l,n in enumerate(data1,1):
            print(l,":",n)

        with open("hub_coords.json", mode='w') as outfile:
            json.dump(data1, outfile)

        print("Updated", x+1)

    print("All Updated Successfully\n")

    check()

def update_del(data1):

    l=input("\nEnter the index number to delete the HUB/HUBs, split it by ',' :")
    to_del=l.split(",")
    to_del.reverse()

    for l in to_del:
        data1.remove(data1[int(l)-1])


    with open("hub_coords.json", mode='w') as outfile:
        json.dump(data1, outfile)
    print("Updated Successfully\n")

    check()


def add_del(data1):
    o=input(''' 
 a.Add element
 b.Delete element

Enter the option: ''')
    if o=='a':
        update_add(data1)
    elif o=="b":
        update_del(data1)
    else:
        print("Invalid option")
        add_del(data1)


def check():
    with open("hub_coords.json", mode='r') as outfile:
        data1=json.load(outfile)

    for l,n in enumerate(data1,1):
        print(l,":",n)

    u=int(input(''' 
 1.Update Database
 2.New Database
 3.Exit

Enter the option: '''))
    if u==2:
        new_data()
    elif u==1:
        add_del(data1)
    elif u==3:
        input("Press Enter to Exit !!")
    else:
        print("Invalid option")
        check()



check()




