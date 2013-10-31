SUCCESS = {
    "ResultCode": "Success",
    "DocCode": "basket-3",
    "DocDate": "2013-10-31",
    "Timestamp": "2013-10-31T11:26:41.0162227Z",
    "TotalAmount": "18.97",
    "TotalDiscount": "0",
    "TotalExemption": "0",
    "TotalTaxable": "18.97",
    "TotalTax": "1.67",
    "TotalTaxCalculated": "1.67",
    "TaxLines": [
        {
            "LineNo": "1",
            "TaxCode": "P0000000",
            "Taxability": "true",
            "BoundaryLevel": "Zip5",
            "Exemption": "0",
            "Discount": "0",
            "Taxable": "11.99",
            "Rate": "0.088750",
            "Tax": "1.06",
            "TaxCalculated": "1.06"}
        ,{
            "LineNo": "2",
            "TaxCode": "P0000000",
            "Taxability": "true",
            "BoundaryLevel": "Zip5",
            "Exemption": "0",
            "Discount": "0",
            "Taxable": "2.99",
            "Rate": "0.088750",
            "Tax": "0.26",
            "TaxCalculated": "0.26"}
        ,{
            "LineNo": "SHIPPING",
            "TaxCode": "FR",
            "Taxability": "true",
            "BoundaryLevel": "Zip5",
            "Exemption": "0",
            "Discount": "0",
            "Taxable": "3.99",
            "Rate": "0.088750",
            "Tax": "0.35",
            "TaxCalculated": "0.35"}
    ]
    ,
    "TaxAddresses": [
        {
            "Address": "Nam Adipisicing Est Sunt Alias Et Minus Sit Dicta ",
            "AddressCode": "-320300137",
            "City": "Soluta culpa praesentium blanditiis ipsa",
            "Country": "US",
            "PostalCode": "10022",
            "Region": "NY",
            "TaxRegionId": "2088629",
            "JurisCode": "3600051000"},
        {
            "Address": "725 5TH Ave",
            "AddressCode": "1163066156",
            "City": "New York",
            "Country": "US",
            "PostalCode": "10022-2519",
            "Region": "NY",
            "TaxRegionId": "2088629",
            "JurisCode": "3600051000"}
    ],
    "TaxDate": "2013-10-31",
    "TaxSummary": [
        {
            "Country": "US",
            "Region": "NY",
            "JurisType": "State",
            "Taxable": "18.97",
            "Rate": "0.040000",
            "Tax": "0.76",
            "JurisName": "NEW YORK",
            "TaxName": "NY STATE TAX"},
        {
            "Country": "US",
            "Region": "NY",
            "JurisType": "City",
            "Taxable": "18.97",
            "Rate": "0.045000",
            "Tax": "0.85",
            "JurisName": "NEW YORK CITY",
            "TaxName": "NY CITY TAX"},
        {
            "Country": "US",
            "Region": "NY",
            "JurisType": "Special",
            "Taxable": "18.97",
            "Rate": "0.003750",
            "Tax": "0.06",
            "JurisName": "METROPOLITAN COMMUTER TRANSPORTATION DISTRICT",
            "TaxName": "NY SPECIAL TAX"
        }
    ]
}

ERROR = {
    "ResultCode": "Error",
    "Messages": [
        {
            "Summary": "Invalid or missing state/province code (EIU).",
            "Details": "EIU is not a known state or province.",
            "RefersTo": "Addresses[0]",
            "Severity": "Error",
            "Source": "Avalara.AvaTax.Services.Tax"}
    ]
}
