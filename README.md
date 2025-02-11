# Placement Prediction System

A machine learning system for predicting student placements using various models. The system provides both a CLI and web interface for making predictions, with separate Docker configurations for each.

## 📁 Repository Structure

```
.
├── placement_predictor_cli_app/           # CLI Application
│   ├── cli.py                    # Command-line interface
│   ├── Dockerfile                # Docker configuration for CLI
│   ├── requirements.txt          # Python dependencies for CLI
│   ├── models/                   # Trained ML models
│   │   └── trained_models.pkl    # Saved models
│   ├── predictions/              # Generated predictions
│   └── X_test.csv                # Test dataset
│
└── placement_predictor_flask_app/ # Web Application
    ├── app.py                    # Flask web application
    ├── Dockerfile                # Docker configuration for web app
    ├── requirements.txt          # Python dependencies for web app
    ├── models/                   # Trained ML models
    ├── templates/                # HTML templates
    ├── uploads/                  # Temporary upload directory
    ├── predictions/              # Generated predictions
    └── testdata.csv              # Test dataset
```

## 🚀 Setup and Installation

### Prerequisites

- Docker
- Git

### CLI Application Setup

1. Build the CLI Docker image:

```bash
cd placement_predictor
docker build -t placement-predictor-cli .
```

2. Run the CLI application:

```bash
docker run placement-predictor-cli
```

### Web Application Setup

1. Build the web application Docker image:

```bash
cd placement_predictor_flask_app
docker build -t placement-predictor-web .
```

2. Run the web application:

```bash
docker run -p 5002:5002 placement-predictor-web
```

The web interface will be available at `http://localhost:5002`

## 🖥️ Using the Applications

### CLI Application

The CLI provides an interactive interface for:

- Single student prediction
- Batch predictions from CSV files
- Model selection options

Example usage:

```bash
docker run placement-predictor-cli
```

### Web Application

The web interface allows you to:

- Upload CSV files for prediction
- View predictions in the browser
- Download prediction results
- Access through any web browser at `http://localhost:5002`

## 📊 Input Data Format

The system expects CSV files with the following columns:

```
StudentID,CGPA,Internships,Projects,Workshops/Certifications,AptitudeTestScore,SoftSkillsRating,ExtracurricularActivities,PlacementTraining,SSC_Marks,HSC_Marks

```

## 🔍 Troubleshooting

Common issues and solutions:

1. **Docker container fails to start**

   - Check if port 5002 is available (for web app)
   - Ensure model files are in the correct location
   - Verify Docker is running

2. **Prediction errors**

   - Verify input data format matches requirements
   - Check if all required columns are present
   - Ensure values are within expected ranges

## 📜 Architecture Diagrams

### Web Application

```mermaid
graph TD
    subgraph Client
        A[Web Browser] -->|Upload CSV| B[Flask Web Interface]
    end

    subgraph Flask Application
        B -->|POST /predict_batch| C[Flask Server]
        C -->|Save| D[Temporary Upload Directory]
        D -->|Read| E[Data Preprocessing]
        
        subgraph Model Pipeline
            E -->|Normalize Data| F[Deep Learning Model]
            F -->|Make Predictions| G[Generate Results]
        end
        
        G -->|Save| H[Predictions Directory]
        G -->|JSON Response| B
    end

    subgraph File System
        I[models/best_model.h5] -->|Load at Startup| F
        J[templates/index.html] -->|Render| B
        K[uploads/] ---|Temporary Storage| D
        L[predictions/*.csv] ---|Store Results| H
    end

    style Client fill:#f9f,stroke:#333,stroke-width:2px
    style Flask Application fill:#bbf,stroke:#333,stroke-width:2px
    style Model Pipeline fill:#bfb,stroke:#333,stroke-width:2px
    style File System fill:#fbb,stroke:#333,stroke-width:2px
```

### CLI Application

```mermaid
graph TD
    subgraph CLI Interface
        A[Start CLI] -->|Main Menu| B{User Choice}
        B -->|Choice 1| C[Single Student Prediction]
        B -->|Choice 2| D[Batch CSV Prediction]
        B -->|Choice 3| E[Exit Program]
    end

    subgraph Single Prediction Flow
        C -->|Input Features| F[Get User Input]
        F -->|Validate Input| G[Create DataFrame]
        G -->|Preprocess| H[Normalized Data]
        H -->|Predict| I[Deep Learning Model]
        I -->|Display| J[Show Result]
    end

    subgraph Batch Prediction Flow
        D -->|Input CSV Path| K[Read CSV File]
        K -->|Process Data| L[Preprocess Features]
        L -->|Batch Predict| I
        I -->|Save Results| M[predictions/predictions_deep_learning.csv]
    end

    subgraph File System
        N[models/best_model.h5] -->|Load at Startup| I
        O[Input CSV] -->|Read| K
        M -->|Write| P[Predictions Directory]
    end

    style CLI Interface fill:#f9f,stroke:#333,stroke-width:2px
    style Single Prediction Flow fill:#bbf,stroke:#333,stroke-width:2px
    style Batch Prediction Flow fill:#bfb,stroke:#333,stroke-width:2px
    style File System fill:#fbb,stroke:#333,stroke-width:2px
```

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

