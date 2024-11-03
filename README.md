# ASS_Architecture-MS
# 📚 Book Collection Manager

## Descriere
**Book Collection Manager** este o aplicație pe bază de microservicii care permite utilizatorilor să gestioneze o colecție de cărți. Utilizatorii pot:
- Să se înregistreze și să se autentifice
- Să adauge, editeze și șteargă cărți

Aceasta oferă o experiență completă de gestionare a colecției de cărți într-un mod distribuit și modular.

---

## Microservicii

Aplicația este formată din mai multe microservicii, fiecare având o responsabilitate specifică:

### 1. 📖 Book Management Service
- **Rol**: Gestionează operațiunile CRUD pentru cărți (Create, Read, Update, Delete).
- **Tehnologii**: Flask, SQLite, Docker.

### 2. 🔑 User Authentication Service
- **Rol**: Gestionează înregistrarea, autentificarea și sesiunea utilizatorilor.
- **Tehnologii**: Flask, Flask-Login, Flask-Bcrypt, SQLite, Docker.

### 3. 📢 Notification Service
- **Rol**: Trimite notificări despre evenimente legate de cărți, cum ar fi adăugarea sau ștergerea acestora.
- **Tehnologii**: Flask, RabbitMQ, Docker.

### 4. 🌐 Facade Service (API Gateway)
- **Rol**: Servește ca un API gateway, redirecționând cererile către microserviciul corespunzător.
- **Tehnologii**: Flask, Docker.

---

## Instrucțiuni de Rulare

Pentru a rula aplicația local, urmează pașii de mai jos:

1. Asigură-te că ai instalat [Docker](https://www.docker.com/get-started) și [Docker Compose](https://docs.docker.com/compose/install/) pe mașina ta.

2. Utilizează comanda pentru a rula, din directoriul proiectului:

   ```bash
   docker-compose up --build
