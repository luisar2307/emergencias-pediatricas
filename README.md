# Sistema de Emergencias Médicas Pediátricas

## 1. Requisitos previos (cada persona instala en su equipo)

- Python 3.12+
- PostgreSQL 16 instalado localmente (https://www.postgresql.org/download/)
- Git

## 2. Clonar el repositorio

```bash
git clone git@github.com:TU-ORG/emergencias-pediatricas.git
cd emergencias-pediatricas
```

Si es tu primera vez usando SSH con GitHub, configura tu llave:
```bash
ssh-keygen -t ed25519 -C "tu-email@ejemplo.com"
cat ~/.ssh/id_ed25519.pub
```
Copia esa clave en GitHub → Settings → SSH and GPG keys → New SSH key.

## 3. Crear entorno virtual

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
```

## 4. Configurar PostgreSQL local

Cada desarrollador crea su propia base de datos local (no se comparte servidor):

```bash
psql -U postgres
CREATE DATABASE emergencias_db;
\q
```

## 5. Configurar variables de entorno

```bash
cp .env.example .env
```

Edita `.env` con tu usuario/contraseña de PostgreSQL local. Este archivo NUNCA se sube a GitHub (ya está en `.gitignore`).

## 6. Migrar y correr el proyecto

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

---

## 7. Flujo de trabajo con Git (obligatorio para todo el equipo)

### Ramas

- `main` → producción, protegida.
- `develop` → integración, base del sprint actual.
- `feature/nombre-tarea` → una rama por tarea.

### Trabajar en una tarea

```bash
git checkout develop
git pull origin develop
git checkout -b feature/nombre-de-tu-tarea
```

Trabajas, guardas avances con commits frecuentes:

```bash
git add .
git commit -m "feat(patients): agrega modelo Tutor"
git push origin feature/nombre-de-tu-tarea
```

### Cambiar de dispositivo (casa/oficina/laptop)

Antes de cerrar tu sesión de trabajo, siempre:
```bash
git add .
git commit -m "wip: avance parcial"
git push origin feature/nombre-de-tu-tarea
```

En el otro dispositivo:
```bash
git clone git@github.com:TU-ORG/emergencias-pediatricas.git   # si es la primera vez ahí
cd emergencias-pediatricas
git checkout feature/nombre-de-tu-tarea
git pull origin feature/nombre-de-tu-tarea
```

Repites los pasos 3-6 de este README para levantar tu entorno local en esa máquina (venv y PostgreSQL son locales a cada equipo).

### Antes de abrir un Pull Request

```bash
git fetch origin
git rebase origin/develop
git push origin feature/nombre-de-tu-tarea --force-with-lease
```

Luego en GitHub: **Pull Request** → base `develop` ← compare `feature/nombre-de-tu-tarea`.

### Reglas de commits

```
feat: nueva funcionalidad
fix: corrección de bug
refactor: cambio sin alterar comportamiento
test: agregar o modificar tests
docs: documentación
```

### Reglas de Pull Request

- Un PR = una tarea/ticket. Nunca mezclar cambios de dos apps distintas.
- Requiere mínimo 1 aprobación.
- El DBA aprueba cualquier PR que modifique `models.py` o migraciones.
- El CI (lint + tests) debe pasar en verde antes de mergear.
- Si tocas `models.py`, avisa en el canal del equipo antes de correr `makemigrations` para evitar migraciones duplicadas/conflictivas.

## 8. Estructura del proyecto

```
config/       settings, urls, wsgi/asgi
accounts/     Usuario custom, autenticación
staff/        PersonalMedico, Rol, Turno
patients/     Paciente, Tutor, AntecedenteMedico
triage/       AtencionTriaje, Sintoma, SignoVital, NivelUrgencia
core/         utilidades comunes, mixins
api/          serializers y routers DRF
```
## 9. EXTENSIONES PARA EL VISUAL STUDIO COTE (OPCIONALES)
```
GitLens       Para saber quien cambia partes del repositorio y colaborar mas
Code Spell Checker (idioma)        Detecta errores ortograficos en el codigo 
Ridiculous Coding        Lo hace mas chistoso y con soniditos
```