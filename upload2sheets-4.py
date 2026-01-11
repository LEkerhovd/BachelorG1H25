import gspread #importerer ønsket pakke
from oauth2client.service_account import ServiceAccountCredentials #importerer credentials handler for Google service konto
from datetime import datetime #bruk for å genrere timestamp for hver rad med data


#Definer tillatelsene (scope) scriptet trenger
# - Tilgang til Google Sheets
# - Tilgang til Google Drive (kreves for å åpne regnearket)

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
    ]

#laster service konto credentials fra JSON key fil
#authentiserer Raspberry Pi med google
creds = ServiceAccuntCredentials.from_json_keyfile_name(
    "zooia-1.sjon",
    scope
    )

client = gspread.authorize(creds) #autoriserer gspread til å bruke creds

#åpner Google sheet ved bruke av navn
#vær sikker på at regnearket er delt med service konto email
sheet = client.open("Pi Data Logger").sheet1

timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S") #Genererer timestamp for når data blir lastet opp

#sett inn sensor data

sheet.append_row([timestamp, value])

print("Data lastet opp!")