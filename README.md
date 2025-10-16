### Docker compose configuration file
```bash
curl -Lo docker-compose.yaml https://raw.githubusercontent.com/nikita463/Journal48TelegramBot/refs/heads/master/docker-compose-prod.yaml
```

### .env file
```bash
curl -Lo .env https://raw.githubusercontent.com/nikita463/Journal48TelegramBot/refs/heads/master/.env-example
```

### data.json file
```bash
curl -Lo data.json https://raw.githubusercontent.com/nikita463/Journal48TelegramBot/refs/heads/master/data-example.json
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