from django.shortcuts import render
import requests
from . import models
from .serializer import SwissProt_Serizalizer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
# Create your views here.

class Swiss_prot:

    def __init__(self, filepath):
        self.file = filepath
        self.hash_file = {}
        self.rf_hash_file = {}
        self.sq_hash_file = {}

        for i in self.file:
            each_line = i.split("   ")
            each_line_id = each_line[0]

            # SQ case:
            if each_line_id == "":
                each_line_id = "SQ"

            # Reference case
            if each_line_id in ['RN', 'RP', 'RC', 'RX', 'RA', 'RL', 'RT']:
                if each_line_id == "RN":
                    ref_number = f"Refernce {each_line[1].strip()}: "
                    if ref_number not in self.rf_hash_file:
                        self.rf_hash_file[ref_number] = {}
                else:
                    if each_line_id not in self.rf_hash_file[ref_number]:
                        self.rf_hash_file[ref_number][each_line_id] = ["   ".join(each_line[1:]).strip()]
                    else:
                        self.rf_hash_file[ref_number][each_line_id] += ["   ".join(each_line[1:]).strip()]

            # FT case
            elif each_line_id == "FT":
                if each_line_id not in self.hash_file:
                    self.hash_file[each_line_id] = [each_line[1:]]
                else:
                    self.hash_file[each_line_id] += [each_line[1:]]

            # Other cases
            elif each_line_id not in self.hash_file:
                self.hash_file[each_line_id] = ["   ".join(each_line[1:]).strip()]
            else:
                self.hash_file[each_line_id] += ["  ".join(each_line[1:]).strip()]

    # ID - Identification.
    def get_ID(self):
        
        if 'ID' not in self.hash_file: return "This record doesn't exist in this file"
        return self.hash_file["ID"][0]

    # AC - Accession number(s).
    def get_AC(self):
        if 'AC' not in self.hash_file: return "This record doesn't exist in this file"
        return "\n ".join(self.hash_file["AC"])

    # DT - Date.
    def get_DT(self):
        
        if 'DT' not in self.hash_file: return "This record doesn't exist in this file"
        return "\n".join(self.hash_file["DT"])

    # DE - Description.
    def get_DE(self):
        if 'DE' not in self.hash_file: return "This record doesn't exist in this file"
        # return "\n".join(self.hash_file["DE"])
        return [i for i in self.hash_file["DE"]]

    # GN - Gene name(s).
    def get_GN(self):
        if 'GN' not in self.hash_file: return "This record doesn't exist in this file"
        return "\n".join(self.hash_file["GN"])

    # OS - Organism species.
    def get_OS(self):
        if 'OS' not in self.hash_file: return "This record doesn't exist in this file"
        return "\n".join(self.hash_file["OS"])

    # OG - Organelle.
    def get_OG(self):
        if 'OG' not in self.hash_file: return "This record doesn't exist in this file"
        return self.hash_file["OG"]

    # OC - Organism classification.
    def get_OC(self):
        if 'OC' not in self.hash_file: return "This record doesn't exist in this file"
        return " ".join(self.hash_file["OC"])

    # RN - Reference info.
    def get_RN(self):
        # if 'RN' not in self.hash_file: return "This record doesn't exist in this file"
        return self.rf_hash_file

    # CC - Comments or notes.
    def get_CC(self):
        if 'CC' not in self.hash_file: return "This record doesn't exist in this file"
        CC_content = []
        note = ""
        for i in self.hash_file["CC"]:
            if i[0:3] == "-!-":
                note += "\n"
                note += i
            else:
                note += i
                note += "   \n  "
                CC_content.append(note)
                note = ""
        return "    ".join(CC_content)

    # DR - Database cross-references.
    def get_DR(self):
        if 'DR' not in self.hash_file: return "This record doesn't exist in this file"
        o = ""
        for i in self.hash_file["DR"]:
            o += str(i)
            o += "\n\n"
        return o

    # KW - Keywords.
    def get_KW(self):
        if 'KW' not in self.hash_file: return "This record doesn't exist in this file"
        return "".join(self.hash_file["KW"])

    # FT - Feature table data.
    def get_FT(self):
        if 'FT' not in self.hash_file: return "This record doesn't exist in this file"
        o = ""
        for i in self.hash_file["FT"]:
            o += str("  ".join(i))
            o += "\n"
        return o

    # SQ - Sequence header & data.
    def get_SQ(self):
        if 'SQ' not in self.hash_file: return "This record doesn't exist in this file"
        header = self.hash_file["SQ"][0]
        sequence = "".join(self.hash_file["SQ"][1:])
        return (f"Header: {header},\n\n Sequence: \n\n {sequence}")




