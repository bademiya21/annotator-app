FROM alpine:latest

COPY . /app
WORKDIR /app

RUN apk upgrade --update \
	&& apk add --no-cache python3 openblas musl libgcc libstdc++ \
	&& apk add --no-cache --virtual build-runtime python3-dev gcc gfortran freetype-dev musl-dev openblas-dev g++ \
	&& pip3 install --no-cache-dir numpy \
	&& pip3 install --no-cache-dir -r requirements.txt \
	&& apk del build-runtime

EXPOSE 5000

CMD ["python3", "application.py"]