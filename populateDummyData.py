import dbUtils

#addPerson( name, lat, lng, phone, isVictim )
#Add Victims:
def addVictims():
    dbUtils.addPerson("George", 39.951426, -75.179021, 1111111111, True)
    dbUtils.addPerson("Andrew", 39.947597, -75.180811, 1111111111, True)
    dbUtils.addPerson("Kevin", 39.943159, -75.176001, 1111111111, True)
    dbUtils.addPerson("John", 39.945502, -75.166682, 1111111111, True)
    dbUtils.addPerson("Jack", 39.970261, -75.178528, 1111111111, True)
    dbUtils.addPerson("Brandon", 39.935787, -75.220462, 1111111111, True)
    dbUtils.addPerson("Rigved", 39.909964, -75.175217, 1111111111, True)
    dbUtils.addPerson("Tejas", 39.951850, -75.236655, 1111111111, True)
    dbUtils.addPerson("Muthukrishnamurthiswami Venkatamurthi AKA Muthu", 39.950534, -75.202796, 1111111111, True)
    dbUtils.addPerson("Alexa", 39.938901, -75.182731, 1111111111, True)
    print("Added Victims!")


#Add First Responders:
def addFirstResponder():
    dbUtils.addPerson("Harrison", 39.967382, -75.194042, 1111111111, False)
    print("Added First Responders")


