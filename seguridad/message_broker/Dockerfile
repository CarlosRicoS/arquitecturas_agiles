# Use official RabbitMQ image with plugins
FROM rabbitmq:4.0-management

# Enable RabbitMQ JWT authentication plugin
RUN rabbitmq-plugins enable --offline rabbitmq_auth_backend_jwt

# Expose ports
EXPOSE 5672 15672

# Start RabbitMQ server
CMD ["rabbitmq-server"]
