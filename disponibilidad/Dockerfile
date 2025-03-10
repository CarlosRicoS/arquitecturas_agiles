FROM alpine:3.18

RUN apk update && apk add --no-cache curl bash

WORKDIR /app

COPY run_experimento.sh .

RUN chmod +x run_experimento.sh

CMD ["bash", "run_experimento.sh"]