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

### Web Application Flow

```mermaid
graph TD
    subgraph User Interface
        A[Web Browser] -->|Upload CSV| B[Flask Interface]
        B -->|Display Results| A
    end

    subgraph Server
        B -->|POST /predict| C[Flask Backend]
        C -->|Save File| D[Upload Directory]
        D -->|Process| E[Data Preprocessing]
        
        subgraph ML Pipeline
            E -->|Normalize| F[Feature Engineering]
            F -->|Predict| G[Deep Learning Model]
            G -->|Generate| H[Results Processing]
        end
        
        H -->|Store| I[Predictions Directory]
        H -->|JSON| B
    end

    subgraph Storage
        J[models/best_model.h5] -.->|Load| G
        K[templates/*.html] -.->|Render| B
        L[uploads/*] -.->|Read| D
        M[predictions/*.csv] <-.->|Save/Load| I
    end

    classDef interface fill:#ff9999,stroke:#333,stroke-width:2px
    classDef server fill:#99ff99,stroke:#333,stroke-width:2px
    classDef storage fill:#9999ff,stroke:#333,stroke-width:2px
    classDef pipeline fill:#ffff99,stroke:#333,stroke-width:2px
    
    class A,B interface
    class C,D,E,H server
    class F,G pipeline
    class J,K,L,M storage
```

### CLI Application Flow

```mermaid
graph TD
    subgraph CLI Interface
        A[Start Program] -->|Display| B{Main Menu}
        B -->|1| C[Single Prediction]
        B -->|2| D[Batch Prediction]
        B -->|3| E[Exit]
    end

    subgraph Single Input Flow
        C -->|Collect| F[User Inputs]
        F -->|Validate| G[Input Processing]
        G -->|Format| H[Create DataFrame]
    end

    subgraph Batch Input Flow
        D -->|Read| I[CSV File]
        I -->|Validate| J[Data Validation]
        J -->|Process| K[Batch Processing]
    end

    subgraph Prediction Pipeline
        H -->|Forward| L[ML Model]
        K -->|Forward| L
        L -->|Generate| M[Predictions]
        M -->|Format| N[Results]
    end

    N -->|Display| O[Output Results]
    N -->|Save| P[predictions/*.csv]

    classDef interface fill:#f9a,stroke:#333,stroke-width:2px
    classDef flow fill:#aff,stroke:#333,stroke-width:2px
    classDef pipeline fill:#ffa,stroke:#333,stroke-width:2px
    classDef output fill:#aaf,stroke:#333,stroke-width:2px

    class A,B,C,D,E interface
    class F,G,H,I,J,K flow
    class L,M pipeline
    class N,O,P output
```

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.