import pyotp

class OTP:

    def __init__(self,secret) -> None:
        self.totp = pyotp.TOTP(secret)

    def create(self,username:str)->str:
        try:
            return self.totp.provisioning_uri(name=username, issuer_name='UtsavApi')
        except Exception as e:
            raise Exception(str(e))
    
    def verify(self,otp:str)->bool:
        try:
            print(self.totp.now())
            return self.totp.verify(otp)
        except Exception as e:
            raise Exception(str(e))

