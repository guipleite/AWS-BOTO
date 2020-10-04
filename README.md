# AWS-BOTO

### Instalar a biblioteca boto3 no python:
``` 
pip3 install boto3
```

### Instalar o client da AWS:
```
sudo apt  install awscli 
```
  ou
```
sudo snap install aws-cli --classic
```
### Configurar o client:
```
aws configure
```
- AWS Access Key ID : <!seu access key id>

- AWS Secret Access Key : <!sua secret access key>

- Default region name : us-east-1

### Rodar o script de criação:
```
python3 ap3.py
```

### Listar todas as tarefas:
```
< IP do LoadBalancer >/todo/api/tasks/
```
### Mostrar uma tarefa especifica:
```
< IP do LoadBalancer >/todo/api/tasks/< id >
```

### Apagar tudo que foi criado:
```
python3 nuke.py
```

### Os scripts de instalação, serviços e aplicação client estão disponíveis no repositório:
https://github.com/guipleite/FLASK_REST
