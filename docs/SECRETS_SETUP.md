# Guía de Configuración de GitHub Secrets

Esta guía te ayudará a configurar todos los secrets necesarios para que el pipeline de CI/CD funcione correctamente.

## Secrets Requeridos

### 1. Docker Hub

Necesarios para build y push de imágenes Docker.

**DOCKER_USERNAME**
- Tu nombre de usuario de Docker Hub
- Ejemplo: `miusuario`

**DOCKER_PASSWORD**
- Tu password o Access Token de Docker Hub
- **Recomendado**: Usar Access Token en lugar de password
- Generar en: https://hub.docker.com/settings/security

### 2. SonarQube

Necesarios para análisis de calidad de código.

**SONAR_TOKEN**
- Token de autenticación de SonarQube
- Generar en: SonarQube → My Account → Security → Generate Token

**SONAR_HOST_URL**
- URL de tu servidor SonarQube
- Ejemplos:
  - Local: `http://localhost:9000`
  - Cloud: `https://sonarcloud.io`
  - Self-hosted: `https://sonar.tu-dominio.com`

### 3. Variables de Aplicación

**MONGO_ROOT_USER**
- Usuario root de MongoDB
- Ejemplo: `admin`

**MONGO_ROOT_PASSWORD**
- Password del usuario root de MongoDB
- Generar un password seguro: https://passwordsgenerator.net/

**JWT_SECRET**
- Secreto para firmar tokens JWT
- Debe ser un string aleatorio largo y seguro
- Generar con: `openssl rand -hex 32`
- Ejemplo: `a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6`

### 4. Deploy a Producción (Opcional)

Solo si vas a usar deploy automático a producción.

**SSH_PRIVATE_KEY**
- Clave SSH privada para conectar al servidor
- Generar par de claves:
  ```bash
  ssh-keygen -t rsa -b 4096 -C "github-actions"
  ```
- Copiar clave pública al servidor:
  ```bash
  ssh-copy-id usuario@servidor
  ```
- Copiar clave privada completa (incluye BEGIN y END)

**PRODUCTION_HOST**
- IP o dominio del servidor de producción
- Ejemplo: `192.168.1.100` o `prod.tu-dominio.com`

**PRODUCTION_USER**
- Usuario SSH del servidor
- Ejemplo: `ubuntu`, `deployer`, etc.

**PRODUCTION_URL**
- URL pública de tu aplicación
- Ejemplo: `https://api.tu-dominio.com`

## Cómo Configurar los Secrets en GitHub

### Paso 1: Ir a Settings
1. Ve a tu repositorio en GitHub
2. Click en **Settings** (⚙️)
3. En el menú lateral, selecciona **Secrets and variables** → **Actions**

### Paso 2: Añadir Secrets
1. Click en **New repository secret**
2. En **Name**: Escribe el nombre EXACTO del secret (ej: `DOCKER_USERNAME`)
3. En **Secret**: Pega el valor del secret
4. Click en **Add secret**
5. Repite para cada secret

### Paso 3: Verificar
- Verifica que todos los secrets estén añadidos
- Los nombres deben coincidir exactamente con los del workflow
- Los secrets no se pueden ver una vez guardados (solo editar/eliminar)

## Secrets por Environment

Si usas environments (staging, production), puedes configurar secrets específicos:

### Para Staging
1. Settings → Environments → New environment
2. Nombre: `staging`
3. Añade secrets específicos de staging

### Para Production
1. Settings → Environments → New environment
2. Nombre: `production`
3. Añade protección: Require reviewers
4. Añade secrets específicos de producción

## Verificación

### Test de Docker Hub
```bash
docker login -u $DOCKER_USERNAME -p $DOCKER_PASSWORD
```

### Test de SonarQube
```bash
curl -u $SONAR_TOKEN: $SONAR_HOST_URL/api/authentication/validate
```

### Test de SSH
```bash
ssh -i private_key $PRODUCTION_USER@$PRODUCTION_HOST
```

## Seguridad

### ✅ Buenas Prácticas
- ✅ Usa Access Tokens en lugar de passwords
- ✅ Rota los secrets regularmente
- ✅ Usa secrets diferentes para staging y production
- ✅ No compartas secrets en código o commits
- ✅ Revoca inmediatamente si un secret se expone
- ✅ Usa nombres descriptivos para los secrets

### ❌ NO Hacer
- ❌ No hardcodees secrets en el código
- ❌ No compartas secrets en Slack/Discord
- ❌ No uses el mismo secret en múltiples proyectos
- ❌ No uses passwords débiles
- ❌ No commits secrets en .env al repositorio

## Troubleshooting

### El workflow no encuentra un secret
- Verifica que el nombre sea EXACTO (case-sensitive)
- Verifica que el secret esté en el scope correcto (repo/environment)

### Docker login falla
- Verifica que las credenciales sean correctas
- Si usas 2FA, debes usar un Access Token

### SonarQube falla
- Verifica que el SONAR_HOST_URL sea accesible
- Verifica que el token tenga permisos correctos

### SSH falla
- Verifica que la clave privada esté completa
- Verifica que el formato incluya BEGIN/END
- Verifica que la clave pública esté en el servidor

## Recursos Adicionales

- [GitHub Actions Secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
- [Docker Access Tokens](https://docs.docker.com/docker-hub/access-tokens/)
- [SonarQube Authentication](https://docs.sonarqube.org/latest/user-guide/user-token/)
- [SSH Key Generation](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent)
