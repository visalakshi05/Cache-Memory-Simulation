from prettytable import PrettyTable
import math

print("\n\t\tCache Memory Simulation\n")

# Function to check if a value satisfies the log condition
def is_valid_log(value):
    try:
        log_value = math.log2(value)
        if log_value.is_integer():
            return True
        else:
            return False
    except ValueError:
        return False

# Function to check if log2 of a number is an integer
def is_power_of_two(n):
    return (n > 0) and (math.log2(n).is_integer())

# User inputs for memory and cache sizes with log checks
try:
    MS = int(input("Enter memory size:"))
    if not is_valid_log(MS):
        raise ValueError("Memory size must be a power of 2.")
    print("-" * 100)

    CS = int(input("Enter L1 cache size:"))
    if not is_valid_log(CS):
        raise ValueError("L1 cache size must be a power of 2.")
    print("-" * 100)

    CS1 = int(input("Enter victim cache size:"))
    if not is_valid_log(CS1):
        raise ValueError("Victim cache size must be a power of 2.")
    print("-" * 100)

    CS2 = int(input("Enter L2 cache size:"))
    if not is_valid_log(CS2):
        raise ValueError("L2 cache size must be a power of 2.")
    print("-" * 100)

    k = int(input("Enter number of ways for L2 cache:"))
    if not is_valid_log(k):
        raise ValueError("Number of ways for L2 cache must be a power of 2.")
    print("-" * 100)

    BS = int(input("Enter block size:"))
    if not is_valid_log(BS):
        raise ValueError("Block size must be a power of 2.")
    print("-" * 100)
    
     # Calculate various parameters based on user inputs
    NB = int(MS / BS)      
    NL = int(CS / BS)
    NL1 = int(CS1 / BS)
    NL2 = int(CS2 / BS)
    NS = int(NL / k)

    # Internal log checks for derived values
    if not is_valid_log(BS):
        raise ValueError("Block size (BS) must be a power of 2.")
    
    if not is_valid_log(NB):
        raise ValueError("Number of blocks (NB) derived from memory size must be a power of 2.")
    
    if not is_valid_log(NL):
        raise ValueError("Number of lines (NL) in L1 cache must be a power of 2.")
    
    if not is_valid_log(NS):
        raise ValueError(f"Number of sets (NS) in L2 cache must be a power of 2.")

    # Calculate index sizes
    BO = int(math.log2(BS))
    BI = int(math.log2(NB))
    CI = int(math.log2(NL))
    SI = int(math.log2(NS))
    PA = int(math.log2(MS))
    
    # Additional check to ensure valid powers of 2 for the calculations
    if not (is_power_of_two(BO) and is_power_of_two(BI) and is_power_of_two(CI) and is_power_of_two(SI) and is_power_of_two(PA)):
        raise ValueError("Error in internal calculations: One or more derived values are not valid powers of 2.")
    
except ValueError as e:
    print(f"Error: {e}")
    exit()

#Tag bit calculation
TB=BI-CI
TB1=BI
TB2=BI-SI

