FROM themattrix/tox-base
ADD . .
RUN tox
