#include <stdio.h>
#include <stdlib.h>
#include <memory.h>
#include <time.h>
#include <malloc.h>
#include <stdbool.h>


struct Laberinto {
	int dimension, alto, ancho;
	unsigned int obstaculosAleatorios;
	int posicionInicialY, posicionInicialX;
	int objetivoX, objetivoY;
	int cantidadObstaculosFijos;
	int* indicesObstaculosFijos;
};

/**
 * Ba'haal the end of line eater
 * Come todo hasta la siguiente linea.
 * Si la siguiente linea contiene un EOF al inicio, tambien lo come.
 */
void comerFinalesDeLinea(FILE * archivo) {
	int c;
	while ((c = fgetc(archivo)) == '\r' || c == '\n') {
		if(c == '\r') {
			fgetc(archivo);// come el \n
		}
	}
	if (c != EOF) {
		ungetc(c, archivo);
	}
}

/**
 * Desde la posicion actual en el archivo mueve el indicador de posicion del stream
 * a la primera posicion de la linea siguiente.
 * Si la primera posicion de la linea siguiente es EOF, el EOF sera leido, pero no devuelto al stream.
 */
void comerLinea(FILE * archivo) {
	fscanf(archivo, "%*[^\n]");
	comerFinalesDeLinea(archivo);
}

/**
 * Lee la entrada del archivo a un struct Informacion pasado por puntero.
 */
void leerEntrada(struct Laberinto* info, char * nombreEntrada) {
	FILE *entrada = fopen(nombreEntrada, "r");

	fscanf(entrada, "%*[^0123456789]%d", &(info->dimension));
	comerFinalesDeLinea(entrada);
	info->alto = info->dimension;
	info->ancho = info->dimension+1;

	comerLinea(entrada);


	info->indicesObstaculosFijos = reallocarray(NULL, info->alto * info->ancho + 1, sizeof(int));

	info->cantidadObstaculosFijos = 0;
	while(getc(entrada) == '(') {
		int x, y;
		fscanf(entrada, "%d,%d)", &y, &x);
		comerFinalesDeLinea(entrada);

		x--; y--;//La entrada empieza en 1

		if(x < 0 || info->dimension <= x || y < 0 || info->dimension <= y) {
			continue;
		}

		info->indicesObstaculosFijos[info->cantidadObstaculosFijos++] = y * info->ancho + x;
	}

	info->indicesObstaculosFijos = reallocarray(info->indicesObstaculosFijos, info->cantidadObstaculosFijos, sizeof(int));


	fscanf(entrada, "%*[^0123456789]%d", &info->obstaculosAleatorios);

	fscanf(entrada, "%*[^(](%d,%d)", &info->posicionInicialY, &info->posicionInicialX);
	info->posicionInicialX--; info->posicionInicialY--;//La entrada empieza en 1

	fscanf(entrada, "%*[^(](%d,%d)", &info->objetivoY, &info->objetivoX);
	info->objetivoX--;info->objetivoY--;//La entrada empieza en 1

	fclose(entrada);
}

/**
 * Dada una probabilidad devuelve un boolean que es true con esa probabilidad
 * Para evitar errores de redondeo la probabilidad debe estar en formato Q1.14
 * Garantia si probabilidad es >= 1 la funcion es constante y devuelve true
 *
 * Atencion: srand() debe haber sido llamado
 */
bool booleanAzaroso(unsigned int probabilidad) {
	static const unsigned int uno = 1 << 14;// 01,00 0000 0000 0000 es un 1 con 14 ceros despues de la coma

	return (rand() % uno) < probabilidad;
}

/**
 * USO TrabajoFinal2019 <ruta entrada> [-s <semilla>]
 */
int main(int argsc, char * argsv[]) {
	char * nombreEntrada = argsv[1];
	long semilla;
	if(argsc < 4) {
		semilla = time(NULL);
	} else {
		semilla = strtol(argsv[3], NULL, 10);
	}

	struct Laberinto* info = malloc(sizeof(struct Laberinto));
	leerEntrada(info, nombreEntrada);

	char* buffer = calloc(info->alto*info->ancho + 1, sizeof(char));

	unsigned int cantidadCasilleros = info->dimension*info->dimension;//casilleros en la grilla
	unsigned int cantidadEspaciosUsados = 1 + 1 + info->cantidadObstaculosFijos;
	unsigned int cantidadEspaciosLibres = cantidadCasilleros - cantidadEspaciosUsados;

	srand(semilla);
	for (int i = 0; i < info->alto*info->ancho; ) {
		for (int j = 0; j < info->ancho-1; ++j) {
			if(buffer[i] == '1') {
				i++;//obstaculo fijo
			} else if(i == info->posicionInicialY * info->ancho + info->posicionInicialX) {
				buffer[i++] = 'I';
			} else if(i == info->objetivoX * info->ancho + info->objetivoY) {
				buffer[i++] = 'X';
			} else if(info->obstaculosAleatorios > 0) {
				//Opero con coma fija para evitar errores de redondeo y underflow
				unsigned int sft = info->obstaculosAleatorios << 14;// la coma esta ahora entre el bit 14 y 15
				unsigned int probabilidadObstaculoAleatorio = sft/cantidadEspaciosLibres;// esta es una division fixed point, con 14 bits de presicion decimal

				if(booleanAzaroso(probabilidadObstaculoAleatorio)) {
					info->obstaculosAleatorios--;
					buffer[i++] = '1';
				} else {
					buffer[i++] = '0';
				}

				cantidadEspaciosLibres--;//como ya se que el espacio contine/no contiene un obstaculo, los casilleros siguientes tienen otra probabilidad
			} else {
				buffer[i++] = '0';
			}
		}
		buffer[i++] = '\n';
	}

	FILE* salida = fopen("salida_intermedia.txt", "w");
	fwrite (buffer , sizeof(char), info->alto*info->ancho, salida);
	fclose(salida);

	free(buffer);
	free(info->indicesObstaculosFijos);
	free(info);
	return 0;
}