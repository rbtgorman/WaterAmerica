import urllib.request
import xml.etree.ElementTree as ET

class AddressValidator():
    def __init__(self, Street_Address2, City, State, Zip5):
        self.Street_Address2 = Street_Address2
        self.City = City
        self.State = State
        self.Zip5 = Zip5

    def __repr__(self): 
        return f'({self.Street_Address2}, {self.City}, {self.State}, {self.Zip5})'

    def __str__(self):
        return self.__repr__()

    def generate_parse_tree(self):
        Address1 = None
      
        address_list = [
            self.Street_Address2.upper(),
            self.City.upper(),
            self.State.upper(),
            self.Zip5.upper()
        ]

        requestXML = f'''
        <?xml version="1.0"?>
        <AddressValidateRequest USERID="487RUTGE6377">
            <Revision>1</Revision>
            <Address ID="0">
                <Address1>{Address1}</Address1>
                <Address2>{self.Street_Address2}</Address2>
                <City>{self.City}</City>
                <State>{self.State}</State>
                <Zip5>{self.Zip5}</Zip5>
            <Zip4/>
            </Address>
        </AddressValidateRequest>
        '''

        docString = requestXML.replace('\n','').replace('\t','')
        docString = urllib.parse.quote_plus(docString)
        url = "http://production.shippingapis.com/ShippingAPI.dll?API=Verify&XML=" + docString

        response = urllib.request.urlopen(url)
        if response.getcode() != 200:
            print("Error making HTTP call:")
            print(response.info())
            return None, None

        contents = response.read()
        return address_list, ET.fromstring(contents)

    def validate_street_address(self):
        address_list, root = self.generate_parse_tree()
        if root is None:
            return False
        for address in root.findall('Address'):
            street_address = address.find("Address2")
            if street_address is not None and street_address.text:
                return address_list[0] == street_address.text
        return False
            
    def validate_city(self):
        address_list, root = self.generate_parse_tree()
        if root is None:
            return False
        for address in root.findall('Address'):
            city = address.find("City")
            if city is not None and city.text:
                return address_list[1] == city.text
        return False

    def validate_state(self):
        address_list, root = self.generate_parse_tree()
        if root is None:
            return False
        for address in root.findall('Address'):
            state = address.find("State")
            if state is not None and state.text:
                return address_list[2] == state.text
        return False

    def validate_zip_code(self):
        address_list, root = self.generate_parse_tree()
        if root is None:
            return False
        for address in root.findall('Address'):
            zip_code = address.find("Zip5")
            if zip_code is not None and zip_code.text:
                return address_list[3] == zip_code.text
        return False
    
    def validate_address(self):
        return self.validate_street_address() and self.validate_city() and self.validate_state() and self.validate_zip_code()

# Only run tests if this script is run directly
if __name__ == "__main__":
    # Test with incorrect address
    wrong_address = AddressValidator("12 Stern Light Drive", "Camden", "NJ", "08054")
    print(f"Wrong Address Validation: {wrong_address.validate_address()}")

    # Test with correct address
    correct_address = AddressValidator("12 Stern Light Dr", "Mount Laurel", "NJ", "08054")
    print(f"Correct Address Validation: {correct_address.validate_address()}")