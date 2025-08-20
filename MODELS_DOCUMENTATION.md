# 🗄️ Documentation des Modèles SQLAlchemy - Dashboard Finance

## 🎯 Vue d'Ensemble

Cette documentation décrit tous les modèles SQLAlchemy créés pour le projet Dashboard Finance. Ces modèles forment la base de données et gèrent les relations entre les entités principales.

## 📊 Structure des Modèles

### **1. Modèle User (Utilisateur)**

**Fichier** : `app/models/user.py`

**Table** : `users`

**Champs** :

- `id` : Clé primaire auto-incrémentée
- `email` : Email unique de l'utilisateur
- `username` : Nom d'utilisateur unique
- `password_hash` : Hash du mot de passe (bcrypt)
- `first_name` : Prénom (optionnel)
- `last_name` : Nom de famille (optionnel)
- `role` : Rôle utilisateur (USER, PREMIUM, ADMIN)
- `is_active` : Statut actif/inactif
- `is_verified` : Email vérifié ou non
- `created_at` : Date de création
- `updated_at` : Date de dernière modification
- `last_login` : Dernière connexion

**Relations** :

- `portfolios` → `UserPortfolio` (1:N)
- `watchlists` → `Watchlist` (1:N)

**Propriétés** :

- `full_name` : Nom complet (prénom + nom)
- `is_admin` : Vérifie si admin
- `is_premium` : Vérifie si accès premium

**Enum UserRole** :

```python
USER = "user"      # Utilisateur standard
PREMIUM = "premium" # Utilisateur premium
ADMIN = "admin"    # Administrateur
```

---

### **2. Modèle Stock (Action)**

**Fichier** : `app/models/stock.py`

**Table** : `stocks`

**Champs** :

- `id` : Clé primaire auto-incrémentée
- `symbol` : Symbole boursier unique (ex: AAPL)
- `name` : Nom de l'entreprise
- `isin` : Numéro ISIN international (optionnel)
- `market` : Marché (NYSE, NASDAQ, etc.)
- `market_type` : Type d'instrument (STOCK, ETF, INDEX, CRYPTO, FOREX)
- `currency` : Devise (USD, EUR, etc.)
- `sector` : Secteur d'activité
- `industry` : Industrie spécifique
- `company_description` : Description de l'entreprise
- `website` : Site web officiel
- `market_cap` : Capitalisation boursière
- `pe_ratio` : Ratio P/E
- `dividend_yield` : Rendement du dividende
- `beta` : Coefficient bêta
- `is_active` : Action active/inactive
- `is_tradable` : Action négociable
- `created_at` : Date de création
- `updated_at` : Date de modification
- `last_price_update` : Dernière mise à jour des prix

**Relations** :

- `prices` → `StockPrice` (1:N)
- `portfolios` → `UserPortfolio` (1:N)
- `watchlists` → `WatchlistItem` (1:N)

**Propriétés** :

- `display_name` : Nom d'affichage (symbole + nom)
- `is_index` : Vérifie si c'est un indice
- `is_crypto` : Vérifie si c'est une crypto

**Enum MarketType** :

```python
STOCK = "stock"     # Action classique
ETF = "etf"         # Fonds négocié en bourse
INDEX = "index"     # Indice boursier
CRYPTO = "crypto"   # Cryptomonnaie
FOREX = "forex"     # Devise
```

---

### **3. Modèle StockPrice (Prix des Actions)**

**Fichier** : `app/models/stock_price.py`

**Table** : `stock_prices`

**Champs** :

- `id` : Clé primaire auto-incrémentée
- `stock_id` : Référence vers l'action (FK)
- `open_price` : Prix d'ouverture
- `high_price` : Prix le plus haut
- `low_price` : Prix le plus bas
- `close_price` : Prix de clôture
- `adjusted_close` : Prix ajusté (splits/dividendes)
- `volume` : Volume échangé
- `average_volume` : Volume moyen
- `change_amount` : Variation en valeur absolue
- `change_percent` : Variation en pourcentage
- `source` : Source des données (yahoo, alpha_vantage, etc.)
- `data_quality` : Qualité des données (high, medium, low)
- `timestamp` : Horodatage des données
- `created_at` : Date de création de l'enregistrement

**Relations** :

- `stock` → `Stock` (N:1)

**Index** :

- `idx_stock_timestamp` : (stock_id, timestamp)
- `idx_timestamp_source` : (timestamp, source)

**Propriétés** :

- `price_range` : Fourchette de prix (high - low)
- `is_up_day` : Jour de hausse (close > open)
- `is_down_day` : Jour de baisse (close < open)

---

### **4. Modèle UserPortfolio (Portefeuille Utilisateur)**

**Fichier** : `app/models/user_portfolio.py`

**Table** : `user_portfolios`

**Champs** :

- `id` : Clé primaire auto-incrémentée
- `user_id` : Référence vers l'utilisateur (FK)
- `stock_id` : Référence vers l'action (FK)
- `quantity` : Quantité d'actions
- `average_price` : Prix d'achat moyen
- `total_invested` : Montant total investi
- `notes` : Notes utilisateur (optionnel)
- `purchase_date` : Date d'achat (optionnel)
- `is_active` : Position active (active, sold, closed)
- `created_at` : Date de création
- `updated_at` : Date de modification

**Relations** :

- `user` → `User` (N:1)
- `stock` → `Stock` (N:1)

**Propriétés** :

