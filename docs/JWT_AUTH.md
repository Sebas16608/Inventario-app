# 🔐 Guía de Autenticación JWT

## Descripción General

Esta aplicación utiliza **JWT (JSON Web Tokens)** para manejar la autenticación y autorización. Es un estándar seguro, stateless y compatible con aplicaciones modernas.

---

## ¿Cómo Funciona JWT?

```
1. El usuario envía credenciales (username/email + password)
   ↓
2. El servidor valida las credenciales
   ↓
3. El servidor genera dos tokens:
   - Access Token (corta vida: 1 hora)
   - Refresh Token (larga vida: 7 días)
   ↓
4. El cliente almacena ambos tokens
   ↓
5. Para cada request, el cliente envía: Authorization: Bearer <access_token>
   ↓
6. Cuando el access token expira, usa el refresh token para obtener uno nuevo
```

---

## 🚀 Flujo de Autenticación

### 1️⃣ Registro

```bash
curl -X POST http://localhost:8000/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "juan",
    "email": "juan@example.com",
    "password": "mi_contraseña_segura",
    "company": 1
  }'
```

**Respuesta:**
```json
{
  "user": {
    "id": 5,
    "username": "juan",
    "email": "juan@example.com"
  },
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "message": "User registered successfully"
}
```

### 2️⃣ Login (Si el usuario ya existe)

```bash
curl -X POST http://localhost:8000/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "juan",
    "password": "mi_contraseña_segura"
  }'
```

**Respuesta:**
```json
{
  "user": {
    "id": 5,
    "username": "juan",
    "email": "juan@example.com"
  },
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "message": "Login successful"
}
```

### 3️⃣ Usar el Access Token

Ahora puedes usar el `access` token en tus requests:

```bash
curl -X GET http://localhost:8000/auth/users/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
```

### 4️⃣ Refrescar el Access Token (cuando expire)

El access token dura **1 hora**. Cuando expire, usa el refresh token:

```bash
curl -X POST http://localhost:8000/auth/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
  }'
```

**Respuesta:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

---

## 📱 Implementación en Frontend

### JavaScript/React

```javascript
// 1. Registro
const register = async (username, email, password, company) => {
  const response = await fetch('http://localhost:8000/auth/register/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, email, password, company })
  });
  const data = await response.json();
  
  // Guardar tokens
  localStorage.setItem('access_token', data.access);
  localStorage.setItem('refresh_token', data.refresh);
  
  return data;
};

// 2. Login
const login = async (username, password) => {
  const response = await fetch('http://localhost:8000/auth/login/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password })
  });
  const data = await response.json();
  
  // Guardar tokens
  localStorage.setItem('access_token', data.access);
  localStorage.setItem('refresh_token', data.refresh);
  
  return data;
};

// 3. Hacer request autenticado
const makeAuthenticatedRequest = async (url, options = {}) => {
  let accessToken = localStorage.getItem('access_token');
  
  let response = await fetch(url, {
    ...options,
    headers: {
      ...options.headers,
      'Authorization': `Bearer ${accessToken}`,
      'Content-Type': 'application/json'
    }
  });
  
  // Si el token expiró (401), refrescar
  if (response.status === 401) {
    const refreshResponse = await fetch('http://localhost:8000/auth/token/refresh/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ refresh: localStorage.getItem('refresh_token') })
    });
    
    if (refreshResponse.ok) {
      const refreshData = await refreshResponse.json();
      localStorage.setItem('access_token', refreshData.access);
      
      // Reintentar con el nuevo token
      response = await fetch(url, {
        ...options,
        headers: {
          ...options.headers,
          'Authorization': `Bearer ${refreshData.access}`,
          'Content-Type': 'application/json'
        }
      });
    } else {
      // Refresh falló, usuario debe hacer login nuevamente
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      window.location.href = '/login';
    }
  }
  
  return response;
};

// 4. Usar en componentes
const fetchUsers = async () => {
  const response = await makeAuthenticatedRequest('http://localhost:8000/auth/users/');
  const data = await response.json();
  return data;
};
```

### Python

