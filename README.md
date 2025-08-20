# 🚀 Dashboard Finance

Une application Python backend moderne pour agréger et visualiser des données financières en temps réel.

## 🎯 Objectif

Créer une plateforme robuste et scalable pour :

- Scraper des données boursières depuis plusieurs sources
- Fournir des API REST et WebSocket pour l'accès aux données
- Gérer l'authentification et les autorisations utilisateur
- Offrir un monitoring et une observabilité complets
- Supporter le déploiement en production avec Docker

## 🏗️ Architecture

### **Structure Modulaire**

```
dashboard-finance/
├── 📁 app/                    # Application principale
│   ├── 📁 api/               # Couche API (FastAPI)
│   ├── 📁 core/              # Configuration et utilitaires
│   ├── 📁 models/            # Modèles de données
│   ├── 📁 services/          # Logique métier
│   ├── 📁 repositories/      # Accès aux données
│   ├── 📁 tasks/             # Tâches Celery
│   └── 📁 utils/             # Utilitaires génériques
├── 📁 tests/                  # Tests automatisés
├── 📁 docker/                 # Configuration Docker
├── 📁 monitoring/             # Monitoring (Prometheus/Grafana)
└── 📁 ci/                     # CI/CD
```

### **Technologies Utilisées**

- **Backend**: FastAPI + Python 3.11+
- **Base de données**: PostgreSQL + SQLAlchemy + Alembic
- **Cache & Queue**: Redis + Celery
- **Scraping**: Playwright
- **Monitoring**: Prometheus + Grafana
- **Containerisation**: Docker + Docker Compose
- **Tests**: pytest + Factory Boy + Faker

## 🚀 Démarrage Rapide

### **Prérequis**

- Python 3.11+
- Docker & Docker Compose
- Git

### **Installation**

1. **Cloner le projet**

```bash
git clone <repository-url>
cd dashboard-finance
```

2. **Configurer l'environnement**

```bash
cp env.example .env
# Éditer .env avec vos configurations
```

3. **Démarrer avec Docker**

```bash
# Construire et démarrer tous les services
make docker-up

# Ou manuellement
docker-compose up -d
```

4. **Accéder à l'application**

- **API**: http://localhost:8000
- **Documentation**: http://localhost:8000/docs
- **Grafana**: http://localhost:3000 (admin/admin)
- **Prometheus**: http://localhost:9090
- **Celery Flower**: http://localhost:5555

### **Installation Locale (Alternative)**

1. **Créer un environnement virtuel**

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
```

2. **Installer les dépendances**

```bash
make install-dev
# ou
pip install -r requirements/development.txt
```

3. **Configurer la base de données**

```bash
# Démarrer PostgreSQL et Redis
docker-compose up -d postgres redis

# Initialiser la base de données
make setup-db
```

4. **Lancer l'application**

```bash
make run
# ou
uvicorn main:app --reload
```

## 🛠️ Commandes Utiles

### **Développement**

```bash
make run              # Lancer l'application
make celery-worker    # Démarrer Celery worker
make celery-beat      # Démarrer Celery beat
make celery-flower    # Démarrer Celery flower
```

### **Tests**

```bash
make test             # Tous les tests
make test-unit        # Tests unitaires
make test-integration # Tests d'intégration
make test-cov         # Tests avec couverture
```

### **Qualité du Code**

```bash
make lint             # Vérification du style
make format           # Formatage automatique
make type-check       # Vérification des types
make check-all        # Toutes les vérifications
```

### **Base de Données**

```bash
make setup-db         # Initialiser la base
make migrate          # Exécuter les migrations
make seed             # Insérer des données de test
```

### **Docker**

```bash
make docker-build     # Construire les images
make docker-up        # Démarrer les services
make docker-down      # Arrêter les services
make docker-logs      # Voir les logs
```

## 📊 Fonctionnalités

### **API REST**

- **Authentication**: JWT tokens, gestion des rôles
- **Users**: Gestion des utilisateurs et profils
- **Stocks**: Données boursières et historiques
- **Portfolios**: Gestion des portefeuilles
- **Watchlists**: Listes de surveillance personnalisées

### **WebSocket**

- Mises à jour en temps réel des cours boursiers
- Notifications de trading
- Alertes de prix

### **Scraping Automatique**

- Collecte périodique des données boursières
- Support de multiples sources (Yahoo Finance, MarketWatch, etc.)
- Gestion des rate limits et des erreurs
- Logs détaillés des opérations

### **Monitoring & Observabilité**

- Métriques Prometheus
- Dashboards Grafana
- Logs structurés avec structlog
- Health checks
- Traçage des performances

## 🔧 Configuration

### **Variables d'Environnement Principales**

```bash
# Application
APP_NAME=dashboard-finance
DEBUG=false
ENVIRONMENT=production

