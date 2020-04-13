FROM lambci/lambda:build-python3.6
RUN mkdir -p /python/
COPY app/requirements.txt /python/
RUN pip install --upgrade pip
RUN pip install -r /python/requirements.txt -t /python/
RUN pip list -o
RUN echo "Built the following: "
RUN ls /python
CMD ["/bin/bash"]