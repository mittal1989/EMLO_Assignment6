FROM python:3.9-slim-buster

WORKDIR /workspace

RUN pip3 install --no-cache-dir torch==1.12.1 torchvision==0.13.1 --index-url https://download.pytorch.org/whl/cpu \
    && pip3 install gradio==3.36.1

COPY gradio_demo.py .

COPY /model/model.script.pt ./model/

COPY /sample ./sample/

CMD ["python3", "gradio_demo.py"]