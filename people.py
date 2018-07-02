#!/bin/python
import os
import sys
import pdb

degree = "csm"
year = "ug2"
roles = "cohort"
finger = "Name"
path = "/afs/inf.ed.ac.uk/user/s16/s1630747/myapps/people/"
data = path + "data/"
p = "cd " + path + " && "
d = "cd " + data + " && "

def fetch(year):
    people = []
    for i in range (year * 100000, (year + 1) * 100000):
        s = os.popen("finger s" + str(i)).read()
        if finger in s:
            uun = "s" + str(i)
            people.append(uun)
    os.system(d + "touch raw/s" + str(year))
    f = open(data + "raw/s" + str(year), "w")
    for uun in people:
        f.write(uun + "\n")
    f.close()

def trim(year):
    people = []
    f = open(data + "raw/s" + year, "r")
    people = str.split(f.read())
    f.close
    trimmed = []
    for uun in people:
        if roles in os.popen("roles -v" + uun).read():
            trimmed.append(uun)
            print getName(uun)
    os.system(d + "touch grad/s" + str(year))
    f = open(data + "grad/s" + year, "w")
    for uun in trimmed:
        f.write(uun + "\n")
    f.close()

def merge():
    files = str.split(os.popen("ls " + data + "grad").read())
    s = " ".join(files)
    os.system("cd " + data + "grad && cat " + s + " > ../all")

def test(query, roles, primary, secondary):
    roles += " "
    primary += " "
    secondary += " "
    req = []
    opt = []
    neg = []
    p = []
    s = []

    for term in query:
        if "%" not in term:
            term += " "
        else:
            term = term.translate(None, "%")

        if "?" in term:
            opt.append(term.translate(None, "?"))
        elif "~" in term:
            neg.append(term.translate(None, "~"))
        elif "*" in term:
            p.append(term.translate(None, "*"))
        elif "." in term:
            s.append(term.translate(None, "."))
        else:
            req.append(term)

    reqTest = all(term in roles for term in req)
    optTest = len(opt) == 0 or not all(term not in roles for term in opt)
    negTest = all(term not in roles for term in neg)
    prmTest = all(term in primary for term in p)
    secTest = all(term in secondary for term in s)

    return reqTest and optTest and negTest and prmTest and secTest

def search(file, query):
    header = "File=" + file + "; Query: " + " ".join(query) + "\n"
    f = open(data + file, "r")
    people = f.readlines()
    f.close()
    results = []
    n = len(people)


    i = 0
    for person in people:
        uun = str.split(person)[0]
        if "s" != uun[0]: n -= 1 ; continue
        i += 1
        sys.stdout.write(uun + ": " + str(i) + "/" + str(n) + " "*20 + "\r")
        sys.stdout.flush()
        roles = str.split(os.popen("roles -v " + uun).read())
        primary = roles[roles.index("Primary") + 2 : roles.index("Secondary")]
        secondary = roles[roles.index("Secondary") + 3 :]
        roles = " ".join(roles)
        primary = " ".join(primary)
        secondary = " ".join(secondary)

        if test(query, roles, primary, secondary):
            name = getName(uun)
            results.append(name)
            print name

    f = open(data + "out", "w")
    f.write(header)
    for name in results:
        f.write(name + "\n")
    f.close()
    os.system(d + "less out")

def getName(uun):
    s = os.popen("finger " + uun).readlines()[0]
    s = str.split(s)[3:]
    s = str(uun) + " " + " ".join(s)
    return s

def archive(name):
    os.system(d + "mv out " + name)

def main():
    numArgs = len(sys.argv) - 1
    if numArgs < 1:
        return
    elif str(sys.argv[1]) == "s":
        search("all", sys.argv[2:])
    elif str(sys.argv[1]) == "sf" and numArgs > 2:
        search(str(sys.argv[2]),  sys.argv[3:])
    elif str(sys.argv[1]) == "fetch":
        for year in sys.argv[2:]:
            fetch(int(year))
    elif str(sys.argv[1]) == "trim":
        for year in sys.argv[2:]:
            trim(year)
    elif str(sys.argv[1]) == "merge":
        merge()
    elif str(sys.argv[1]) == "archive" and numArgs == 2:
        archive(str(sys.argv[2]))
    elif str(sys.argv[1]) == "view" and numArgs == 2:
        os.system(d + "less " + str(sys.argv[2]))
    elif str(sys.argv[1]) == "list":
        os.system(d + "ls")
    elif str(sys.argv[1]) == "del" and numArgs > 1:
        os.system(d + "rm " + " ".join(sys.argv[2:]))

main()
