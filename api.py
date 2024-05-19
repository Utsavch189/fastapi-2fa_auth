from sendmail import SendMail
from otp import OTP
import json
from fastapi import FastAPI,Response,Request
from fastapi.middleware.cors import CORSMiddleware
import multiprocessing

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

#dummy user object

class User:
    username='utsav'
    password=1234
    email='utsavchatterjee71@gmail.com'

@app.post('/2fa-login/')
async def login(request:Request):
    try:
        body=await request.body()
        data=json.loads(body.decode())
        username=data.get('username')
        password=data.get('password')

        # simualate login

        if User.username==username and User.password==password:
            # use username as secrets for user by supposing that they are unique
            otp=OTP(username)

            subject='Two Factor Authentication'
            body='Scan The QR in your authenticator app!'
            p=multiprocessing.Process(
                target=SendMail.send_qr,
                args=(
                    subject,
                    username,
                    body,
                    User.email,
                    otp
                )
            )
            p.start()

            return Response(content=json.dumps({
            "message":"Email sent!"
        },indent=4),status_code=200)

        return Response(content=json.dumps({
            "message":"wrong credentials!"
        },indent=4),status_code=400)
    
    except Exception as e:
        content={
            "message":str(e)
        }
        return Response(content=json.dumps(content),status_code=500) 


@app.post('/2fa-verify/')
async def verify(request:Request):
    try:
        body=await request.body()
        data=json.loads(body.decode())
        token=data.get('otp')
        username=data.get('username')
        otp=OTP(username)
        if(otp.verify(str(token).strip())):
            return Response(content=json.dumps({
            "message":"logged in!"
        },indent=4),status_code=200)

        return Response(content=json.dumps({
            "message":"wrong otp!"
        },indent=4),status_code=400)
    
    except Exception as e:
        content={
            "message":str(e)
        }
        return Response(content=json.dumps(content),status_code=500)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)