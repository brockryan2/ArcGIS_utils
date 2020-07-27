## Brock Ryan
# created: 9/20/2017
# last updated: 10/03/2018
# Various snippets to define custom label properties in ArcMap / Pro (Using the Python language)

# Snippet 1:
## Used to only display the first x number of characters of the label

def FindLabel ( [Zoning] ):
    s = [Zoning]

    if (len(s) == 3):  # logic used to vary the length for certain features (ex: I wanted to label abbreviated zone names in which the abbreviation varied by feature type [RE vs. CON])
        s = s[:3]

    else: s = s[:2]  # splices used to only lebel the first x # of characters

    return  s


#Snippet 2:
## Address Point Name (Title Case):

def FindLabel ([Street_Num], [Street_Nam], [Street_Suf]):
      fields = ([Street_Num], [Street_Nam], [Street_Suf])
      result = " ".join(item for item in fields if item).title()
      return result


#Snippet 3:
## Street Name (Title Case):

def FindLabel ( [StreetDirection] ,[StreetName], [StreetType] ):

      fields = ([StreetDirection] ,[StreetName], [StreetType])
      result = " ".join(item for item in fields if item).title()
      return result



# label expression to better display parcel info for certain maps
  # this label displays parce id, owner name, and parcel address

  # parcel id --> no formatting
  # owner name --> run a .title() case conversion then check to see if a suffix (currently only II and III) exists
    # if one of these two suffixes exists, then the .title() case conversion text of Iii is replaced with III.
  # address --> title case conversion

#snippet 4:

  def FindLabel ([ParcelID], [Owner], [Address]):
    PID = [ParcelID]
    tmp = [Owner]
    adr = [Address]

    owner = tmp.title()

    if 'Iii' in owner:
        owner = owner.replace('Iii', 'III')
    elif 'Ii' in own:
        owner = owner.replace('Ii', 'II')

    return "  P A R C E L  # :  "  + PID + "\n \n   O W  N E R  :  " + owner + "\n \nA D D R E S S :  " +  adr.title()

