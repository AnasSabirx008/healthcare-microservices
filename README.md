
                                [ Machine Locale (Développeur) ]
                                               │
                                               │ (Seeding SQL - Port 3306)
                                               ▼
[ Utilisateur / Client ] ──────────────► [ Application Load Balancer ] (healthcare-alb)
                                               │ (SG: healthcare-alb-sg)
                                               │ (HTTP - Port 80)
                                               │
                      ┌────────────────────────┴────────────────────────┐
                      │ Path: /                                         │ Path: /admin/*
                      ▼                                                 ▼
        [ Target Group: patient-tg ]                     [ Target Group: staff-tg ]
              (Port 5000 / IP)                                 (Port 5000 / IP)
                      │                                                 │
                      ▼                                                 ▼
        [ ECS Service: patient-service ]                 [ ECS Service: staff-service ]
         (Fargate Task / Port 5000)                       (Fargate Task / Port 5000)
         (SG: ecs-tasks-sg)                               (SG: ecs-tasks-sg)
         (Image: patient-service:latest)                  (Image: staff-service:latest)
                      │                                                 │
                      └────────────────────────┬────────────────────────┘
                                               │ (MySQL - Port 3306)
                                               ▼
                                 [ Amazon RDS MySQL DB ] (healthcare-db)
                                       (Port 3306 / DB Name: clinic)
                                       (SG: default / rds-sg)
