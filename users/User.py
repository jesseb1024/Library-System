class User:
    def __init__(self, name, phone, mail):
        self.name = name
        self.phone = phone
        self.mail = mail

    def parse_user_details(self, details_str):
        try:
            user_details_in_list = details_str.split(" ")
            if len(user_details_in_list) != 3:
                raise ValueError("The input string must contain exactly three parts: name, phone, and mail.")
            self.name = user_details_in_list[0]
            self.phone = user_details_in_list[1]
            self.mail = user_details_in_list[2]
        except Exception as e:
            print(f"Error parsing user details: {e}")

    def __str__(self):
        return f"Name: {self.name}, Phone: {self.phone}, Mail: {self.mail}"