# Convert decimal to binary
def decimal_to_binary(n,binary):
    if n == 0:
        return binary
    else:
        binary= str(n % 2)+binary
        return decimal_to_binary(n//2,binary)
    
# Pad binary representation to a specific length
def pad_binary(binary_str, target_length):
    return binary_str.zfill(target_length)

# Initialize cache dictionaries
d={}   #L1 
d1={}  #Victim
d2={}  #L2

# Initialize L1 cache
for i in range(NL):
    temp=str(decimal_to_binary(i,""))
    temp1 = pad_binary(temp, CI)
    d[temp1]=[0,'',0]            # Valid,Tag,Dirty bit

# Initialize Victim cache
for i in range(NL1):
    d1[i]=[0,'',0]     # Valid,Tag,Frequency

# Initialize L2 cache
for i in range(NS):
    temp=str(decimal_to_binary(i,""))
    temp2=0
    temp_d={}
    temp1 = pad_binary(temp, SI)

    for i in range(k):
        temp_d[str(temp2)]=[0,'',0,0]   # Valid, Tag, Dirty bit, Frequency
        temp2+=1
    d2[temp1]=temp_d

# Function to print L1 cache
def print_DM(c): 

    print("\nL1 cache:")
    ind=[]
    val=[]
    tag=[]
    dir=[]
    for i in c:
        ind.append(i)
        val.append(c[i][0])
        tag.append(c[i][1])
        dir.append(c[i][2])
    columns=['Index','Valid','Tag','Dirty']
    table=PrettyTable()
    table.add_column(columns[0],ind)
    table.add_column(columns[1],val)
    table.add_column(columns[2],tag)
    table.add_column(columns[3],dir)
    print(table)

# Function to print victim cache
def print_V(c):
    print("\nVictim cache:")
    ind=[]
    val=[]
    tag=[]
    freq=[]
    for i in c:
        ind.append(i)
        val.append(c[i][0])
        tag.append(c[i][1])
        freq.append(c[i][2])
    columns=['Index','Valid','Tag','Frequency']
    table=PrettyTable()
    table.add_column(columns[0],ind)
    table.add_column(columns[1],val)
    table.add_column(columns[2],tag)
    table.add_column(columns[3],freq)
    print(table)
    
# Function to print L2 cache
def print_L2(c):
    print("\nL2 cache:")
    ind=[]
    val=[]
    tag=[]
    dir=[]
    freq=[]
    si=[]
    for j in c:
        for i in c[j]:
            ind.append(i)
            val.append(c[j][i][0])
            tag.append(c[j][i][1])
            dir.append(c[j][i][2])
            freq.append(c[j][i][3])
            if(j not in si):
                si.append(j)
            else:
                si.append('')
    columns=['Set index','Index','Valid','Tag','Dirty','Frequency']
    table=PrettyTable()
    table.add_column(columns[0],si)
    table.add_column(columns[1],ind)
    table.add_column(columns[2],val)
    table.add_column(columns[3],tag)
    table.add_column(columns[4],dir)
    table.add_column(columns[5],freq)
    print(table)

#Fetch from Main memory 
def fetch_from_main_memory():
    print("Fetching from Main Memory")

# K-way Set Associative cache function with L2 cache
def L2(ch,d2,loc):
    if ch==1:    # Load operation
        min=k
        delete=''
        flag=0
        update=''
        for i in d2[loc[TB2:TB2+SI]]:    # Cache hit
            if d2[loc[TB2:TB2+SI]][i][1]==loc[0:TB2]:
                print("\nL2 cache: Hit!! From L2 cache -> Sending it to L1 cache")
                print("-"*100)
                delete=''
                update=i
                break
            if d2[loc[TB2:TB2+SI]][i][1]=='' and flag==0:   # Empty entry found
                delete=i
                flag=1
            if min>d2[loc[TB2:TB2+SI]][i][3] and flag==0:   # Find least frequently used entry
                min=d2[loc[TB2:TB2+SI]][i][3]
                delete=i
        if delete!='':   # Cache miss
            print("\nL2 cache: Miss!!")
            print("-"*100)
            fetch_from_main_memory()
            print("-"*100)
            d2[loc[TB2:TB2+SI]][delete][1]=loc[0:TB2]   
            d2[loc[TB2:TB2+SI]][delete][2]=0
            update=delete
        d2[loc[TB2:TB2+SI]][update][0]=1
        d2[loc[TB2:TB2+SI]][update][1]=loc[0:TB2]
        d2[loc[TB2:TB2+SI]][update][3]=k
        for i in d2[loc[TB2:TB2+SI]]:
            if d2[loc[TB2:TB2+SI]][i][1]!=loc[0:TB2] and d2[loc[TB2:TB2+SI]][i][3]>0:
                d2[loc[TB2:TB2+SI]][i][3]=d2[loc[TB2:TB2+SI]][i][3]-1   # Decrement frequency for others
        
    elif ch==2:   # Store operation
        min=k
        delete=''
        flag=0
        update=''
        for i in d2[loc[TB2:TB2+SI]]:
            if d2[loc[TB2:TB2+SI]][i][1]==loc[0:TB2]:   # Cache hit
                print("\nL2 cache: Hitt!! Found and updated with previous value in L2 cache")
                print("-"*100)
                if(d2[loc[TB2:TB2+SI]][i][2]==1):    # If dirty bit is set
                    print("\nL2 cache: Storing the before value in MM")
                    print("-"*100)
                d2[loc[TB2:TB2+SI]][i][2]=1
                delete=''
                update=i
                break
            if d2[loc[TB2:TB2+SI]][i][1]=='' and flag==0:  # Empty entry found
                delete=i
                flag=1
            if min>d2[loc[TB2:TB2+SI]][i][3] and flag==0:  # Find least frequently used entry
                min=d2[loc[TB2:TB2+SI]][i][3]
                delete=i
                if(d2[loc[TB2:TB2+SI]][i][2]==1):
                    print("\nL2 cache: Storing the before value in MM")
                    print("-"*100)
                d2[loc[TB2:TB2+SI]][delete][2]=1
        if delete!='':  # Cache miss
            d2[loc[TB2:TB2+SI]][delete][1]=loc[0:TB2]
            update=delete
        d2[loc[TB2:TB2+SI]][update][0]=1
        d2[loc[TB2:TB2+SI]][update][1]=loc[0:TB2]
        d2[loc[TB2:TB2+SI]][update][3]=k
        for i in d2[loc[TB2:TB2+SI]]:
            if d2[loc[TB2:TB2+SI]][i][1]!=loc[0:TB2] and d2[loc[TB2:TB2+SI]][i][3]>0:
                d2[loc[TB2:TB2+SI]][i][3]=d2[loc[TB2:TB2+SI]][i][3]-1     # Decrement frequency for others       
    else:
        print("Enter valid choice")

    return d2

# Fully Associative cache function with victim cache
def Victim(ch,d1,loc,d2):
    if ch==1:   # Load operation
        min=NL1
        delete=''
        flag=0
        update=''
        for i in d1:
            if d1[i][1]==loc[0:TB1]:   #Cache hit
                print("\nVictim cache: Hit!! From vicitm cache->Sending it to L1 cache")
                print("-"*100)
                delete=''
                update=i
                break
        else:   #Cache miss
            print("\nVictim cache: Miss!! Finding it in L2 cache")
            print("-"*100)
            d2=L2(ch,d2,loc)
    elif ch==2:  # Store operation
        min=NL1
        delete=''
        flag=0
        update=''
        for i in d1:
            if d1[i][1]==loc[0:TB1]:   # Cache hit
                delete=''
                update=i
                break
            if d1[i][1]=='' and flag==0:   # Empty entry found
                delete=i
                flag=1
            if min>d1[i][2] and flag==0:   # Find least frequently used entry
                min=d1[i][2]
                delete=i
        if delete!='':   # Cache miss
            d1[delete][1]=loc[0:TB1]
            update=delete
        d1[update][0]=1
        d1[update][1]=loc[0:TB1]
        d1[update][2]=NL1
        for i in d1:
            if d1[i][1]!=loc[0:TB1] and d1[i][2]>0:
                d1[i][2]=d1[i][2]-1
        print("\nVictim cache: Updating with replaced value in victim cache")
        print("-"*100)
    else:
        print("Enter valid choice")
    return d1

# Direct-mapped cache function with L1 cache
def DM(ch,d,loc,d1,d2):
    if ch==1:   # Load operation
        if(d[loc[TB:TB+CI]][0]==0):   # Cache miss
            print("\nL1 cache: Miss !! Have to check from victim cache")
            print("-"*100)
            d1=Victim(ch,d1,loc,d2)
            d[loc[TB:TB+CI]][0]=1
            d[loc[TB:TB+CI]][1]=loc[0:TB]
        else:  
            if(d[loc[TB:TB+CI]][1]==loc[0:TB]):  # Cache hit
                print("\nL1 cache: Hit!! Found in L1 cache")
                print("-"*100)
                if(d[loc[TB:TB+CI]][2]==1):   # Check dirty bit
                    print("\nL1 cache: Storing the before value in L2 cache")
                    print("-"*100)
                    d2=L2(ch,d2,str(d[loc[TB:TB+CI]][1]+loc[TB:TB+CI]))
            else:
                print("\nL1 cache: Miss!! Have to check from Victim cache")
                print("-"*100)
                d1=Victim(ch,d1,loc,d2)
                #d1=Victim(2,d1,str(d[loc[TB:TB+CI]][1]+loc[TB:TB+CI]),d2)
            d[loc[TB:TB+CI]][1]=loc[0:TB]
        d[loc[TB:TB+CI]][2]=0
    elif ch==2:   # Store operation
        if(d[loc[TB:TB+CI]][0]==0):   # Cache miss
            print("\nL1 cache: Miss!! Storing it in cache memory")
            print("-"*100)
            d[loc[TB:TB+CI]][0]=1
            d[loc[TB:TB+CI]][1]=loc[0:TB]
        else:
            if(d[loc[TB:TB+CI]][1]==loc[0:TB]):   # Cache hit
                print("\nL1 cache: Hit !! Updated new value in L1 cache")
                print("-"*100)
                d2=L2(ch,d2,loc)
            else:
                print("\nL1 cache: Miss !! New tag bit!,Storing it in cache memory")
                print("-"*100)
                if(d[loc[TB:TB+CI]][2]==1):   # Check dirty bit
                    print("\nL1 cache: Storing the before value in L2 cache")
                    print("-"*100)
                    d2=L2(ch,d2,str(d[loc[TB:TB+CI]][1]+loc[TB:TB+CI]))
                d1=Victim(ch,d1,str(d[loc[TB:TB+CI]][1]+loc[TB:TB+CI]),d2)
            d[loc[TB:TB+CI]][1]=loc[0:TB]
        d[loc[TB:TB+CI]][2]=1
    else:
        print("Enter valid choice")
    return d

# Main function to simulate memory operations
def main(d,d1,d2):
    while(1):
        add=int(input("\nEnter address: "))
        print("-"*100)
        loc=''
        
        # Convert the address into binary index and offset
        BI_add=str(decimal_to_binary(add//BS,""))
        BO_add=str(decimal_to_binary(add%BS,""))
        if(len(BI_add)==BI):
            loc+=BI_add
        else:
            for i in range(BI-len(BI_add)):
                loc+='0'
            loc+=BI_add
        if(len(BO_add)==BO):
            loc+=BO_add
        else:
            for i in range(BO-len(BO_add)):
                loc+='0'
            loc+=BO_add
        print("\nBinary value of address:",loc)

        los=int(input("\nChoice\n1.Load\n2.Store\nEnter your choice:"))
        d=DM(los,d,loc,d1,d2)
        
        #Print states of cache
        print_DM(d)
        print_V(d1)
        print_L2(d2)
        
        flag=input("\nDo u want to continue?(1/0)")
        if(flag=='0'): # Exit if user chooses 0
            break

# Input validation before starting the simulation
if MS < BS or CS % BS != 0 or CS1 % BS != 0 or CS2 % BS != 0:
    print("Invalid inputs: Cache or memory sizes must be divisible by block size.")
elif MS<=CS or MS<=CS1 or MS<=CS2:
    print("Invalid inputs: Main memory size is less.")
elif CS1>=CS or CS1>=CS2 or CS>=CS2:
    print("Invalid inputs: Cache size hierarchy is incorrect.")
elif PA!=BI+BO:
    print("Invalid input: Physical address bits mismatch.")
else:
    #Print initial state
    print_DM(d)
    print_V(d1)
    print_L2(d2)
    #Start stimulation
    main(d,d1,d2)