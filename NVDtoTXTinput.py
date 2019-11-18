
import pandas as pd
import json

# Parse .json files from national security database
# cveFile should be the .json that comes from the NVD datbase. For example: nvdcve-1.1-2018.json
# newCSVname is optional. If newCSVname is passed, it should end in .csv
# NVDtoDF returns a dataframe
def NVDtoDF(cveFile, newCSVname=None):

    #
    with open(cveFile, "r") as read_file:
        data = json.load(read_file)
    df = pd.DataFrame(data['CVE_Items'])

    # get number of vulnerabilities in cveFile
    cveCount = df['cve'].count()

    # these lists will populate be used to create the dataframe
    IDarray = []
    descriptionArray = []
    attackVectorArr = []
    baseScore3Arr = []
    baseSeverity3Arr = []
    exploitablityScore3Arr = []
    impactScore3Arr = []
    baseScore2Arr = []
    severity2Arr = []
    exploitablityScore2Arr = []
    cveCount = df.cve.count()
    unableToFill = "couldNotFill"

    # populate each list
    for i in range(0, cveCount):

        IDarray.append(data['CVE_Items'][i]['cve']['CVE_data_meta']['ID'])
        descriptionArray.append(data['CVE_Items'][i]['cve']['description']['description_data'][0]['value'])
        if ('baseMetricV3' in data['CVE_Items'][i]['impact']):
            attackVectorArr.append(data['CVE_Items'][i]['impact']['baseMetricV3']['cvssV3']['attackVector'])
            baseSeverity3Arr.append(data['CVE_Items'][i]['impact']['baseMetricV3']['cvssV3']['baseSeverity'])
            baseScore3Arr.append(data['CVE_Items'][i]['impact']['baseMetricV3']['cvssV3']['baseScore'])
            exploitablityScore3Arr.append(data['CVE_Items'][i]['impact']['baseMetricV3']['exploitabilityScore'])
            impactScore3Arr.append(data['CVE_Items'][i]['impact']['baseMetricV3']['impactScore'])
        else:
            attackVectorArr.append(unableToFill)
            baseSeverity3Arr.append(unableToFill)
            baseScore3Arr.append(unableToFill)
            exploitablityScore3Arr.append(unableToFill)
            impactScore3Arr.append(unableToFill)
        if ('baseMetricV2' in data['CVE_Items'][i]['impact']):
            baseScore2Arr.append(data['CVE_Items'][i]['impact']['baseMetricV2']['cvssV2']['baseScore'])
            severity2Arr.append(data['CVE_Items'][i]['impact']['baseMetricV2']['severity'])
            exploitablityScore2Arr.append(data['CVE_Items'][i]['impact']['baseMetricV2']['exploitabilityScore'])
        else:
            baseScore2Arr.append(unableToFill)
            severity2Arr.append(unableToFill)
            exploitablityScore2Arr.append(unableToFill)

    # convert each populated list to a pandas/numpy Series
    IDs = pd.Series(IDarray)
    descriptions = pd.Series(descriptionArray)
    attackVector = pd.Series(attackVectorArr)
    baseScore3 = pd.Series(baseScore3Arr)
    baseSeverity3 = pd.Series(baseSeverity3Arr)
    exploitablityScore3 = pd.Series(exploitablityScore3Arr)
    impactScore3 = pd.Series(impactScore3Arr)
    baseScore2 = pd.Series(baseScore2Arr)
    severity2 = pd.Series(severity2Arr)
    exploitablityScore2 = pd.Series(exploitablityScore2Arr)

    # create each column
    df['CVE_ID'] = IDs
    df['description'] = descriptions
    df['attack_vector'] = attackVector
    df['baseScore_V3'] = baseScore3
    df['baseSeverity_V3'] = baseSeverity3
    df['exploitablityScore_V3'] = exploitablityScore3
    df['impactScore_V3'] = impactScore3
    df['baseScore_V2'] = baseScore2
    df['severity_V2'] = severity2
    df['exploitablityScore_V2'] = exploitablityScore2

    # Making descriptions lowercase makes finding technology keywords easier.
    df['description'] = df['description'].str.lower()

    CVEorg = df
    # drop extra columns
    CVEorg = CVEorg.drop(columns=['configurations', 'cve', 'impact', 'lastModifiedDate', 'publishedDate'])

    # write to newCSVname.csv in current directory
    if newCSVname:
        CVEorg.to_csv('%s.csv' % newCSVname, index=False)

    return CVEorg

# Processes dataframe from NVDtoDF, along with a list of technology keywords into a text file that will be
# input to the attacker instance.
# dframe is the processed CVE dataframe
# keyword_list is a list of lowercase strings of technlogies
# new_file_name is the name of the file to write to
def get_input_txt(dframe, keyword_list, new_file_name):
    temp_df = dframe.copy()

    temp_df['description'] = temp_df['description'].str.lower()

    # Create boolian for each keyword that specifies whether it is found in the vulnerability description
    for k in keyword_list:
        temp_df[k] = temp_df['description'].str.contains(pat=k)

    # Open/create txt file
    output = open('%s.txt' % new_file_name, "w")
    output.seek(0)
    output.truncate()
    for k in keyword_list:
        # Dataframe of only CVEs with keyword k in the description
        k_df = temp_df[temp_df[k] == True]
        cve_string = ""
        score_string = ""

        for index, row in k_df.iterrows():
            # Row of CVE-IDs seperated by '|'s
            cve_string += (str(row['CVE_ID']) + '|')
            # Row of sets of base score, exploitability score, impact score seperated by whitespace
            score_string += (str(row['baseScore_V3']) + ',' + str(row['exploitablityScore_V3']) + \
                             ',' + str(row['impactScore_V3']) + ' ')
        cve_string = cve_string[:-1] # take extra '|' from end
        score_string = score_string[:-1] # take extra whitespace from end

        # write to file
        output.write("keyword: ")
        output.write(str(k))
        output.write("\n")
        output.write("CVE count: ")
        output.write(str(k_df['CVE_ID'].count()))
        output.write("\n")
        output.write(cve_string)
        output.write("\n")
        output.write("\n")
        output.write(score_string)
        output.write("\n")
        output.write("\n")

    output.close()


# Combines NVDtoDF and get_input_text functions to take a .json from the NVD database
def NVDtoTXT(CVEfile, keyword_list, new_file_name):
    myDF = NVDtoDF(CVEfile, False)
    get_input_txt(myDF, keyword_list, new_file_name)






