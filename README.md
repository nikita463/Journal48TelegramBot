### Docker compose configuration file
```bash
curl -Lo docker-compose.yaml https://raw.githubusercontent.com/nikita463/Journal48TelegramBot/refs/heads/master/docker-compose-prod.yaml
```

### .env file
```bash
curl -Lo .env https://raw.githubusercontent.com/nikita463/Journal48TelegramBot/refs/heads/master/.env-example
```

---

### Docker compose up
```bash
docker compose up -d && docker compose logs -ft
```

### Upgrade
```bash
docker compose down && docker compose pull && docker compose up -d && docker compose logs -ft
```