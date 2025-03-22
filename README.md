# LLM Evaluation Labs

A comprehensive platform for evaluating and comparing Large Language Models (LLMs).

## Features

- Multi-model evaluation support (OpenAI, Anthropic, Google AI, Azure OpenAI)
- Customizable evaluation metrics and criteria
- Real-time performance monitoring
- Detailed analytics and visualizations
- User authentication and role-based access control
- API rate limiting and monitoring
- Comprehensive logging and error tracking

## Prerequisites

- Python 3.11+
- Node.js 20+
- PostgreSQL 15+
- Redis 7+
- Docker and Docker Compose

## Quick Start

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/llm-evaluation-labs.git
   cd llm-evaluation-labs
   ```

2. Set up environment variables:
   ```bash
   cp backend/.env.example backend/.env
   # Edit .env with your configuration
   ```

3. Start the development environment:
   ```bash
   docker-compose up -d
   ```

4. Initialize the database:
   ```bash
   docker-compose exec backend alembic upgrade head
   ```

5. Access the application:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs
   - PgAdmin: http://localhost:5050

## Required API Keys

1. Authentication:
   - Generate JWT secret: `openssl rand -hex 32`

2. LLM Providers:
   - OpenAI API Key: https://platform.openai.com/api-keys
   - Anthropic API Key: https://console.anthropic.com/
   - Azure OpenAI: Azure Portal > OpenAI resource
   - Google AI API Key: Google Cloud Console

3. Monitoring:
   - Sentry DSN: https://sentry.io
   - New Relic License Key: New Relic account settings

4. AWS (for production):
   - AWS Access Key ID
   - AWS Secret Access Key
   - S3 Bucket Name

## Development

1. Install backend dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. Install frontend dependencies:
   ```bash
   cd frontend
   npm install
   ```

3. Run tests:
   ```bash
   # Backend tests
   cd backend
   pytest

   # Frontend tests
   cd frontend
   npm test
   ```

## Production Deployment

1. Configure production environment variables
2. Build and push Docker images
3. Deploy using your preferred orchestration tool (e.g., Kubernetes, ECS)

### AWS Deployment Prerequisites:

1. Create ECR repositories:
   ```bash
   aws ecr create-repository --repository-name llm-eval-frontend
   aws ecr create-repository --repository-name llm-eval-backend
   ```

2. Create ECS cluster and services
3. Configure GitHub Actions secrets:
   - AWS_ACCESS_KEY_ID
   - AWS_SECRET_ACCESS_KEY
   - AWS_REGION

## Architecture

- Frontend: React + TypeScript + Vite
- Backend: FastAPI + SQLAlchemy
- Database: PostgreSQL
- Cache: Redis
- CI/CD: GitHub Actions
- Monitoring: Sentry + New Relic
- Deployment: AWS (ECR + ECS)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License - see LICENSE file for details
