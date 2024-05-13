# CRT_project

Proyecto de asignatura CRT. Las funcionalidades del código de este proyecto se dividen en dos partes. La primera parte contiene el código que se usa para leer los datos del circuito electrónico. Se configuran las GPIOs de la Raspberry y se leen del pulsador y el sensor de temperatura y humedad. Las pulsaciones del botón se leen mediante interrupciones y si se registra una pulsación se cambia el estado de los LEDs y se cambia la información mostrada en pantalla. También se inicializa un bloque de memoria compartida en la que se escriben las mediciones del sensor.

La segunda parte contiene el código para ejecutar el servidor OPC-UA que lee los datos escritos en la memoria compartida y el cliente que se conecta al servidor y leer esa información. Tanto servidor como cliente deben estar conectados a la misma red y el cliente puede acceder a los datos en forma de objetos de dato del servidor. Para facilitar el acceso al servidor y a los datos del cliente, el código del cliente se ejecuta con una GUI interactiva y fácil de usar.

## Primeros pasos

Una copia de este repo contiene todos los scripts y ejemplos necesarios para leer los datos del circuito y para ejecutar el servidor y el cliente. Sin embargo, no es un proyecto autocontenido, por lo que las librerías y paquetes necesarios para que funcion se deben descargar por separado.

### Prerequisitos

Para poder ejecutar los scripts y ejemplos de este proyecto se requiere que los siguientes paquetes hayan sido instalados previamente.
- [WiringPi](https://github.com/WiringPi/WiringPi)

<details><summary><b>Show instructions</b></summary>

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

<details><summary><b>Show instructions</b></summary>

1. Actualizar pip:

 ```sh
 pip install --upgrade pip
 ````

2. Instalar paquete:

```sh
pip install RPi.GPIO
```

</details>


### Installing

A step by step series of examples that tell you how to get a development
environment running

Say what the step will be

    Give the example

And repeat

    until finished

End with an example of getting some data out of the system or using it
for a little demo

## Running the tests

Explain how to run the automated tests for this system

### Sample Tests

Explain what these tests test and why

    Give an example

### Style test

Checks if the best practices and the right coding style has been used.

    Give an example

## Deployment

Add additional notes to deploy this on a live system

## Built With

  - [Contributor Covenant](https://www.contributor-covenant.org/) - Used
    for the Code of Conduct
  - [Creative Commons](https://creativecommons.org/) - Used to choose
    the license

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code
of conduct, and the process for submitting pull requests to us.

## Versioning

We use [Semantic Versioning](http://semver.org/) for versioning. For the versions
available, see the [tags on this
repository](https://github.com/PurpleBooth/a-good-readme-template/tags).

## Authors

  - **Billie Thompson** - *Provided README Template* -
    [PurpleBooth](https://github.com/PurpleBooth)

See also the list of
[contributors](https://github.com/PurpleBooth/a-good-readme-template/contributors)
who participated in this project.

## License

This project is licensed under the [CC0 1.0 Universal](LICENSE.md)
Creative Commons License - see the [LICENSE.md](LICENSE.md) file for
details

## Acknowledgments

  - Hat tip to anyone whose code is used
  - Inspiration
  - etc
