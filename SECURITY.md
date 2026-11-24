# Politique de sécurité

Chaque règle ci-dessous est reliée au **contrôle automatique** qui la fait respecter : une règle que rien ne vérifie n'est qu'une intention.

| Règle | Contrôle |
|---|---|
| Aucun secret dans le dépôt | `gitleaks` en CI, protection au push de GitHub (Secret Protection) |
| Aucune dépendance avec faille connue | `pip-audit` en CI, Dependabot |
| Pas de motif de code dangereux connu | `bandit` en CI |
| Le code SQL ne se mélange jamais aux données | requêtes paramétrées, test `test_sql_injection_is_inert` |
| Les entrées sont validées | `test_validation` (5 cas invalides rejetés) |
| Le conteneur ne tourne pas en root | étape CI qui échoue si `id -u` vaut 0 |
| Aucune faille HIGH ou CRITICAL corrigeable dans l'image | scan `Trivy` en CI |
| Les outils de la CI ne peuvent pas être modifiés à l'insu du projet | actions épinglées par SHA de commit, mises à jour proposées par Dependabot |
| La CI n'a que le strict nécessaire | `permissions: contents: read`, `persist-credentials: false` |
| Seul du code contrôlé entre dans `main` | ruleset : Pull Request et contrôles `checks` et `docker` obligatoires, force-push interdit |
| Le compte propriétaire est protégé | double authentification (contrôle manuel, non automatisable) |

## Pourquoi épingler les actions par SHA

En mars 2026, 76 des 77 étiquettes de version de l'action `aquasecurity/trivy-action` ont été détournées pour exécuter du code malveillant dans des pipelines qui n'avaient pas changé d'une ligne. Une référence par SHA de commit est immuable : ce scénario n'aurait eu aucun effet ici.

## Signaler un problème

Ouvre une *issue* sur ce dépôt.