- `current_value` : Valeur actuelle de la position
- `unrealized_pnl` : Plus/moins value latente
- `position_size` : Taille de position (small, medium, large)

---

### **5. Modèle Watchlist (Liste de Surveillance)**

**Fichier** : `app/models/watchlist.py`

**Table** : `watchlists`

**Champs** :

- `id` : Clé primaire auto-incrémentée
- `user_id` : Référence vers l'utilisateur (FK)
- `name` : Nom de la liste
- `description` : Description (optionnel)
- `is_default` : Liste par défaut
- `created_at` : Date de création
- `updated_at` : Date de modification

**Relations** :

- `user` → `User` (N:1)
- `items` → `WatchlistItem` (1:N)

---

### **6. Modèle WatchlistItem (Élément de Liste de Surveillance)**

**Fichier** : `app/models/watchlist.py`

**Table** : `watchlist_items`

**Champs** :

- `id` : Clé primaire auto-incrémentée
- `watchlist_id` : Référence vers la liste (FK)
- `stock_id` : Référence vers l'action (FK)
- `notes` : Notes utilisateur (optionnel)
- `target_price` : Prix cible pour alertes
- `alert_enabled` : Alertes activées
- `created_at` : Date de création

**Relations** :

- `watchlist` → `Watchlist` (N:1)
- `stock` → `Stock` (N:1)

---

### **7. Modèle ScrapingLog (Journal de Scraping)**

**Fichier** : `app/models/scraping_log.py`

**Table** : `scraping_logs`

**Champs** :

- `id` : Clé primaire auto-incrémentée
- `source` : Source des données
- `scraping_type` : Type de scraping
- `target_symbol` : Symbole cible (optionnel)
- `status` : Statut de l'opération
- `started_at` : Début du scraping
- `completed_at` : Fin du scraping (optionnel)
- `duration` : Durée en secondes
- `records_processed` : Enregistrements traités
- `records_updated` : Enregistrements mis à jour
- `records_created` : Enregistrements créés
- `error_message` : Message d'erreur (optionnel)
- `retry_count` : Nombre de tentatives
- `max_retries` : Nombre maximum de tentatives
- `user_agent` : User-Agent utilisé
- `ip_address` : Adresse IP
- `request_headers` : En-têtes de requête
- `created_at` : Date de création
- `updated_at` : Date de modification

**Relations** : Aucune (table de logs)

**Enums** :

```python
ScrapingStatus: PENDING, IN_PROGRESS, SUCCESS, FAILED, TIMEOUT, RATE_LIMITED
ScrapingType: STOCK_PRICE, COMPANY_INFO, FINANCIAL_DATA, MARKET_DATA, NEWS
```

**Propriétés** :

- `is_successful` : Vérifie si réussi
- `is_failed` : Vérifie si échec
- `can_retry` : Vérifie si retry possible
- `efficiency_rate` : Taux d'efficacité

---

## 🔗 Relations entre Modèles

```
User (1) ←→ (N) UserPortfolio (N) ←→ (1) Stock (1) ←→ (N) StockPrice
  ↓
  (1) ←→ (N) Watchlist (1) ←→ (N) WatchlistItem (N) ←→ (1) Stock
```

**Explications** :

- Un utilisateur peut avoir plusieurs positions en portefeuille
- Un utilisateur peut avoir plusieurs listes de surveillance
- Une action peut avoir plusieurs prix historiques
- Une action peut être dans plusieurs portefeuilles
- Une action peut être dans plusieurs listes de surveillance

---

## 🚀 Utilisation des Modèles

### **Import des Modèles**

```python
from app.models import User, Stock, StockPrice, UserPortfolio, Watchlist
```

### **Création d'Instances**

```python
# Créer un utilisateur
user = User(
    email="john@example.com",
    username="john_doe",
    password_hash="hashed_password",
    first_name="John",
    last_name="Doe"
)

# Créer une action
stock = Stock(
    symbol="AAPL",
    name="Apple Inc.",
    market="NASDAQ",
    sector="Technology"
)
```

### **Relations**

```python
# Ajouter une action à un portefeuille
portfolio_item = UserPortfolio(
    user_id=user.id,
    stock_id=stock.id,
    quantity=100,
    average_price=150.0,
    total_invested=15000.0
)

# Créer une liste de surveillance
watchlist = Watchlist(
    user_id=user.id,
    name="Tech Stocks",
    description="Actions technologiques à surveiller"
)
```

---

## 📝 Prochaines Étapes

### **1. Création des Tables**

- [ ] Exécuter `create_tables()` pour créer toutes les tables
- [ ] Configurer Alembic pour les migrations

### **2. Repositories**

- [ ] Créer les repositories pour chaque modèle
- [ ] Implémenter les opérations CRUD

### **3. Services**

- [ ] Créer les services métier
- [ ] Implémenter la logique de gestion des portefeuilles

### **4. API Endpoints**

- [ ] Créer les endpoints pour chaque modèle
- [ ] Implémenter l'authentification et autorisation

---

## 🔍 Tests et Validation

### **Test des Modèles**

```bash
# Dans le conteneur Docker
docker compose exec app python -c "
from app.models import User, Stock
print('✅ Models imported successfully!')
"
```

### **Vérification de la Structure**

- Tous les modèles peuvent être importés
- Les relations sont correctement définies
- Les propriétés calculées fonctionnent
- Les enums sont valides

---

**✅ Statut** : Tous les modèles SQLAlchemy sont créés et fonctionnels
**🔜 Prochaine étape** : Créer les repositories et implémenter la logique métier
