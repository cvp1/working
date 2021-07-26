docker build --tag cvande/sms/dynapp2 .
docker run -d -p 5001:5000 cvande/sms/dynapp2 
docker ps
