import hashlib
import gspread
from google.oauth2.service_account import Credentials

def MD5(value):
    return hashlib.md5(str(value).encode()).hexdigest()

def md5_from_sheet1_to_sheet2(sheet_id):
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
    client = gspread.authorize(creds)

    sh = client.open_by_key(sheet_id)
    sheet1 = sh.worksheet("B2B New")
    sheet2 = sh.worksheet("Server")

    data = sheet1.get_all_values()

    output = []

    for row in data:
        g = row[6] if len(row) > 6 else ""
        h = row[7] if len(row) > 7 else ""

        output.append([
            g,                    # G as-is
            h,                    # H as-is
            MD5(g) if g else "",  # MD5(G)
            MD5(h) if h else ""   # MD5(H)
        ])

    sheet2.update(
        f"A1:D{len(output)}",
        output,
        value_input_option="USER_ENTERED"
    )

    print("Data copied with original types preserved")

md5_from_sheet1_to_sheet2(
    sheet_id="Enter Sheet id Here"
)
