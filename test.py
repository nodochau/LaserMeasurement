import pandas as pd

data = pd.read_csv('InventoryData.csv')

print(data)

def findPositions(material):
  theDic = {}
  thelist = []
  for row in data.itertuples():
    if row.MATERIAL == material:
      thelist.append(row.XPOS)
      thelist.append(row.YPOS)
      theDic[material] = thelist
  return theDic

print(findPositions(789))

print(findPositions(789)[789][0])