```python
import requests
from datetime import datetime, timedelta

class APIClient:
    def __init__(self, base_url='http://localhost:8000'):
        self.base_url = base_url
        self.access_token = None
        self.refresh_token = None
        self.token_expiry = None
    
    def register(self, username, email, password, company):
        """Register new user"""
        response = requests.post(
            f'{self.base_url}/auth/register/',
            json={'username': username, 'email': email, 'password': password, 'company': company}
        )
        if response.status_code == 201:
            data = response.json()
            self.access_token = data['access']
            self.refresh_token = data['refresh']
            self.token_expiry = datetime.now() + timedelta(hours=1)
        return response.json()
    
    def login(self, username, password):
        """Login user"""
        response = requests.post(
            f'{self.base_url}/auth/login/',
            json={'username': username, 'password': password}
        )
        if response.status_code == 200:
            data = response.json()
            self.access_token = data['access']
            self.refresh_token = data['refresh']
            self.token_expiry = datetime.now() + timedelta(hours=1)
        return response.json()
    
    def _refresh_token(self):
        """Refresh access token"""
        response = requests.post(
            f'{self.base_url}/auth/token/refresh/',
            json={'refresh': self.refresh_token}
        )
        if response.status_code == 200:
            data = response.json()
            self.access_token = data['access']
            self.token_expiry = datetime.now() + timedelta(hours=1)
        return response.json()
    
    def _get_headers(self):
        """Get headers with token"""
        # Si el token va a expirar en menos de 5 minutos, refrescalo
        if self.token_expiry and datetime.now() > self.token_expiry - timedelta(minutes=5):
            self._refresh_token()
        
        return {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
    
    def get(self, endpoint):
        """Make GET request"""
        response = requests.get(
            f'{self.base_url}{endpoint}',
            headers=self._get_headers()
        )
        return response.json()
    
    def post(self, endpoint, data):
        """Make POST request"""
        response = requests.post(
            f'{self.base_url}{endpoint}',
            json=data,
            headers=self._get_headers()
        )
        return response.json()

# Uso
client = APIClient()
client.login('juan', 'contraseña123')
users = client.get('/auth/users/')
print(users)
```

---

## 🔒 Mejores Prácticas de Seguridad

### ✅ QUÉ HACER

1. **Almacenar tokens de forma segura**
   - En navegadores: `localStorage` o `sessionStorage` (considera usar HTTP-only cookies si es posible)
   - En aplicaciones: Almacenar en memoria o archivos cifrados

2. **Refrescar el token antes de que expire**
   - No esperes a que el token expire
   - Refrescalo cuando tenga menos de 5 minutos de vida

3. **Usar HTTPS en producción**
   - Todos los tokens deben transmitirse sobre conexiones seguras

4. **Incluir el token en cada request autenticado**
   - Header: `Authorization: Bearer <token>`

### ❌ QUÉ EVITAR

1. **No guardes tokens en cookies sin HttpOnly**
   - Las cookies son vulnerables a XSS

2. **No incluyas información sensible en tokens**
   - Los tokens pueden ser decodificados

3. **No uses el mismo token para múltiples aplicaciones**
   - Cada aplicación debe tener su propio scope

4. **No expongas el refresh token**
   - Es más crítico que el access token

---

## ⏱️ Configuración de Tiempos

```
Access Token  → Válido por 1 hora
Refresh Token → Válido por 7 días
```

Estos valores se pueden configurar en `settings.py`:

```python
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    ...
}
```

---

## 🐛 Troubleshooting

### "Token is invalid or expired"

```
Significa que el access token expiró.
Solución: Usa el refresh token para obtener uno nuevo.
```

### "Given token not valid for any token type"

```
El token está dañado o es inválido.
Solución: Vuelve a hacer login.
```

### "Invalid token."

```
El header Authorization no es válido.
Asegúrate de usar: Authorization: Bearer <token>
```

---

## 📚 Referencias

- [JWT.io](https://jwt.io)
- [Django REST Framework SimpleJWT](https://django-rest-framework-simplejwt.readthedocs.io/)
- [RFC 7519 - JSON Web Token](https://tools.ietf.org/html/rfc7519)
