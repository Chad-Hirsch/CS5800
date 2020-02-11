 #CHAD HIRSCH
 #CS5800

 #get the file name of test NFA
filename = input("Please enter the name of test file: ")

 #reading test file all at once
test = open(filename + ".txt").read()
test = test.split("\n") #creating list according to lines

#get the starting state
start_state = test[0]

#get the accepting state
accept = test[1]
accept = accept.split(",") #if there are more than on eaccepting state

same = False #if start state and accepting state are both same
multi = False #if there are more than on accepting state
many = False #if starting state is one of the accepting state

if len(accept) == 1:
    same = start_state in accept

else:
    many = start_state in accept
    multi = True

#removing first two lines (starting and accepting states)
test = test[2:]

#dictionary to keep record of all the transitions
transitions = {}

for i in test:
    a = i.split(",")
    b = a[0] + "," + a[2]
    if b in transitions:
        transitions[b] = transitions[b] + "U" + a[1] #take the union of transitions between two same states
    else:
        transitions[b] = a[1]

#repeat untill only remaining states are starting and accepting state
while len(transitions) > 1:
    del_state = "" #keep record of which state is being deleted
    del_seleceted = False #flag to track if deleting state has been selected

    trans = {} #keep all the required transition in one place

    to = {} #keep all the transition between j and i states
    fro = {} #keep all the transitions between i and k states

    state_ii = "" #save the transition between i and i

    #loop to decide which state should be deleted
    #and then separate all the transitions related to that state
    for i in transitions:
        a = i.split(",")

        #if we haven't selected any state yet
        if(not del_seleceted):

            #if first state is not accepting or starting state
            #select it as a deleting state and add the rule to the appropriate dict
            if a[0] != start_state and a[0] not in accept:
                del_state = a[0]
                del_seleceted = True
                fro[i] = transitions[i]
                print(del_state)
            
            #if second state is not accepting or starting state
            #select it as a deleting state and add the rule to the appropriate dict
            elif a[1] != start_state and a[1] not in accept:
                del_state = a[1]
                del_seleceted = True
                to[i] = transitions[i]
                print(del_state)
            
            #add the selected rule to the trans dict, so that we can remove it from our mane dict
            if (del_seleceted):
                trans[i] = transitions[i]

        #if we have selected the deleting state
        else:

            #if the rule is for i to i, then add it as a star rule
            if a[0] == del_state and a[1] == del_state:
                state_ii = "(" + transitions[i] + ")*" #converting it to the star rule
                trans[i] = transitions[i]

            #if the rule represents i to k, add to appropriate dict
            elif a[0] == del_state:
                fro[i] = transitions[i]
                trans[i] = transitions[i]
            
            #if the rule represents j to i, add to appropriate dict
            elif a[1] == del_state:
                to[i] = transitions[i]
                trans[i] = transitions[i]

    #remove selected rules from the main dict
    [transitions.pop(x) for x in trans]

    #adding new transition between j and k states
    for j in to:
        for k in fro:
            a = j.split(",")[0] + "," + k.split(",")[1]
            b = to[j] + state_ii + fro[k]
            if a in transitions:
                transitions[a] = transitions[a] + "U" + b #Union if more than one transition is available for i and j
            else:
                transitions[a] = b

    if len(transitions) <= 4:
        keys = list(transitions.keys())
        end = False #flag to check if we only have start and accepting state left

        if multi:
            if len(accept) == 2 and many:
                s_a = start_state + "," + accept[1] #start to accept transition
                a_s = accept[1] + "," + start_state #accept to start loop
                a_a = accept[1] + "," + accept[1] #accept to accept loop

            s_s = start_state + "," + start_state #start to start loop

            #merging the final transitions to one main transition to get the regex

            #if there are 4 transitions: start self loop, start to accept, accept self loop, and accept to start
            if len(transitions) == 4 and s_a in keys and s_s in keys and a_s in keys and a_a in keys:
                b = "((({0})U({1})({3})*({2}))*(({1})U(({1})({3})({2}))*))*".format(transitions[s_s], transitions[s_a], transitions[a_s], \
                    transitions[a_a])
                end = True
            
            #if there are 2 transitions: self loop, and start to accept
            elif len(transitions) == 2 and s_s in keys and s_a in keys:
                b = "(({0})U({0})({1})U({1}))*".format(transitions[s_s], transitions[s_a])
                end = True
            
            #if there are 2 transitions: start to accept, and accept to start
            elif len(transitions) == 2 and s_a in keys and a_s in keys:
                b = "({0}U(({0})({1}))*)*".format(transitions[s_a], transitions[a_s])
                end = True


        if not multi:
            s_a = start_state + "," + accept[0] #start to accept transition
            s_s = start_state + "," + start_state #start to start loop
            a_s = accept[0] + "," + start_state #accept to start loop

            #merging the final transitions to one main transition to get the regex

            #if there are 3 transitions: self loop, start to accept, and accept to start
            if len(transitions) == 3 and s_a in keys and s_s in keys and a_s in keys:
                b = "({0})*({1})(({2})({0})*({1}))*".format(transitions[s_s], transitions[s_a], transitions[a_s])
                end = True
            
            #if there are 2 transitions: self loop, and start to accept
            elif len(transitions) == 2 and s_s in keys and s_a in keys:
                b = "({0})*({1})".format(transitions[s_s], transitions[s_a])
                end = True
            
            #if there are 2 transitions: start to accept, and accept to start
            elif len(transitions) == 2 and s_a in keys and a_s in keys:
                b = "({0})(({1})({0}))*".format(transitions[s_a], transitions[a_s])
                end = True

        #remove every other transition, and add final regex
        if end:
            transitions = {}
            transitions[s_a] = b


#print the regex
if same:
    print("(" + transitions[next(iter(transitions))] + ")*") #if starting and final state is same, then return the kleene star
else:
    print(transitions[next(iter(transitions))])