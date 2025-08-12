module.exports = {
  apps: [{
    name: 'shopvipremium-backend',
    script: 'venv/bin/python',
    args: 'server.py',
    instances: 1,
    autorestart: true,
    watch: false,
    max_memory_restart: '1G'
  }]
}