// PM2 Ecosystem Configuration for Shop VIP Premium
// This file will be used by the deployment script

module.exports = {
  apps: [{
    name: 'shopvippremium-backend',
    script: 'venv/bin/python',
    args: '-m uvicorn server:app --host 0.0.0.0 --port 8001 --workers 4',
    cwd: '/var/www/shopvippremium/backend',
    instances: 1,
    autorestart: true,
    watch: false,
    max_memory_restart: '1G',
    env: {
      NODE_ENV: 'production',
      PYTHONPATH: '/var/www/shopvippremium/backend',
      MONGO_URL: 'mongodb://localhost:27017',
      DB_NAME: 'shopvippremium_db'
    },
    error_file: '/var/log/pm2/shopvippremium-backend-error.log',
    out_file: '/var/log/pm2/shopvippremium-backend-out.log',
    log_file: '/var/log/pm2/shopvippremium-backend.log',
    time: true,
    log_date_format: 'YYYY-MM-DD HH:mm:ss Z',
    
    // Advanced PM2 configuration
    min_uptime: '10s',
    max_restarts: 10,
    restart_delay: 4000,
    
    // Health monitoring
    health_check_grace_period: 3000,
    health_check_fatal_exceptions: true,
    
    // Performance monitoring
    monitoring: true,
    pmx: true,
    
    // Auto-restart conditions
    node_args: '--max-old-space-size=1024',
    
    // Graceful shutdown
    kill_timeout: 5000,
    shutdown_with_message: true,
    
    // Log rotation
    log_type: 'json',
    merge_logs: true,
    
    // Environment specific settings
    env_production: {
      NODE_ENV: 'production',
      PORT: 8001,
      PYTHONPATH: '/var/www/shopvippremium/backend'
    },
    
    env_development: {
      NODE_ENV: 'development',
      PORT: 8001,
      PYTHONPATH: './backend'
    }
  }],

  // Deployment configuration
  deploy: {
    production: {
      user: 'root',
      host: 'shopvippremium.com',
      ref: 'origin/main',
      repo: 'https://github.com/yourusername/shopvippremium.git',
      path: '/var/www/shopvippremium',
      'pre-deploy-local': '',
      'post-deploy': 'cd backend && source venv/bin/activate && pip install -r requirements.txt && cd ../frontend && yarn install && yarn build && pm2 reload ecosystem.config.js --env production',
      'pre-setup': '',
      'post-setup': 'cd backend && python3.11 -m venv venv && source venv/bin/activate && pip install -r requirements.txt && cd ../frontend && yarn install',
      env: {
        NODE_ENV: 'production'
      }
    }
  }
};