# mdrop
<!-- https://github.com/thppn/droplets/blob/main/mdrop.png -->
## Actions
### List
```bash
curl -X GET "https://api.digitalocean.com/v2/droplets" \
     -H "Authorization: Bearer $(cat ~/.do_token)" | jq '.droplets[] | {id: .id, name: .name, ip: .networks.v4[0].ip_address}'
```

### Create

```bash
curl -X POST "https://api.digitalocean.com/v2/droplets" \
     -H "Authorization: Bearer $(cat ~/.do_token)" \
     -H "Content-Type: application/json" \
     -d "$(jq -n --arg fingerprint "$(cat ~/.fingerprint)" '{
           name: "my-droplet",
           region: "nyc3",
           size: "s-1vcpu-1gb",
           image: "ubuntu-20-04-x64",
           ssh_keys: [$fingerprint],
           backups: false,
           ipv6: true,
           monitoring: true
         }')"

```

### Delete
```bash
curl -X DELETE "https://api.digitalocean.com/v2/droplets/$1" \
     -H "Authorization: Bearer $(cat ~/.do_token)"
```

### Connect
```bash
ssh root@$(cat ip)
```
## Configuration
### Generate SSH key
```bash
ssh-keygen -t rsa -b 4096 -C "your-email@example.com"
```

### Add Key to Digital Ocean
```bash
curl -X POST "https://api.digitalocean.com/v2/account/keys" \
     -H "Authorization: Bearer $(cat ~/.do_token)" \
     -H "Content-Type: application/json" \
     -d '{
           "name": "Termux SSH Key",
           "public_key": "'"$(cat ~/.ssh/id_rsa.pub)"'"
         }'
```
### Save fingerprint
```bash
curl -X GET "https://api.digitalocean.com/v2/account/keys" \
     -H "Authorization: Bearer $(cat ~/.do_token)" | jq -r '.ssh_keys[0].fingerprint' > fingerprint
```

### Save IP

```bash
curl -X GET "https://api.digitalocean.com/v2/droplets"      -H "Authorization: Bearer $(cat ~/.do_token)" | jq '.droplets[] | {id: .id, name: .name, ip: .networks.v4[0].ip_address}' | jq -r '.ip' > 'ip'
```