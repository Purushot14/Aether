# 🌩️ Aether – AI-Powered Cloud Cost Optimization Platform

Aether is a cloud-native, AI-augmented platform designed to help platform teams identify and reduce overprovisioned infrastructure costs across Kubernetes and multi-cloud workloads.

---

## 🚀 Features

- 🤖 **AI-based Resource Right-Sizing** – Predicts optimal CPU/Memory for K8s workloads using Isolation Forest
- 📏 **Rule-based Recommendations** – Plain Python logic to suggest actions based on historical usage
- 📊 **Interactive Dashboard** – Streamlit UI to visualize savings opportunities per tenant
- 🔧 **Terraform IaC Modules** – EKS + Prometheus observability infrastructure
- 🔐 **Multi-Tenant & GitOps Friendly** – Secure, modular, and CI/CD ready

---

## 🧱 Project Structure

```
aether/
├── api/                   # FastAPI service (stubbed)
├── ai_engine/             # AI/ML logic (Isolation Forest model)
│   └── right_sizer.py
├── rules/                 # Pure Python rule engine
│   └── rule_engine.py
├── data_pipeline/         # (To be implemented: metric ingestion)
├── dashboard/             # Streamlit dashboard
│   └── app.py
├── infra/
│   └── terraform/         # IaC setup for EKS + Prometheus
│       ├── modules/
│       │   ├── eks/
│       │   └── prometheus/
│       └── environments/
│           └── dev/terraform.tfvars
├── pyproject.toml         # Poetry dependencies
├── docker-compose.yml     # Local dev setup
└── README.md              # You're here!
```

---

## 🧪 How to Run Everything

### 1. 🔧 Install Dependencies (Poetry)

```bash
poetry install
```

---

### 2. 🤖 Run the AI Right-Sizing Engine

```bash
poetry run python ai_engine/right_sizer.py
```

> Outputs recommended CPU/memory for pods with confidence score based on usage data.

---

### 3. 📏 Run the Rule Engine

```bash
poetry run python rules/rule_engine.py
```

> Evaluates sample workloads and prints rule-based recommendations like:
```
[RECOMMENDATION] analytics-pod: scale_down_cpu — CPU usage below 40% for 7+ days
```

---

### 4. 📊 Launch the Streamlit Dashboard

```bash
poetry run streamlit run dashboard/app.py
```

> View recommendations in a tabular format with tenant-wise filtering.

---

### 5. 🛠️ Provision Infrastructure with Terraform

#### Setup

Update your `terraform.tfvars` with valid `vpc_id` and `subnet_ids` in:

```hcl
aether/infra/terraform/environments/dev/terraform.tfvars
```

#### Run

```bash
cd aether/infra/terraform/modules/eks
terraform init
terraform apply -var-file=../../environments/dev/terraform.tfvars

cd ../prometheus
terraform init
terraform apply
```

---

## 🧠 Model Details

- **Model:** Isolation Forest
- **Use:** Detects underutilized workloads for downscaling
- **Extension:** Forecasting (Prophet, LSTM) planned in future versions

---

## 🔐 Security Principles

- Least-privilege IAM for AWS modules
- GitOps workflow compatible (ArgoCD/Flux ready)
- Future: Auth-enabled dashboards + multi-tenant K8s namespaces

---

## 📥 Contributing

We welcome:
- New ML-based optimization techniques
- Alerting & notification plugins
- GitHub PR-based automation logic

---

## 📄 License

MIT License — feel free to build on top of it.