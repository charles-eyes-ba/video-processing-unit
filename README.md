# Video Processing Unit - VPU

The Video Processing Unit (A.k.a VPU) is the module that run the classification algorithms on the video feeds.

## Application Architecture 
<br/>
<p align="center">
  <img src="imgs/vpu.arch.png">
</p>

## Configuration
Create a `.env` file following the `.env.example` file.

## Iniciando
To start the VPU you must run the following command
```shell
python main.py
```

## Application Server APIs

É necessário duas _requests_ para interagir com o servidor de aplicação, uma para leitura e outra envio de dados.

- Read data:
    - Method: GET
    - Reponse: cameras URL and IDs

- Send data:
    - Method: POST
    - Body: camera id, camera width, camera height, boxes, scores and classes 