# CC - Comments or notes.
def get_CC(self):
    if 'CC' not in self.hash_file: return "This record doesn't exist in this file"
    return "\n".join(self.hash_file["CC"])



@api_view(['GET','POST'])
def SwissProt_Get_Post(request):
    # GET
    if request.method == 'GET':
        sequences = models.SwissProt_Model.objects.all()
        serializer = SwissProt_Serizalizer(sequences, many=True)
        return Response(serializer.data)


    # POST
    elif request.method == 'POST':
        
        
        urll = request.data["url"]

        response = requests.get(urll)
        data = response.text
        f = ""
        # for i, line in enumerate(data.split('\n')):
        #     f+=line
        #     f+='\n'

        objectt = models.SwissProt_Model()
        objectt.url = urll
        if response.status_code==200:
            objectt.downlaoded = True
            objectt.data = data.split('\n')
            print("ok")
        else:
            objectt.downlaoded = False
            objectt.data = "None"
            return Response(status= status.HTTP_400_BAD_REQUEST)

        
        req = request.data["Required"]
        #[""]
        

        obj = Swiss_prot(data.split('\n'))
        
        dic = {}
        print("ok")
        print("required = ",req)
        if req == "*":
            dic["Identification"] = obj.get_ID()
            dic["Accession_number"] = obj.get_AC()
            dic["Date"] = obj.get_DT()
            dic["Description"] = obj.get_DE()
            dic["Gene_name"] = obj.get_GN() 
            dic["Organism_species"] = obj.get_OS()
            dic["Organelle"] = obj.get_OG()
            dic["Organism_classification"] = obj.get_OC()
            dic["Reference_info"] = obj.get_RN()
            dic["Comments_or_notes_attached"] = obj.get_CC()
            dic["Database_cross_references"] = obj.get_DR()
            dic["Keywords"] = obj.get_KW()
            dic["Feature_table_data"] = obj.get_FT()
            dic["Sequence"] = obj.get_SQ()
        else:            
            counter = 0
            for i in req:
                print("i = ",i)
                if i=="Identification": 
                    

                    dic["Identification"] = obj.get_ID()
                elif i=="Accession number": 
                    
                    dic["Accession_number"] = obj.get_AC()
                elif i=="Date": 
                    
                    dic["Date"] = obj.get_DT()

                elif i=="Description": 

                    dic["Description"] = obj.get_DE()

                elif i=="Gene_name": 
                
                    dic["Gene_name"] = obj.get_GN() 

                elif i=="Organism_species": 
                    
                    dic["Organism_species"] = obj.get_OS()

                elif i=="Organelle": 
                    
                    dic["Organelle"] = obj.get_OG()
                    

                elif i=="Organism_classification": 
                    
                    dic["Organism_classification"] = obj.get_OC()
                    
                elif i=="Reference_info": 
                    
                    dic["Reference_info"] = obj.get_RN()

                elif i=="Comments_or_notes_attached": 
                    
                    dic["Comments_or_notes_attached"] = obj.get_CC()

                elif i=="Database_cross_references": 
                    
                    dic["Database_cross_references"] = obj.get_DR()

                elif i=="Keywords": 
                    
                    dic["Keywords"] = obj.get_KW()

                elif i=="Feature_table_data": 
                    
                    dic["Feature_table_data"] = obj.get_FT()

                elif i=="Sequence": 
                    
                    dic["Sequence"] = obj.get_SQ()
                else:
                    dic["you entered something wrong"] : counter
                    counter +=1

        print(dic)        
        serializer = SwissProt_Serizalizer(data=dic)
        
        if serializer.is_valid():
            print("valid")
            serializer.save()
            return Response(serializer.data, status= status.HTTP_201_CREATED)
        print("not valid")
        print(serializer.data)
        return Response(serializer.data, status= status.HTTP_400_BAD_REQUEST)
