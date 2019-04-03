#/bin/bash
cd ./Services/Authentication
python auth_service.py &

cd ./Services/User
python user_service.py &

cd ./Services/Authentication
python auth_service.py &

cd ./Services/Authentication
python auth_service.py &