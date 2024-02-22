#--------------------------------------------------#
#   ╭╮╱╱╭━━━┳╮╱╱╭━━╮╭━━━┳━━━╮╭╮╱╭╮╱╱╱╱╱╭╮
#   ┃┃╱╱┃╭━╮┃┃╱╱┃╭╮┃┃╭━╮┃╭━╮┃┃┃╱┃┃╱╱╱╱╭╯╰╮
#   ┃┃╱╱┃┃╱┃┃┃╱╱┃╰╯╰┫┃╱┃┃╰━━╮┃╰━╯┣╮╭┳━╋╮╭╋━━┳━╮
#   ┃┃╱╭┫┃╱┃┃┃╱╭┫╭━╮┃╰━╯┣━━╮┃┃╭━╮┃┃┃┃╭╮┫┃┃┃━┫╭╯
#   ┃╰━╯┃╰━╯┃╰━╯┃╰━╯┃╭━╮┃╰━╯┃┃┃╱┃┃╰╯┃┃┃┃╰┫┃━┫┃
#   ╰━━━┻━━━┻━━━┻━━━┻╯╱╰┻━━━╯╰╯╱╰┻━━┻╯╰┻━┻━━┻╯
#--------------------------------------------------#

import re
import json
import urllib.parse

# Gets list from XSOAR
listRAW = demisto.executeCommand("getList", {"listName":"LOLBAS_Simple_2"})

# Makes list a string object
list_str = json.dumps(listRAW)

# regex for gathering only filenames contained in the LOLBAS list
pattern = r'\b[\w-]+(?:\.[\w-]+)+\b(?=.*HumanReadable)'
pattern2 = r'Contents.*?\b(true|false)\b'

# Loops through the RAW list and gets only the filenames (without beginning or ending characters)
list_semi_raw = re.findall(pattern, list_str)

# Creates a list that is ONLY the file names
clean_list = [value.strip(",") for value in list_semi_raw]

# Establish final list for stored "true" results
Final_Results = []

# Create loop that looks for upper case, lower case and capitalized versions of the LOLBAS filename.
for i in clean_list:
    # Three different variations of the filename - XDR will sometimes capitalize or turn a file into all caps
    upper = i.upper()
    lower = i.lower()
    capital = i.capitalize()

    # Runs a command for all different variations to search for the filename in the context data
    # If the logic matches "true" then it stores it in a list with all "true" hits
    upperRAW = demisto.executeCommand("ContextSearchForString", {"str": upper})
    upperJSON = json.dumps(upperRAW)
    upperTF = re.findall(pattern2, upperJSON)
    if upperTF[0] == "true":
        Final_Results.append(i)

    lowerRAW = demisto.executeCommand("ContextSearchForString", {"str": lower})
    lowerJSON = json.dumps(lowerRAW)
    lowerTF = re.findall(pattern2, lowerJSON)
    if lowerTF[0] == "true":
        Final_Results.append(i)

    capitalRAW = demisto.executeCommand("ContextSearchForString", {"str": capital})
    captialJSON = json.dumps(capitalRAW)
    capitalTF = re.findall(pattern2, captialJSON)
    if capitalTF[0] == "true":
        Final_Results.append(i)

# Verifies the data for all successfull hits
print(Final_Results)

# Logic for creating the url for an analyst to click on
url = "https://lolbas-project.github.io/lolbas/Binaries/"
urls = []
for j in Final_Results:
    stripped = j[:-4]
    urlJ = url + stripped + "/"
    urls.append(urlJ)

# Remmoves any apostraphes for the final URL to be presented
urls_final = [value.strip("'") for value in urls]
print(urls_final)
