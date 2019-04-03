FROM python:3
ENV SPACONTAINER=auth_service
EXPOSE 7000
RUN mkdir -p /Server/Services/Authentication/
COPY /Server/Services/Authentication/ Server/Services/Authentication/
COPY /Server/Lib Server/Lib
RUN echo "nameserver" > /etc/resolv.conf 
RUN apt update
RUN apt install -y libzbar-dev
RUN pip install $(cat /Server/Services/Authentication/config/libraries)
RUN pip install $(cat /Server/Lib/config/libraries)
CMD [ "python", "/Server/Services/Authentication/auth_service.py", "&>", "/Server/output" ]