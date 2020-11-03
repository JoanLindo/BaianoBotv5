FROM movecrew/one4ubot:alpine-latest

RUN mkdir /One4uBot && chmod 777 /One4uBot
ENV PATH="/One4uBot/bin:$PATH"
WORKDIR /One4uBot

RUN git clone https://github.com/thewhiteharlot/PurpleBot -b sql-extended /PurpleBot

#
# Copies session and config(if it exists)
#
COPY ./sample_config.env ./userbot.session* ./config.env* /PurpleBot/

#
# Finalization
#
CMD ["python3","-m","userbot"]
