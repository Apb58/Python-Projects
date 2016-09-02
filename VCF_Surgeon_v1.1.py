# VCF Surgeon: Add variants to VCF file (read from separate text file)
# VCF Surgeon v1.0
# v1.0: Allow user to use variant text file with multiple variants

# 08/26/2016
# Adrian Bubie

#Given a text file containing the chromosome, start, ref, alt and vaf, add a
#variant row to a specified VCF. See "Var_to_add" text file for required formatting

def PGM_vcf_mod(File, Var):
    
    VCF = File.read()
    Lines = VCF.split('\r')
    print "length of original VCF:",len(Lines)
    
    #Get variant fields from VAR file:
    Var_re = Var.read().split('\n')
    
    if len(Var_re)%4 != 0:
        tkMessageBox.showinfo("VCF Surgeon: Error", "Variant Text file either has too many or too few lines! Please reformat.")
        

    var_sets = list()
    for i in range(0, len(Var_re),4):
        var_set = Var_re[i:i+4]
        var_sets.append(var_set)
        
    for variant in var_sets:
        
        vals_1 = variant[0].split(':')
        chrome = vals_1[0]
        pos = vals_1[1]

        vals_2 = variant[1].split(':')
        ref = vals_2[1]

        vals_3 = variant[2].split(':')
        alt = vals_3[1]

        vals_4 = variant[3].split(':')
        vaf = float(vals_4[1])


        #Construct new Variant line:
        vaf_true = float(vaf/100.0)
        AO = str(int(1000*vaf_true))
        sample = '0/1:100:1000:1000:0:0:'+AO+':'+AO+':0:0'
        line_parts = (chrome,pos,'.',ref,alt,'100','PASS','.','GT:GQ:DP:FDP:RO:FRO:AO:FAO:AF:SAR:SAF:SRF:SRR:FSAR:FSAF:FSRF:FSRR',sample)

        new_line_parts = list()
        for item in line_parts:
            item = str(item)
            new_line_parts.append(item)

        new_line = '\t'.join(new_line_parts)

        # Find position in VCF to insert new variant:
        found = False
        for i in range(0,len(Lines)-1):
            if Lines[i].startswith(chrome):
                cols = Lines[i].split('\t')
                POS = cols[1]
    
                if POS > pos:
                    Lines.insert(i,new_line)
                    found = True
                    break

                else:
                    pass

        #If there are no variants already in the VCF with your new variant's chromosome, add the line to the end of the file
        if found == False:
            j = len(Lines)
            Lines.insert(j,new_line)


    return Lines


def MiSeq_vcf_mod(File, Var):

    VCF = File.read()
    Lines = VCF.split('\r')
    print "length of original VCF:",len(Lines)
    
    #Get variant fields from VAR file:
    Var_re = Var.read().split('\n')

    if len(Var_re)%4 != 0:
        tkMessageBox.showinfo("VCF Surgeon: Error", "Variant Text file either has too many or too few lines! Please reformat.")

    var_sets = list()
    for i in range(0, len(Var_re),4):
        var_set = Var_re[i:i+4]
        var_sets.append(var_set)

    for variant in var_sets:
        
        vals_1 = variant[0].split(':')
        chrome = vals_1[0]
        pos = vals_1[1]
        chrm_num = int(chrome.strip('chr'))

        vals_2 = variant[1].split(':')
        ref = vals_2[1]

        vals_3 = variant[2].split(':')
        alt = vals_3[1]

        vals_4 = variant[3].split(':')
        vaf = float(vals_4[1])


        #Construct new Variant line:
        vaf_true = float(vaf/100.0)
        AO = int(1000*vaf_true)
        RD = str(1000-AO)
        AO = str(AO)
        sample = '0/1:100:'+RD+','+AO+':0:0'
        line_parts = (chrome,pos,'.',ref,alt,'100','PASS','.','GT:GQ:AD:VF:NL:SB:GQX',sample)

    
        new_line_parts = list()
        for item in line_parts:
            item = str(item)
            new_line_parts.append(item)

        new_line = '\t'.join(new_line_parts)

        # Find position in VCF to insert new variant:
        found = False
        for i in range(0,len(Lines)-1):
            if Lines[i].startswith(chrome):
                cols = Lines[i].split('\t')
                POS = cols[1]
    
                if POS > pos:
                    Lines.insert(i,new_line)
                    found = True
                    break

                else:
                    pass

        #If there are no variants already in the VCF with your new variant's chromosome, add the line to the end of the file
        if found == False:
            j = len(Lines)
            Lines.insert(j,new_line)
    

    return Lines


def mainfunc():

    file_name = E1.get()
    var_name = E2.get()
    platform = E3.get()
   
    import os
    file_path = os.path.abspath(file_name)
    var_path = os.path.abspath(var_name)

    if file_path.endswith('.vcf'):
        File = open(file_path,'r')
        
    else:
        tkMessageBox.showinfo("VCF Surgeon: Error", "The VCF File you have entered is either Invalid or does not exist")

    if var_path.endswith('.txt'):
        Var = open(var_path,'r')

    else:
        tkMessageBox.showinfo("VCF Surgeon: Error", "The Variant File you have entered is either Invalid or does not exist")

    if platform == 'PGM':
        Lines = PGM_vcf_mod(File, Var)

        #Restucture and create the new VCF file:
        #N_VCF = open('/Users/Adrian/Desktop/VCF Surgeon/TSVC_variants_new.vcf','w')
        N_VCF = open('New_VCF.vcf','w')
        print "length of new VCF:",len(Lines)

        N_VCF.write('\r'.join(Lines))
        N_VCF.close()
        File.close()
        Var.close()

        tkMessageBox.showinfo("VCF Surgeon", "Success! Your new VCF has been generated")

    if platform == 'MiSeq':
        Lines = MiSeq_vcf_mod(File, Var)

        #Restucture and create the new VCF file:
        #N_VCF = open('/Users/Adrian/Desktop/VCF Surgeon/TSVC_variants_new.vcf','w')
        N_VCF = open('New_VCF.vcf','w')
        print "length of new VCF:",len(Lines)

        N_VCF.write('\n'.join(Lines))
        N_VCF.close()
        File.close()
        Var.close()

        tkMessageBox.showinfo("VCF Surgeon", "Success! Your new VCF has been generated")

    elif platform not in ['MiSeq','PGM']:
        tkMessageBox.showinfo("VCF Surgeon: Error", "The Platform You have entered is Invalid")


if __name__ == "__main__":
    
    import Tkinter
    from Tkinter import *
    import tkMessageBox

    top = Tkinter.Tk()
    top.title("VCF_Surgeon")
    top.geometry('600x200')
    

    L1 = Label(top, text="Enter Name of VCF (include .vcf):")
    L1.pack()

    E1 = Entry(top)
    E1.pack()

    L2 = Label(top, text="Enter Name of Variant Text File (include .txt):")
    L2.pack()

    E2 = Entry(top)
    E2.pack()

    L3 = Label(top, text="Enter Platform type (PGM or MiSeq):")
    L3.pack()

    E3 = Entry(top)
    E3.pack()


    B = Tkinter.Button(top, text = "Run", command = mainfunc)
    B.pack()

    top.mainloop()
        
