FROM python:3
ENV SPACONTAINER=file_service
EXPOSE 7000
RUN mkdir -p /Server/Services/File/
COPY /Server/Services/File/ Server/Services/File/
COPY /Server/Lib Server/Lib
RUN echo "nameserver" > /etc/resolv.conf 
RUN apt update
RUN apt install -y libzbar-dev
RUN pip install $(cat /Server/Services/File/config/libraries)
RUN pip install $(cat /Server/Lib/config/libraries)
CMD [ "python", "/Server/Services/File/file_service.py", "&>", "/Server/output" ]