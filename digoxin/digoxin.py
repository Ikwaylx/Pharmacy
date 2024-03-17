#imports the sys for argv argc implementation
import sys

#insert constants here
DIGOXIN_DISTRIBUTION_VOLUME = float(7.3)
DIGOXIN_SALT_FACTOR = 1
DIGOXIN_F = float(0.65)
TIME_CONSTANT = 24

def main():
    #TODO Ensure that correct usage of the function is made
    if len(sys.argv) != 6:
        sys.exit("Usage: ./digoxin.py age sex creatinine digconc weight")

    #define all variables
    age = int(sys.argv[1])
    sex = sys.argv[2].lower()
    creatinine = int(sys.argv[3])
    digconc = float(sys.argv[4])
    weight = float(sys.argv[5])
    crcl = float(0)
    volume_distribution = 0
    loadingdose = 0
    ivloadingdose = 0
    isHF = input('Does your patient have CHF? (y/n): ').lower().strip() == 'y'
    digoxin_clearance = 0
    maintenance_dose = 0


#do the calculation of creatinine clearance
    if sex != 'male':
        if sex != 'female':
            sys.exit("Error: Please enter male or female for sex")

    crcl = int(calculate_creatinine_clearance(age, sex, weight, creatinine))
    print("Creatinine Clearance = " + str(crcl) + "ml/min\n")

# Calculate the volume of distribution using two equations
    volume_distribution = calculate_volume_of_distribution(crcl, weight)
    print("the volume of distribution for this patient = " + str(volume_distribution) + "L\n")

# Calculate the desired loading doses
    loadingdose = int(calculate_loading_dose(digconc, volume_distribution))
    print("The oral loading dose needed for this patient would be " + str(loadingdose) + " micrograms")
    ivloadingdose = int(calculate_iv_loading_dose(digconc, volume_distribution))
    print("The IV loading dose for this patient if applicable would be " + str(ivloadingdose) + " micrograms\n")

# Calculate digoxin clearance
    digoxin_clearance = calculate_clearance(weight, crcl, isHF)

# Then calculate a maintenance dose based on that
    maintenance_dose = calculate_maintenance_dose(digconc, digoxin_clearance)
    print("The maintenance dose for oral tablets should be " + str(maintenance_dose) + " micrograms daily\n")
    sys.exit("Calculations completed successfully!")
    
        

#functions
        
def calculate_creatinine_clearance(age, sex, weight, creatinine):
    crcl = round(weight * (140 - age) / creatinine)
    if sex == "female":
        return crcl
    else:
        crcl = crcl * 1.23
        return crcl
    
def calculate_volume_of_distribution(crcl, weight):
    #Use formula for normal renal function first
    volume1 = DIGOXIN_DISTRIBUTION_VOLUME * weight
    #Then use the formula in renal impairment
    volume2 = 3.8 * weight + (3.1 * crcl)
    #compare the two, choose the lower of the two
    if volume1 < volume2:
        return volume1
    else:
        return volume2

def calculate_loading_dose(digconc, volume):
    loadingdose = (digconc * volume) / (DIGOXIN_SALT_FACTOR * DIGOXIN_F)
    loadingdose = round(loadingdose / 125) * 125
    return loadingdose

def calculate_iv_loading_dose(digconc, volume):
    loadingdose = (digconc * volume) / DIGOXIN_SALT_FACTOR
    loadingdose = round(loadingdose / 250) * 250
    return loadingdose

def calculate_clearance(weight, crcl, isHF):
    if isHF:
        clearance = 0.33 * weight + (0.9 * crcl)
        #convert to L/hr
        clearance = clearance * 60 / 1000
        return clearance
    else:
        clearance = 0.8 * weight + crcl
        #convert to L/hr
        clearance = clearance * 60 / 1000
        return clearance

def calculate_maintenance_dose(digconc, clearance):
    maintenance_dose = (((digconc * clearance) * TIME_CONSTANT) / DIGOXIN_SALT_FACTOR) / DIGOXIN_F
    maintenance_dose = round(maintenance_dose / 125) * 125
    return maintenance_dose
    
if __name__ == "__main__":
    main()
    