# Base de données
DATABASE_URL=postgresql://user:pass@localhost:5432/db

# Redis
REDIS_URL=redis://localhost:6379/0

# Sécurité
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret

# Scraping
SCRAPING_INTERVAL_MINUTES=5
ALPHA_VANTAGE_API_KEY=your-api-key
```

### **Configuration de la Base de Données**

Le projet utilise PostgreSQL avec :

- Schéma `app` pour toutes les tables
- Extensions : uuid-ossp, pg_trgm, btree_gin
- Index optimisés pour les requêtes fréquentes
- Triggers pour les timestamps automatiques

## 🧪 Tests

### **Structure des Tests**

```
tests/
├── unit/           # Tests unitaires
├── integration/    # Tests d'intégration
├── e2e/           # Tests end-to-end
├── fixtures/       # Données de test
└── conftest.py     # Configuration pytest
```

### **Exécution des Tests**

```bash
# Tests avec couverture
pytest --cov=app --cov-report=html

# Tests spécifiques
pytest tests/unit/ -v
pytest tests/integration/ -v

# Tests avec markers
pytest -m "slow"
pytest -m "integration"
```

## 📈 Monitoring

### **Prometheus**

- Métriques HTTP (requêtes, latence)
- Métriques de base de données
- Métriques Celery
- Métriques système

### **Grafana**

- Dashboard de l'application
- Métriques de performance
- Alertes configurables

### **Logs**

- Format JSON structuré
- Niveaux configurables
- Rotation automatique
- Intégration avec les systèmes de monitoring

## 🚀 Déploiement

### **Développement**

```bash
docker-compose -f docker-compose.yml up -d
```

### **Production**

```bash
docker-compose -f docker-compose.prod.yml up -d
```

### **CI/CD**

Le projet inclut des workflows GitHub Actions pour :

- Tests automatiques
- Analyse de qualité du code
- Déploiement automatique
- Sécurité et vulnérabilités

## 🔒 Sécurité

- **Authentication**: JWT tokens sécurisés
- **Authorization**: RBAC (Role-Based Access Control)
- **Rate Limiting**: Protection contre les abus
- **Input Validation**: Validation stricte des entrées
- **HTTPS**: Support SSL/TLS en production
- **Secrets**: Gestion sécurisée des clés API

## 🤝 Contribution

1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/AmazingFeature`)
3. Commit les changements (`git commit -m 'Add some AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

### **Standards de Code**

- Black pour le formatage
- isort pour l'import sorting
- flake8 pour le linting
- mypy pour le type checking
- Pre-commit hooks configurés

## 📚 Documentation

- **API**: http://localhost:8000/docs (Swagger UI)
- **Architecture**: `docs/architecture/`
- **Déploiement**: `docs/deployment/`
- **API Reference**: `docs/api/`

## 🐛 Dépannage

### **Problèmes Courants**

1. **Base de données non accessible**

```bash
docker-compose logs postgres
make setup-db
```

2. **Redis non accessible**

```bash
docker-compose logs redis
docker-compose restart redis
```

3. **Erreurs de migration**

```bash
alembic current
alembic upgrade head
```

4. **Problèmes de scraping**

```bash
docker-compose logs celery-worker
docker-compose restart celery-worker
```

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 📞 Support

- **Issues**: GitHub Issues
- **Discussions**: GitHub Discussions
- **Email**: [votre-email@example.com]

## 🙏 Remerciements

- FastAPI pour le framework web
- SQLAlchemy pour l'ORM
- Celery pour les tâches asynchrones
- Playwright pour le scraping
- La communauté Python open source

---

**Développé avec ❤️ par [Votre Nom]**
