# CRT_project

Proyecto de asignatura CRT. Las funcionalidades del código de este proyecto se dividen en dos partes. La primera parte contiene el código que se usa para leer los datos del circuito electrónico. Se configuran las GPIOs de la Raspberry y se leen del pulsador y el sensor de temperatura y humedad. Las pulsaciones del botón se leen mediante interrupciones y si se registra una pulsación se cambia el estado de los LEDs y se cambia la información mostrada en pantalla. También se inicializa un bloque de memoria compartida en la que se escriben las mediciones del sensor.

La segunda parte contiene el código para ejecutar el servidor OPC-UA que lee los datos escritos en la memoria compartida y el cliente que se conecta al servidor y leer esa información. Tanto servidor como cliente deben estar conectados a la misma red y el cliente puede acceder a los datos en forma de objetos de dato del servidor. Para facilitar el acceso al servidor y a los datos del cliente, el código del cliente se ejecuta con una GUI interactiva y fácil de usar. Ademas de este primer cliente que se comparte en el repositorio (https://github.com/FreeOpcUa/opcua-client-gui) se dispone de un segundo cliente el cual corriendo en paralelo con un script de python es capaz de mostrar unas graficas donde se muestra la fluctuacion de los datos telemetricos publicados.

## Primeros pasos

Una copia de este repo contiene todos los scripts y ejemplos necesarios para leer los datos del circuito y para ejecutar el servidor y el cliente. Sin embargo, no es un proyecto autocontenido, por lo que las librerías y paquetes necesarios para que funcion se deben descargar por separado.

### Prerequisitos

Para poder ejecutar los scripts y ejemplos de este proyecto se requiere que los siguientes paquetes hayan sido instalados previamente.

- [WiringPi](https://github.com/WiringPi/WiringPi)

<details><summary><b>Mostrar instrucciones</b></summary>

1. Actualizar paquete apt:

```sh
sudo apt-get update
````

2. Clonar repositorio WiringPi:

```sh
git clone https://github.com/WiringPi/WiringPi
````

3. Cambiar al repositorio y ejecutar:

```sh
cd WiringPi
./build
```

</details>

- [RPi.GPIO](http://sourceforge.net/projects/raspberry-gpio-python/)

<details><summary><b>Mostrar instrucciones</b></summary>

1. Actualizar pip:

 ```sh
 pip install --upgrade pip
 ````

2. Instalar paquete:

```sh
pip install RPi.GPIO
```

</details>

- [Open62541]](https://github.com/open62541/open62541)

<details><summary><b>Mostrar instrucciones</b></summary>

1. Instalar con CMake:

 ```sh
 sudo apt install cmake
 ````

2. Generar carpeta de build:

```sh
cd open62541 | mkdir build
```


3. Cambiar el CMakeLists.txt y habilitar UA_ENABLE_AMALGAMATION :

 ```sh
 option(UA_ENABLE_AMALGAMATION "Concatenate the library to a single file open62541.h/.c" OFF) ->
 option(UA_ENABLE_AMALGAMATION "Concatenate the library to a single file open62541.h/.c" ON)
 ````

2. Dentro de la carpeta build:

```sh
cmake .. | make
```
Aun asi, los archivos fuente que se usan el repositorio para generar aplicaciones OPC-UA  estan junto a los fuentes con los nombres open62541.c/.h .
</details>

### Instalación

Lo único que hay que hacer para instalar este proyecto es clonar el repositorio en local.

    git clone https://github.com/AitorSalazar/CRT_project.git

## Ejecución de los ejemplos de medición

Los scripts para leer los datos del sensor se encuentran en la carpeta `Signal_Generation`. Se han desarrollado y testeado varias variantes del código. Los dos ejemplos principales y completamente funciones se encuentran en las subcarpetas `RPI.GPIO` y `WiringPi`. Ambas se usan para acceder a los GPIOs y la primera contiene el código escrito en Python mientras que la segunda lo tiene escrito en C++. La elección de lenguajes orientados a objetos es debido a que la librería para comunicarse con el sensor utiliza objetos.

Para ejecutar el ejemplo escrito en Python,

    cd Signal_Generation/RPI.GPIO/
    python measure_irq_shm.py

Para ejecutar el ejemplo escrito en C++,

    cd Signal_Generation/WiringPi/
    ls

Si el ejecutable no se encuentra en el directorio:

    g++ -I. measureC_irq_shm.cpp DHT.cpp -o MeasureExecutable -lwiringPi

Ejecutar el ejemplo,

    ./MeasureExecutable


## Authors

  - **Christopher Carmona** [ChrisCarmona11](https://github.com/ChrisCarmona11)
  - **Aitor Salazar** [AitorSalazar](https://github.com/AitorSalazar)


## License

Este proyecto está licenciado bajo licencia [GNU Genereal Public License v3.0](LICENSE.md)
Licencia Creative Commons - ver [LICENSE.md](LICENSE.md) para más detalles.
