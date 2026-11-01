# SNAPSHOT · AUTO BACKUP v1.5

## Estado

**Auto Backup v1.5 terminado y publicado.**

Repositorio:

`https://github.com/CorrosionLabs/Auto-Backup`

Rama principal:

`main`

Release publicada:

`v1.5`

Archivo fuente canónico:

`auto_backup_v15.py`

El ejecutable Windows está publicado como **Asset de la Release v1.5**, no dentro del historial Git.

---

## Funcionalidad actual

Auto Backup realiza copias ZIP de una carpeta seleccionada.

### Backups automáticos

- Carpeta de destino:  
  `Destination/Auto/`

- Nombre:  
  `Backup_YYYY-MM-DD_HH-MM-SS.zip`

- Intervalo configurable en minutos.

- Número máximo de copias configurable.

- Rotación FIFO:  
  al superar el máximo configurado, elimina la copia automática más antigua.

### Backups manuales

Botón:

`Create now`

- Carpeta de destino:  
  `Destination/Manual/`

- Las copias manuales no participan en el FIFO.

- Se consideran permanentes salvo eliminación manual.

- Permiten introducir una descripción opcional.

- La descripción se sanea antes de incorporarse al nombre.

Formato:

`Backup_YYYY-MM-DD_HH-MM-SS_description.zip`

La lógica de creación usa un archivo temporal antes de sustituirlo por el ZIP definitivo.

---

## Interfaz

Tecnología:

- Python

- CustomTkinter

- Pillow

Ventana actual:

`690 × 420`

Estética Corrosion Labs:

- cabecera oscura;

- cuerpo blanco;

- rojo como color de acento;

- diseño compacto;

- logo embebido en Base64.

Cabecera:

`AUTO BACKUP v1.5`

La versión aparece pequeña junto al nombre.

---

## Botones Start / Stop

Estado detenido:

- `Start` negro.

- `Stop` gris.

Estado funcionando:

- `Start` gris/deshabilitado.

- `Stop` negro/activo.

`Start` solo se habilita cuando Source y Destination contienen una ruta. La validación real de las carpetas se mantiene aparte.

---

## Indicador circular

Canvas:

`200 × 200`

Texto centrado en:

`100, 100`

Estados:

- `STOPPED`

- cuenta atrás `MM:SS`

- `SAVING`

El anillo negro sirve como pista y el progreso rojo aumenta conforme transcurre el intervalo.

La imagen del anillo se genera a resolución 4× y se reduce con LANCZOS para evitar bordes dentados.

### SAVING

En la última modificación de v1.5:

- los backups automáticos muestran `SAVING`;

- los backups manuales también muestran `SAVING`;

- `SAVING` parpadea mientras se está generando el ZIP.

No se modificó la lógica de backup para implementar este comportamiento; es únicamente estado visual de la interfaz.

---

## Funcionamiento temporal

Al pulsar `Start`:

1. se ejecuta inmediatamente un backup automático;

2. durante ese proceso aparece `SAVING`;

3. cuando termina, se establece el siguiente deadline;

4. comienza la cuenta atrás;

5. al llegar al siguiente ciclo vuelve a realizarse un backup.

Por tanto, el intervalo se cuenta actualmente **desde el final del backup anterior hasta el comienzo del siguiente**.

---

## Textos

La interfaz principal está en inglés.

Estados inferiores:

- `Stopped`

- `Running`

- `Creating manual snapshot…`

- `Manual snapshot created: ...`

- `Last backup: ...`

Quedan algunos diálogos internos en castellano, especialmente selección y validación de rutas. Esto no se corrigió en v1.5.

---

## GitHub

Estructura publicada:

```
Auto-Backup/├── auto_backup_v15.py├── README.md├── requirements.txt└── img/    ├── cabe_github autobackup.png    ├── folder.ico    └── logo.png
```

`requirements.txt`:

```
customtkinterPillow
```

README incluye descripción, características, requisitos, ejecución y estructura de backups.

Se añadió una imagen de cabecera desde:

`img/cabe_github autobackup.png`

### Flujo Git usado

El repositorio se gestionó desde la terminal de VSCode porque el conector GitHub de ChatGPT tenía acceso de lectura pero no de escritura sobre `CorrosionLabs`.

Repositorio clonado con:

```
git clone https://github.com/CorrosionLabs/Auto-Backup.git
```

Primer commit:

```
git commit -m "Initial release v1.5"
```

Publicación inicial:

```
git push -u origin main
```

---

## exeBuilder

El ejecutable de Auto Backup se generó usando nuestro **exeBuilder v9**.

exeBuilder v9 quedó también considerado terminado antes de continuar con Auto Backup.

No mezclar el desarrollo de exeBuilder con Auto Backup v2 salvo que sea necesario para la compilación.

---

## Punto de partida para Auto Backup v2

La **v1.5 debe considerarse baseline estable**.

Para desarrollar v2:

- partir de `auto_backup_v15.py`;

- conservar intacta la lógica funcional existente salvo decisión explícita;

- trabajar paso a paso;

- una modificación cada vez;

- diagnosticar antes de corregir;

- no introducir refactorizaciones ni nuevas abstracciones sin necesidad;

- mantener la separación `Auto/` y `Manual/`;

- mantener GitHub como repositorio público de Corrosion Labs;

- publicar v2 mediante nueva Release cuando esté terminada.

No hay todavía requisitos funcionales definidos para v2. Deben decidirse en el nuevo chat.
