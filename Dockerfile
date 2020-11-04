FROM movecrew/purplebot:alpine-latest

RUN mkdir /PurpleBot && chmod 777 /PurpleBot
ENV PATH="/PurpleBot/bin:$PATH"
WORKDIR /PurpleBot

RUN git clone https://github.com/thewhiteharlot/PurpleBot -b sql-extended /PurpleBot

#
# Copies session and config(if it exists)
#
COPY ./sample_config.env ./userbot.session* ./config.env* /PurpleBot/

#
# Finalization
#
CMD ["python3","-m","userbot"]
