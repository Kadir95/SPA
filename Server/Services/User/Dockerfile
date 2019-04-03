FROM python:3
ENV SPACONTAINER=user_service
EXPOSE 7000
RUN mkdir -p /Server/Services/User/
COPY /Server/Services/User/ Server/Services/User/
COPY /Server/Lib Server/Lib
RUN echo "nameserver" > /etc/resolv.conf 
RUN apt update
RUN apt install -y libzbar-dev
RUN pip install $(cat /Server/Services/User/config/libraries)
RUN pip install $(cat /Server/Lib/config/libraries)
CMD [ "python", "/Server/Services/User/user_service.py", "&>", "/Server/output" ]