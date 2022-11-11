"""Common datasets"""

from collections import OrderedDict

us_states = {
    'AK': 'Alaska', 'AL': 'Alabama', 'AR': 'Arkansas', 'AZ': 'Arizona', 'CA': 'California',
    'CO': 'Colorado', 'CT': 'Connecticut', 'DC': 'District of Columbia', 'DE': 'Delaware',
    'FL': 'Florida', 'GA': 'Georgia', 'HI': 'Hawaii', 'IA': 'Iowa', 'ID': 'Idaho',
    'IL': 'Illinois', 'IN': 'Indiana', 'KS': 'Kansas', 'KY': 'Kentucky', 'LA': 'Louisiana',
    'MA': 'Massachusetts', 'MD': 'Maryland', 'ME': 'Maine', 'MI': 'Michigan', 'MN': 'Minnesota',
    'MO': 'Missouri', 'MS': 'Mississippi', 'MT': 'Montana', 'NC': 'North Carolina', 'ND': 'North Dakota',
    'NE': 'Nebraska', 'NH': 'New Hampshire', 'NJ': 'New Jersey', 'NM': 'New Mexico', 'NV': 'Nevada',
    'NY': 'New York', 'OH': 'Ohio', 'OK': 'Oklahoma', 'OR': 'Oregon', 'PA': 'Pennsylvania',
    'RI': 'Rhode Island', 'SC': 'South Carolina', 'SD': 'South Dakota', 'TN': 'Tennessee',
    'TX': 'Texas', 'UT': 'Utah', 'VA': 'Virginia', 'VT': 'Vermont', 'WA': 'Washington',
    'WI': 'Wisconsin', 'WV': 'West Virginia', 'WY': 'Wyoming'
}

# NOTE: updated at 2022-11-10, from each ISO's website
iso_states = OrderedDict([
    ("MISO", ["Alabama", "Arkansas", "Illinois", "Indiana", "Iowa",
     "Kentucky", "Louisiana", "Michigan", "Minnesota", "Mississippi",
              "Missouri", "North Dakota", "South Dakota", "Texas", "Wisconsin"]),
    ("SPP", ["Arkansas", " Iowa", " Kansas", " Louisiana", " Minnesota",
     "Missouri", " Montana", " Nebraska", " New Mexico", " North Dakota",
             "Oklahoma", " South Dakota", " Texas", " Wyoming"]),
    ("PJM", ["Delaware", "Illinois", "Indiana", "Kentucky", "Maryland",
     "Michigan", "New Jersey", "North Carolina", "Ohio", "Pennsylvania",
             "Tennessee", "Virginia", "West Virginia", "District of Columbia"]),
    ("ERCOT", ["Texas"]),
    ("CAISO", ["California"]),
    ("ISONE", ["Connecticut", " Maine", " Massachusetts", " New Hampshire", " Rhode Island",
     "Vermont"]),
    ("NYISO", ["New York"]),
])
