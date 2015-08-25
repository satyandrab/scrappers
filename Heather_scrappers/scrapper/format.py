#!/usr/bin/python
# -*- coding: utf-8 -*-

import csv

header = [ 'id','name','gender',
           'photo','photo_web',
           'web_button','web_sendafriend',
           'state','qual_licensestateCode','zipcode',
           'btn_email',
           'freeconsult',
           'fin_mincost','fin_maxcost','fin_slidescale',
           'qual_yrpractice','qual_school',
           'qual_yrgrad','qual_licensenum',
           'modified','yrmod']
def genDictSet(string,outDict):
  tmpList         = [x.replace(' ','_') for x in string.split(':')]
  nextKey         = tmpList[0]
  for index,x in enumerate(tmpList[1:]):
    tmp = [y.strip() for y in x.split(';')]
    if nextKey not in outDict:
      outDict[nextKey] = set()
    if index+2 < len(tmpList):
      outDict[nextKey].update(tmp[:-1])
    else:
      outDict[nextKey].update(tmp)
    nextKey = tmp[-1]

occSet            = set()
specSet           = set()
paySet            = set()
insurSet          = set()
fieldsDict        = {}
clientsDict       = {}
progDict          = {}
with open('profiles.csv', 'rb') as csvfile:
  reader            = csv.DictReader(csvfile, delimiter=',')
  for row in reader:
    occ             = [x.strip() for x in row['occupation'].split(';')]
    spec            = [x.strip() for x in row['specialties'].split(';')]
    pay             = [x.strip() for x in row['fin_payment'].split(';')]
    insur           = [x.strip() for x in row['fin_insurance'].split(';')]
    genDictSet(row['fields'],fieldsDict)
    genDictSet(row['clientFocus'],clientsDict)
    genDictSet(row['programTreatment'],progDict)
    progList        = filter(lambda c:len(c[1])>0 ,progDict.iteritems())
    progList        = [[x[0],filter(lambda c: len(c)>0 ,x[1])] for x in progList]
    if len(occ[0])>0:
      occSet.update(occ)
    if len(spec[0])>0:
      specSet.update(spec)
    if len(pay[0])>0:
      paySet.update(pay)
    if len(insur[0])>0:
      insurSet.update(insur)
  csvfile.close()
  
statesDict = {}
with open('States.csv', 'rb') as statesfile:
  reader            = csv.DictReader(statesfile, delimiter=',')
  for row in reader:
    statesDict[row['stateUpper'].encode('utf-8')] = row['stateCode']
    
with open('profiles.csv', 'rb') as csvfile:
  reader            = csv.DictReader(csvfile, delimiter=',')
  with open('profilesCoded.csv', 'w') as csvfileWrite:
    occHeader     = ['occ_'+x for x in occSet]
    specHeader    = ['spec_'+x for x in specSet]
    payHeader     = ['pay_'+x for x in paySet]
    insurHeader   = ['insur_'+x for x in insurSet]
    fieldsHeader  = [[key+'_'+x for x in val] for (key,val) in fieldsDict.iteritems()]
    fieldsHeader  = [item for sublist in fieldsHeader for item in sublist]
    clientsHeader = [[key+'_'+x for x in val] for (key,val) in clientsDict.iteritems()]
    clientsHeader = [item for sublist in clientsHeader for item in sublist]
    progHeader    = [[x[0]+'_'+y for y in x[1]]for x in progList]
    progHeader    = [item for sublist in progHeader for item in sublist]
    
    
    headers = header + occHeader + specHeader + payHeader + insurHeader + fieldsHeader + progHeader + clientsHeader
    writer = csv.DictWriter(csvfileWrite, fieldnames=headers)
    writer.writeheader()

    for row in reader:
      rowDict         = {}
      fields          = {}
      clients         = {}
      prog            = {}
      occ             = [x.strip() for x in row['occupation'].split(';')]
      spec            = [x.strip() for x in row['specialties'].split(';')]
      pay             = [x.strip() for x in row['fin_payment'].split(';')]
      insur           = [x.strip() for x in row['fin_insurance'].split(';')]
      genDictSet(row['fields'],fields)
      genDictSet(row['clientFocus'],clients)
      genDictSet(row['programTreatment'],prog)
      for x in header:
        rowDict[x] = row[x]
      if row['state']:
        state = row['state'].upper().replace('\xc2\xa0',' ')
        if state in statesDict:
          rowDict['state'] = statesDict[state]
        else:
          rowDict['state'] = state
      if row['qual_licensestateCode']:
        qual_licensestateCode = row['qual_licensestateCode'].upper().replace('\xc2\xa0',' ')
        if qual_licensestateCode in statesDict:
          rowDict['qual_licensestateCode'] = statesDict[qual_licensestateCode]
        else:
          rowDict['qual_licensestateCode'] = qual_licensestateCode

      for x in occSet:
        if x in occ:
          rowDict['occ_'+x] = '1'
        else:
          rowDict['occ_'+x] = '0'
      for x in specSet:
        if x in spec:
          rowDict['spec_'+x] = '1'
        else:
          rowDict['spec_'+x] = '0'
      for x in paySet:
        if x in pay:
          rowDict['pay_'+x] = '1'
        else:
          rowDict['pay_'+x] = '0'
      for x in insurSet:
        if x in insur:
          rowDict['insur_'+x] = '1'
        else:
          rowDict['insur_'+x] = '0'
          
      for x in progList:
        for y in x[1]:
          if x[0] in prog:
            if y in prog[x[0]]:
              rowDict[x[0]+'_'+y]='1'
            else:
              rowDict[x[0]+'_'+y]='0'
          else:
            rowDict[x[0]+'_'+y]='0'
      for key,value in clientsDict.iteritems():
        for v in value:
          if key in clients:
            if v in clients[key]:
              rowDict[key+'_'+v]='1'
            else:
              rowDict[key+'_'+v]='0'
          else:
            rowDict[key+'_'+v]='0'
      for key,value in fieldsDict.iteritems():
        for v in value:
          if key in fields:
            if v in fields[key]:
              rowDict[key+'_'+v]='1'
            else:
              rowDict[key+'_'+v]='0'
          else:
            rowDict[key+'_'+v]='0'

      writer.writerow(rowDict)
