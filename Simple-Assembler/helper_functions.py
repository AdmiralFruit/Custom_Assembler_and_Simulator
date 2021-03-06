from general_consts import *
from register_and_type_constants import *
from validity_checker import *


def getRegisterEncoding(register):
    """Returns Register Encoding"""
    return register_to_encoding[register]


def getRegisterCount(type):
    """Returns Register Count"""
    return type_to_reg_no[type]


def isVarValid(var_declared,var_called,alphanum,inst):
    """Checks if Variables are Valid"""
    numarr = ['0','1','2','3','4','5','6','7','8','9']
    inst2 = inst.copy()
    inst2.append('var')
    len1 = len(var_declared)
    for i in var_declared:
        if i[1]!=1:
            return (-1,i[1])
        if i[1]==1:
            a = i[0]
            b = len(a)
            count = 0
            count2 = 0
            for j in a:
                if j in alphanum:
                    count+=1
                if j in numarr:
                    count2+=1
            if count!=b:
                return (-2,i[0])
            if b==count2:
                return (-5,i[0])
    b2 = len(var_called)
    var2 = []
    for i in var_declared:
        var2.append(i[0])
    for i in var2:
        if i in inst2:
            return (-4,i)
    
    for i in var_called:
        if i not in var2:
            return (-3,i)
            
    return (0,0) #no issues all variables declared and called are valid


def isLabelValid(lbl_called,lbl_declared,lbl_inst,inst,alphanum,lbl_declared2,var_declared2): #add in main
    """Checks if Labels are Valid"""
    numarr = ['0','1','2','3','4','5','6','7','8','9']
    inst2 = inst.copy()
    inst2.append('var')
    l1 = len(lbl_declared)
    l2 = len(lbl_inst)
    if l1!=l2:
        return (-5,0)
    count2 = 0
    for i in lbl_declared:
        a = i[0]
        b = len(a)
        count = 0
        count4 = 0
        for j in a:
            if j in alphanum:
                count+=1
            if j in numarr:
                count4+=1
        if count!=b:
            return (-1,i[1])
        if b==count4:
            return (-6,i[1])
        else:
            c = lbl_inst[count2]
            if isLineValid2(c)!=0 or lineTypesMatch(c,lbl_declared2,var_declared2)!=0:
                return (-2,i[1])
        count2+=1
    count3 = 0
    b2 = len(lbl_called)
    lbl2 = []
    for i in lbl_declared:
        lbl2.append(i[0])
    for i in lbl_called:
        if i not in lbl2:
            return (-3,i)     
    for i in lbl2:
        if i in inst2:
            return (-4,i)
    return (0,0)


def Duplication(lbl_declared,var_declared,lbl_declared2,var_declared2): #add in main
    """Checks if there are any Duplicate Labels or Variables"""
    a = len(lbl_declared)
    b = len(var_declared)
    for i in var_declared2:
        if i in lbl_declared2:
            return (-1,i)
    for i in range(0,a):
        a2 = lbl_declared[i][0]
        for j in range(i+1,a):
            if a2==lbl_declared[j][0]:
                return (-2,a2)
    for i in range(0,b):
        b2 = var_declared[i][0]
        for j in range(i+1,b):
            if b2==var_declared[j][0]:
                return (-3,var_declared[j][1])
    return (0,0)

    
def isLineValid(line_comp):
    """Checks if line is valid that is the instruction is valid and the size corresponds to the instruction"""
    if isInstructionValid(line_comp[0]) == False:
        return -1
    if isSizeRight(line_comp[0], line_comp) == False:
        return -2
    return 0

def isLineValid2(line_comp):
    """Checks if line is valid that is the instruction is valid and the size corresponds to the instruction"""
    if isInstructionValid2(line_comp[0]) == False:
        return -1
    if isSizeRight(line_comp[0], line_comp) == False:
        return -2
    return 0

def lineTypesMatch(line_comp,lbl_declared2,var_declared2):
    """Checks if the objects in the line match the objects which they were supposed to be i.e. registers
    are in place of registers in the syntax and so on"""
    temp = ""
    if line_comp[0]=="mov":
        if "$" in line_comp[-1]:
            temp = "movi"
        else:
            temp = "movr"
    else:
        temp = line_comp[0]
    ls_type_order = type_to_syntaxconstituents[OPcode_table[temp][-1]]
    for i in range(1, len(line_comp)):
        if ls_type_order[i] == 'Register':
            if isRegisterValid(line_comp[i]) is False:
                return -1
            if isRegisterValid(line_comp[i])==-1:
                if line_comp[0]!="movr":
                    return -4
        if ls_type_order[i] == 'Immediate':
            if isImmediateValid(line_comp[i]) is False:
                return -2
            if isImmediateRangeValid(line_comp[i]) is False:
                return -3
        if ls_type_order[i] == 'Memory Address': #start from here
            if line_comp[0]=='ld' or line_comp[0]=='st':
                if line_comp[-1] not in var_declared2:
                    if line_comp[-1] in lbl_declared2: #illegal use
                        return -5
                    else:
                        return -6      
            if line_comp[0]=='jmp' or line_comp[0]=='jlt' or line_comp[0]=='jgt' or line_comp[0]=='je': 
                if line_comp[-1] not in lbl_declared2:
                    if line_comp[-1] in var_declared2: #illegal use
                        return -7
                    else:
                        return -8
                
                '''else:
                    if isLabelValid(lbl_called,lbl_declared,lbl_inst,inst,alphanum)!=0:
                        return -9'''
    return 0
