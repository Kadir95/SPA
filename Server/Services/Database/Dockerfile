FROM python:3
ENV SPACONTAINER=database_service
EXPOSE 7000
RUN mkdir -p /Server/Services/Database/
COPY /Server/Services/Database/ Server/Services/Database/
COPY /Server/Lib Server/Lib
RUN echo "nameserver" > /etc/resolv.conf 
RUN apt update
RUN apt install -y libzbar-dev
RUN pip install $(cat /Server/Services/Database/config/libraries)
RUN pip install $(cat /Server/Lib/config/libraries)
CMD [ "python", "/Server/Services/Database/database_service.py", "&>", "/Server/output" ]