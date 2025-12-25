# Claude Docker Setup

A Docker-based setup for running Claude locally with Python and Anthropic API

## Features

- **Multi-stage Docker build** for optimized image size
- - **Docker Compose** configuration for easy deployment
  - - **Python 3.11** with latest Anthropic SDK
    - - **Environment variable management** with .env support
      - - **Health checks** to ensure container stability
        - - **Volume mounts** for persistent cache and development
          - - **Network isolation** with custom Docker network
           
            - ## Prerequisites
           
            - - Docker Desktop or Docker Engine installed
              - - Anthropic API key (get one at [console.anthropic.com](https://console.anthropic.com))
                - - Python 3.9+ (for local development)
                  - - Git
                   
                    - ## Quick Start
                   
                    - ### 1. Clone the Repository
                   
                    - ```bash
                      git clone https://github.com/the-steele-zone/claude-docker-setup.git
                      cd claude-docker-setup
                      ```

                      ### 2. Set Up Environment Variables

                      ```bash
                      cp .env.example .env
                      # Edit .env and add your ANTHROPIC_API_KEY
                      nano .env
                      ```

                      **Important:** Never commit your `.env` file to version control.

                      ### 3. Build and Run with Docker Compose

                      ```bash
                      # Build the Docker image
                      docker-compose build

                      # Start the container
                      docker-compose up -d

                      # View logs
                      docker-compose logs -f claude
                      ```

                      ### 4. Run the Application

                      ```bash
                      # Interactive mode
                      docker-compose exec claude python app.py

                      # Or access the running container
                      docker-compose exec claude /bin/bash
                      ```

                      ## Docker Commands Reference

                      ### Build the Image

                      ```bash
                      docker build -t claude-app .
                      ```

                      ### Run the Container

                      ```bash
                      docker run -it --env-file .env claude-app
                      ```

                      ### Docker Compose

                      ```bash
                      # Start services
                      docker-compose up

                      # Run in background
                      docker-compose up -d

                      # Stop services
                      docker-compose down

                      # View logs
                      docker-compose logs -f

                      # Execute command
                      docker-compose exec claude python app.py
                      ```

                      ## Project Structure

                      ```
                      claude-docker-setup/
                      ├── Dockerfile              # Multi-stage Docker build
                      ├── docker-compose.yml      # Docker Compose configuration
                      ├── requirements.txt        # Python dependencies
                      ├── app.py                  # Example application
                      ├── .env.example           # Example environment variables
                      ├── .gitignore             # Git ignore rules
                      └── README.md              # This file
                      ```

                      ## Configuration

                      ### Environment Variables

                      The `.env` file contains:

                      - `ANTHROPIC_API_KEY`: Your Anthropic API key (required)
                      - - `PYTHONUNBUFFERED=1`: Unbuffered Python output
                        - - `PYTHONDONTWRITEBYTECODE=1`: Disable .pyc files
                         
                          - ### Docker Compose Configuration
                         
                          - The `docker-compose.yml` includes:
                         
                          - - **Service**: Claude application container
                            - - **Volumes**: Code mounting and cache persistence
                              - - **Ports**: Port 8000 exposed for external access
                                - - **Health checks**: Automatic health monitoring
                                  - - **Networks**: Isolated network for security
                                   
                                    - ## Development
                                   
                                    - ### Local Development (Without Docker)
                                   
                                    - ```bash
                                      # Create virtual environment
                                      python -m venv venv
                                      source venv/bin/activate  # On Windows: venv\Scripts\activate

                                      # Install dependencies
                                      pip install -r requirements.txt

                                      # Set environment variable
                                      export ANTHROPIC_API_KEY="your-key-here"

                                      # Run the application
                                      python app.py
                                      ```

                                      ### Modifying the Application

                                      Edit `app.py` to customize the Claude integration. The example includes:

                                      - Interactive conversation with Claude
                                      - - Conversation history management
                                        - - Error handling
                                          - - User-friendly prompts
                                           
                                            - ## API Reference
                                           
                                            - The application uses the Anthropic Python SDK:
                                           
                                            - ```python
                                              from anthropic import Anthropic

                                              client = Anthropic(api_key="your-key")
                                              message = client.messages.create(
                                                  model="claude-sonnet-4-5-20250929",
                                                  max_tokens=1024,
                                                  messages=[{"role": "user", "content": "Hello!"}]
                                              )
                                              ```

                                              For detailed documentation, visit [docs.anthropic.com](https://docs.anthropic.com)

                                              ## Troubleshooting

                                              ### API Key Not Found

                                              Ensure `.env` file exists in the project root with your API key:
                                              ```bash
                                              ANTHROPIC_API_KEY=your-actual-key
                                              ```

                                              ### Port Already in Use

                                              If port 8000 is in use, modify `docker-compose.yml`:
                                              ```yaml
                                              ports:
                                                - "8001:8000"  # Changed from 8000:8000
                                              ```

                                              ### Docker Build Issues

                                              Clean up and rebuild:
                                              ```bash
                                              docker-compose down
                                              docker system prune
                                              docker-compose build --no-cache
                                              ```

                                              ### Permission Denied

                                              On Linux, add your user to docker group:
                                              ```bash
                                              sudo usermod -aG docker $USER
                                              ```

                                              ## Security Considerations

                                              - **Never commit `.env`**: API keys should never be in version control
                                              - - **Use Docker secrets** for production deployments
                                              - **Limit container resources** with memory/CPU constraints
                                              - - **Use environment variables** for sensitive data
                                                - - **Keep dependencies updated** regularly
                                                 
                                                  - ## Performance Tips
                                                 
                                                  - - Use **multi-stage builds** to reduce image size
                                                    - - **Cache Docker layers** effectively
                                                      - - **Limit max_tokens** to optimize API usage
                                                        - - **Reuse connections** when making multiple requests
                                                          - - **Monitor container resources** with `docker stats`
                                                           
                                                            - ## Support and Feedback
                                                            - 
                                                            For issues or suggestions, please open an issue on GitHub.

## License

MIT License - feel free to use and modify

## Links

- [Anthropic Documentation](https://docs.anthropic.com)
- - [Docker Documentation](https://docs.docker.com)
  - - [Docker Compose Documentation](https://docs.docker.com/compose)
    - - [Python SDK Repository](https://github.com/anthropics/anthropic-sdk-python)
