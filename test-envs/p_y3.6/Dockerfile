FROM k1lib_test_base
RUN source ~/.bashrc && conda install python=3.6 && conda install pytorch torchvision cpuonly -c pytorch
COPY requirements.txt requirements.txt
RUN source ~/.bashrc && conda install ruamel.yaml && pip install Cython && conda install --file requirements.txt
RUN source ~/.bashrc && conda install dill pillow graphviz
#>>log 2>>log
CMD source ~/.bashrc && ./cmd.sh

